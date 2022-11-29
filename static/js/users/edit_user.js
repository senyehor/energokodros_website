$(document).ready(function () {
    style_roles_select();
    __get_roles_select().change(
        redirect_from_selected_option_and_clear_selected_on_click(
            'edit-user-role-pk-in-post'
        )
    );
})

function style_roles_select() {
    __get_roles_select().removeAttr('disabled');
}

function __get_roles_select() {
    return $('#id_roles');
}