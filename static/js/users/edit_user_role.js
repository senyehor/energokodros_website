$(document).ready(function () {
    style_selects();

    __get_facility_role_has_access_to_select().click(
        redirect_to_selected_object(
            'edit-facility-pk-in-post'
        )
    );
    __get_user_role_owner_select().click(
        redirect_to_selected_object(
            'edit-user-pk-in-post'
        )
    )
})

function style_selects() {
    __get_user_role_owner_select().removeAttr('disabled');
    __get_facility_role_has_access_to_select().removeAttr('disabled');
    // removing arrows as select is used to provide id to redirect on click
    __get_user_role_owner_select().css('appearance', 'none');
    __get_facility_role_has_access_to_select().css('appearance', 'none');

    add_on_click_redirects_text_after_div_first_label(__get_user_role_owner_div());
    add_on_click_redirects_text_after_div_first_label(__get_facility_role_has_access_to_div());
}


function __get_user_role_owner_select() {
    return $('#id_user_info');
}

function __get_user_role_owner_div() {
    return $('#div_id_user_info');
}

function __get_facility_role_has_access_to_select() {
    return $('#id_facility_has_access_to_info');
}

function __get_facility_role_has_access_to_div() {
    return $('#div_id_facility_has_access_to_info');
}