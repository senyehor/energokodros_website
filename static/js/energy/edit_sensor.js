$(document).ready(() => {
    add_on_click_redirects_texts();
    add_redirect_on_click_to_related_objects();
    remove_disabled_from_related_objects_selects();
})

function add_on_click_redirects_texts() {
    add_on_click_redirects_text_after_div_first_label(__get_box_div());
    add_on_click_redirects_text_after_div_first_label(__get_set_div());
}

function add_redirect_on_click_to_related_objects() {
    __get_box_select().click(
        redirect_to_selected_object('edit-box-pk-in-post')
    );
    __get_set_select().click(
        redirect_to_selected_object('edit-box-sensor-set-pk-in-post')
    );
}

function remove_disabled_from_related_objects_selects() {
    __get_box_select().removeAttr('disabled');
    __get_set_select().removeAttr('disabled');
}

function __get_box_select() {
    return $('#id_box')
}

function __get_set_select() {
    return $('#id_set')
}

function __get_box_div() {
    return $('#div_id_box');
}

function __get_set_div() {
    return $('#div_id_set');
}