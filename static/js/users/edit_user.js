$(document).ready(function () {
    style_roles_select();
    add_redirect_on_roles_click();
    add_on_click_redirects_text_after_div_first_label(__get_roles_select_div());
})

function add_redirect_on_roles_click() {
    __get_roles_select().change(
        redirect_to_selected_object(
            'edit-user-role-pk-in-post'
        )
    );
}

function style_roles_select() {
    __get_roles_select().removeAttr('disabled');
}

function __get_roles_select_div() {
    return $('#div_id_roles');
}

function __get_roles_select() {
    return $('#id_roles');
}