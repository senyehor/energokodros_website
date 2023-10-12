function get_selected_option_for_select(select) {
    return select.find('option:selected').val();
}

function reverse_url(url_name) {
    return $(`#${url_name}`).text();
}

function update_select_with_options(select, options) {
    select.empty();
    for (const id_label_object_index in (options)) {
        let hashed_id = options[id_label_object_index][0];
        let label = options[id_label_object_index][1];
        select.append(
            `<option value="${hashed_id}">${label}</option>`
        )
    }
}