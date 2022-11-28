$(document).ready(function () {
    style_roles_select();
    __get_roles_select().change(
        redirect_from_selected_option_and_clear_selected_on_click('edit-user-role-pk-in-post')
    );
})

function style_roles_select() {
    remove_disabled_set_width_100(__get_roles_select());
}

function __get_roles_select() {
    return $('#id_roles');
}