function update_facility_choices_for_chosen_institution_callback(
    institution_select_func,
    update_with_ids_and_labels_callback
) {
    return () => {
        $.ajax({
            url: reverse_url('get-institution-facilities'),
            type: 'POST',
            dataType: 'json',
            headers: get_headers_for_ajax_object(),
            data: {
                institution_id: __get_selected_institution_id(institution_select_func)
            },
            success: (ids_and_labels) => {
                update_with_ids_and_labels_callback(ids_and_labels);
            },
            error: (error) => {
                add_error_alert(DEFAULT_UNEXPECTED_ERROR_MESSAGE);
            }
        });
    }
}

function __get_selected_institution_id(institution_select_func) {
    return get_selected_option_for_select(institution_select_func());
}