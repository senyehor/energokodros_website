from energy.forms import BoxFormNoRelationFields, BoxSensorSetFormset, SensorsFormset


class STEPS:
    BOX = 'box'
    SENSORS = 'sensors'
    BOX_SENSORS_SET = 'box_sensor_set'


FORMS = (
    (STEPS.BOX, BoxFormNoRelationFields),
    # default sensors count is max but can be adjusted by user
    (STEPS.SENSORS, SensorsFormset),
    # box_sensors_set should be created dynamically depending on sensor count from previous step
    (STEPS.BOX_SENSORS_SET, BoxSensorSetFormset)
)

BOX_WITH_SENSORS_CREATION_TEMPLATES = {
    STEPS.BOX:             'energy/box_with_sensors/box.html',
    STEPS.SENSORS:         'energy/box_with_sensors/sensors.html',
    STEPS.BOX_SENSORS_SET: 'energy/box_with_sensors/box_sensors_set.html',
}

FORMS_ORDER_FROM_ZERO = {
    STEPS.BOX:             0,
    STEPS.SENSORS:         1,
    STEPS.BOX_SENSORS_SET: 2
}
