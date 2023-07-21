const FORM_ADDITIONAL_CLASSES_BY_PATH = {
    'login': ['w-25',],
    'registration': ['w-50',]
}

const FORM_CONTAINER_ADDITIONAL_CLASSES_BY_PATH = {
    'login': ['pt-5',],
    'registration': ['pt-1',]
}

$(document).ready(function () {
    add_spacing_between_form_group();
    add_classes_depending_on_page();
})

function add_spacing_between_form_group() {
    $('form > div.form-group').each(
        function () {
            $(this).addClass('pt-3');
        }
    )
}

function add_classes_depending_on_page() {
    let path = get_path();
    let form = $('#form-card');
    let form_container = $('#form-container');
    FORM_ADDITIONAL_CLASSES_BY_PATH[path].forEach(
        cls => form.addClass(cls)
    )
    FORM_CONTAINER_ADDITIONAL_CLASSES_BY_PATH[path].forEach(
        cls => form_container.addClass(cls)
    )
}

function get_path() {
    // filter is used to remove '' strings at the beginning and end
    let path_parts = window.location.pathname.split('/').filter(item => !!item);
    return path_parts.at(-1);
}