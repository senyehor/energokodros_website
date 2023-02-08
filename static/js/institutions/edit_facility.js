$(document).ready(function () {
    style_and_setup_selects();
})

function style_and_setup_selects() {
    // disabled is included in django field to ignore possible input
    // but user can move to facility or role page by clicking a descendant
    __get_descendants_select().removeAttr('disabled');
    __get_roles_for_facility_select().removeAttr('disabled');

    add_descendants_select_on_click_label();
    add_roles_on_click_label();

    __get_descendants_select().change(
        redirect_to_selected_object('edit-facility-pk-in-post')
    );
    __get_roles_for_facility_select().change(
        redirect_to_selected_object('edit-user-role-pk-in-post')
    );
}


function add_descendants_select_on_click_label() {
    add_muted_text_after_div_label(
        __get_descendants_div(),
        ON_CLICK_REDIRECTS_TEXT
    );
}

function add_roles_on_click_label() {
    add_muted_text_after_div_label(
        __get_roles_for_facility_select_div(),
        ON_CLICK_REDIRECTS_TEXT
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
