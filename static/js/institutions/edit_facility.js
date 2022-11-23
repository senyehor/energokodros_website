$(document).ready(function () {
    style_and_setup_descendants_select();
})

function style_and_setup_descendants_select() {
    // disabled is included in django field to ignore possible input
    // but user can move to facility page by clicking a descendant
    __get_descendants_select().removeAttr('disabled');
    __get_descendants_select().addClass('w-100');
}


function __get_descendants_select() {
    return $('#id_descendants')
}
