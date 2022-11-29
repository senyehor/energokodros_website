$(document).ready(function () {
    style_selects();

    __get_facility_role_has_access_to_select().click(
        redirect_from_selected_option_and_clear_selected_on_click(
            'edit-facility-pk-in-post'
        )
    );
    __get_user_role_owner_select().click(
        redirect_from_selected_option_and_clear_selected_on_click(
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

    add_muted_text_after_div_label(
        __get_user_role_owner_div(),
        ON_CLICK_REDIRECTS_TEXT
    );
    add_muted_text_after_div_label(
        __get_facility_role_has_access_to_div(),
        ON_CLICK_REDIRECTS_TEXT
    );
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