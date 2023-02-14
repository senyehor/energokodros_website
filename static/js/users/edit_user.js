$(document).ready(function () {
    style_roles_select();
    add_redirect_on_roles_click();
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

function __get_roles_select() {
    return $('#id_roles');
}