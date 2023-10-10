$(document).ready(function () {
    set_form_to_be_submitted_on_sensors_count_change();
})


function set_form_to_be_submitted_on_sensors_count_change() {
    __get_sensor_count_select().change(function () {
        add_input_to_indicate_that_sensor_count_was_changed();
        __get_sensors_form().submit();
    });
}

function add_input_to_indicate_that_sensor_count_was_changed() {
    __get_sensors_form().append($('<input type="hidden" name="sensor_count_changed" value="true">'));
}

function __get_sensor_count_select() {
    return $('#id_sensor_count');
}

function __get_sensors_form() {
    return $('#sensors_form');
}