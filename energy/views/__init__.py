from .aggregated_consumption_view import ConsumptionPageView, get_consumption_with_total_consumption
from .box_with_sensors_creation import BoxWithSensorsCreateView
from .energy_report import get_energy_report
from .generic import (
    BoxEditDeleteView, BoxListView, BoxSensorSetEditDeleteView, BoxSensorSetListView,
    SensorEditDeleteView,
    SensorListView,
)
from .simple import (
    get_aggregation_status_and_last_time_run,
    run_aggregation,
)
