$(document).ready(() => {
    add_redirect_to_related_sensor_on_click();
    remove_disabled_from_related_objects_select();
    add_on_click_redirect_to_related_object_text();
    add_redirect_to_related_facility();
})

function add_redirect_to_related_facility() {
    let facility_label = $('label[for="id_facility"]');
    facility_label.append("| <a id='go_to_facility' class='link-primary'>Перейти до об'єкту</a>");
    $('#go_to_facility').click(
        redirect_to_selected_object_with_get_id_callback(
            'edit-facility-pk-in-post',
            () => {
                return get_selected_option_for_select(__get_related_facility_select());
            }
        )
    );
}

function add_redirect_to_related_sensor_on_click() {
    __get_related_sensor_select().click(
        redirect_to_selected_object('edit-sensor-pk-in-post')
    )
}

function remove_disabled_from_related_objects_select() {
    __get_related_sensor_select().removeAttr('disabled');
}

function add_on_click_redirect_to_related_object_text() {
    add_on_click_redirects_text_after_div_first_label(__get_related_sensor_select_div())
}

function __get_related_sensor_select_div() {
    return $('#div_id_sensor_number')
}

function __get_related_sensor_select() {
    return $('#id_sensor_number')
}

function __get_related_facility_select() {
    return $('#id_facility')
}