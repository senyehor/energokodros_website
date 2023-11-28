$(document).ready(function () {
    style_and_setup_selects();
})

function style_and_setup_selects() {
    // disabled is included in django field to ignore possible input
    // but user can move to facility or role page by clicking a descendant
    remove_disabled_set_width_100(__get_descendants_select());
    remove_disabled_set_width_100(__get_roles_for_facility_select());

    add_descendants_select_on_click_label();
    add_roles_on_click_label();

    __get_descendants_select().change(
        redirect_from_selected_option_and_clear_selected_on_click('edit-facility-pk-in-post')
    );
    __get_roles_for_facility_select().change(
        redirect_from_selected_option_and_clear_selected_on_click('edit-user-role-pk-in-post')
    );
}


function add_descendants_select_on_click_label() {
    add_muted_text_after_div_label(
        __get_descendants_div(),
        'При натисканні на об‘єкт вас перенаправить на його сторінку'
    );
}

function add_roles_on_click_label() {
    add_muted_text_after_div_label(
        __get_roles_for_facility_select_div(),
        'При натисканні на роль вас перенаправить на її сторінку'
    );
}

function __get_descendants_div() {
    return $('#div_id_descendants');
}


function __get_descendants_select() {
    return $('#id_descendants')
}

function __get_roles_for_facility_select_div() {
    return $('#div_id_roles_that_have_access_to_this_facility');
}

function __get_roles_for_facility_select() {
    return $('#id_roles_that_have_access_to_this_facility');
}
