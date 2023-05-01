from .aggregated_consumption_view import ConsumptionPageView, get_consumption_with_total_consumption
from .box_with_sensors_creation import BoxWithSensorsCreateView
from .generic import (
    BoxEditDeleteView, BoxListView, BoxSensorSetEditDeleteView, BoxSensorSetListView,
    SensorEditDeleteView,
    SensorListView,
)
from .simple import get_facilities_choices_for_role, run_aggregation
