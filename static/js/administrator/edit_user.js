$(document).ready(function () {
    style_roles_select();
})

function style_roles_select() {
    __get_roles_select().removeAttr('disabled');
    __get_roles_select().addClass('w-100');
}

function __get_roles_select() {
    return $('#id_roles');
}