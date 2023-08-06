import datetime
import json
import logging
import numbers
import os
import pathlib
from typing import Dict, List, Union

import fastjsonschema

from aws_lambda_powertools.helper.models import MetricUnit

from .exceptions import MetricUnitError, MetricValueError, SchemaValidationError, UniqueNamespaceError

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

_schema_path = pathlib.Path(__file__).parent / "./schema.json"
with _schema_path.open() as f:
    CLOUDWATCH_EMF_SCHEMA = json.load(f)


class MetricManager:
    """Base class for metric functionality (namespace, metric, dimension, serialization)

    MetricManager creates metrics asynchronously thanks to CloudWatch Embedded Metric Format (EMF).
    CloudWatch EMF can create up to 100 metrics per EMF object
    and metrics, dimensions, and namespace created via MetricManager
    will adhere to the schema, will be serialized and validated against EMF Schema.

    **Use `aws_lambda_powertools.metrics.metrics.Metrics` or
    `aws_lambda_powertools.metrics.metric.single_metric` to create EMF metrics.**

    Environment variables
    ---------------------
    POWERTOOLS_METRICS_NAMESPACE : str
        metric namespace to be set for all metrics

    Raises
    ------
    MetricUnitError
        When metric metric isn't supported by CloudWatch
    MetricValueError
        When metric value isn't a number
    UniqueNamespaceError
        When an additional namespace is set
    SchemaValidationError
        When metric object fails EMF schema validation
    """

    def __init__(self, metric_set: Dict[str, str] = None, dimension_set: Dict = None, namespace: str = None):
        self.metric_set = metric_set or {}
        self.dimension_set = dimension_set or {}
        self.namespace = os.getenv("POWERTOOLS_METRICS_NAMESPACE") or namespace

    def add_namespace(self, name: str):
        """Adds given metric namespace

        Example
        -------
        **Add metric namespace**

            metric.add_namespace(name="ServerlessAirline")

        Parameters
        ----------
        name : str
            Metric namespace
        """
        if self.namespace is not None:
            raise UniqueNamespaceError(
                f"Namespace '{self.namespace}' already set - Only one namespace is allowed across metrics"
            )
        logger.debug(f"Adding metrics namespace: {name}")
        self.namespace = name

    def add_metric(self, name: str, unit: MetricUnit, value: Union[float, int]):
        """Adds given metric

        Example
        -------
        **Add given metric using MetricUnit enum**

            metric.add_metric(name="BookingConfirmation", unit=MetricUnit.Count, value=1)

        **Add given metric using plain string as value unit**

            metric.add_metric(name="BookingConfirmation", unit="Count", value=1)

        Parameters
        ----------
        name : str
            Metric name
        unit : MetricUnit
            `aws_lambda_powertools.helper.models.MetricUnit`
        value : float
            Metric value

        Raises
        ------
        MetricUnitError
            When metric unit is not supported by CloudWatch
        """
        if len(self.metric_set) == 100:
            logger.debug("Exceeded maximum of 100 metrics - Publishing existing metric set")
            metrics = self.serialize_metric_set()
            print(json.dumps(metrics))
            self.metric_set = {}

        if not isinstance(value, numbers.Number):
            raise MetricValueError(f"{value} is not a valid number")

        if not isinstance(unit, MetricUnit):
            try:
                unit = MetricUnit[unit]
            except KeyError:
                unit_options = list(MetricUnit.__members__)
                raise MetricUnitError(f"Invalid metric unit '{unit}', expected either option: {unit_options}")

        metric = {"Unit": unit.value, "Value": float(value)}
        logger.debug(f"Adding metric: {name} with {metric}")
        self.metric_set[name] = metric

    def serialize_metric_set(self, metrics: Dict = None, dimensions: Dict = None) -> Dict:
        """Serializes metric and dimensions set

        Parameters
        ----------
        metrics : Dict, optional
            Dictionary of metrics to serialize, by default None
        dimensions : Dict, optional
            Dictionary of dimensions to serialize, by default None

        Example
        -------
        **Serialize metrics into EMF format**

            metrics = MetricManager()
            # ...add metrics, dimensions, namespace
            ret = metrics.serialize_metric_set()

        Returns
        -------
        Dict
            Serialized metrics following EMF specification

        Raises
        ------
        SchemaValidationError
            Raised when serialization fail schema validation
        """
        if metrics is None:
            metrics = self.metric_set

        if dimensions is None:
            dimensions = self.dimension_set

        logger.debug("Serializing...", {"metrics": metrics, "dimensions": dimensions})

        dimension_keys: List[str] = list(dimensions.keys())
        metric_names_unit: List[Dict[str, str]] = []
        metric_set: Dict[str, str] = {}

        for metric_name in metrics:
            metric: str = metrics[metric_name]
            metric_value: int = metric.get("Value", 0)
            metric_unit: str = metric.get("Unit")

            if metric_value > 0 and metric_unit is not None:
                metric_names_unit.append({"Name": metric_name, "Unit": metric["Unit"]})
                metric_set.update({metric_name: metric["Value"]})

        metrics_definition = {
            "CloudWatchMetrics": [
                {"Namespace": self.namespace, "Dimensions": [dimension_keys], "Metrics": metric_names_unit}
            ]
        }
        metrics_timestamp = {"Timestamp": int(datetime.datetime.now().timestamp() * 1000)}
        metric_set["_aws"] = {**metrics_timestamp, **metrics_definition}
        metric_set.update(**dimensions)

        try:
            logger.debug("Validating serialized metrics against CloudWatch EMF schema", metric_set)
            fastjsonschema.validate(definition=CLOUDWATCH_EMF_SCHEMA, data=metric_set)
        except fastjsonschema.JsonSchemaException as e:
            message = f"Invalid format. Error: {e.message}, Invalid item: {e.name}"  # noqa: B306, E501
            raise SchemaValidationError(message)
        return metric_set

    def add_dimension(self, name: str, value: str):
        """Adds given dimension to all metrics

        Example
        -------
        **Add a metric dimensions**

            metric.add_dimension(name="operation", value="confirm_booking")

        Parameters
        ----------
        name : str
            Dimension name
        value : str
            Dimension value
        """
        logger.debug(f"Adding dimension: {name}:{value}")
        self.dimension_set[name] = value
