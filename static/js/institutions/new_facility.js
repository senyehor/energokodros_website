$(document).ready(function () {
    set_width_for_all_selects();
    update_parent_facility_select();
    __get_institution_select().change(update_parent_facility_select);
})

function update_parent_facility_select() {
    $.ajax({
        url: reverse_url('get-institution-facilities'),
        type: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        data: {
            institution_id: __get_selected_institution_id()
        },
        success: (ids_and_labels) => {
            update_select_with_options(__get_parent_facility_select(), ids_and_labels);
        },
        error: (error) => {
            add_error_alert(DEFAULT_UNEXPECTED_ERROR_MESSAGE);
        }
    });
}

function set_width_for_all_selects() {
    __get_parent_facility_select().addClass('w-100');
    __get_institution_select().addClass('w-100');
}

function __get_selected_institution_id() {
    return get_selected_option_for_select(__get_institution_select());
}

function __get_institution_select() {
    return $('#id_institution');
}

function __get_parent_facility_select() {
    return $('#id_parent_facility');
}