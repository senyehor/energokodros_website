$(document).ready(function () {
    style_roles_select();
})

function style_roles_select() {
    remove_disable_set_width_100(__get_roles_select());
}

function __get_roles_select() {
    return $('#id_roles');
}