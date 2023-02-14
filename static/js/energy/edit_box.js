$(document).ready(() => {
    add_on_click_redirects_texts();
    add_redirect_on_click_to_related_objects();
    remove_disabled_from_related_objects_selects();
})

function add_on_click_redirects_texts() {
    add_on_click_redirects_text_after_div_first_label(__get_sensor_sets_div());
}

function add_redirect_on_click_to_related_objects() {
    __get_sensor_sets_select().change(
        redirect_to_selected_object('edit-box-sensor-set-pk-in-post')
    );
}

function remove_disabled_from_related_objects_selects() {
    __get_sensor_sets_select().removeAttr('disabled');
}

function __get_sensor_sets_select() {
    return $('#id_sensor_sets');
}

function __get_sensor_sets_div() {
    return $('#div_id_sensor_sets');
}