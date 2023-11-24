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

function remove_disable_set_width_100(elem) {
    elem.removeAttr('disabled');
    elem.addClass('w-100');
}

function generate_muted_p(text) {
    return '<p class="fw-light text-muted">' +
        `${text}` +
        '</p>'
}

function add_success_alert(message) {
    __get_alerts_container_create_if_not_exists().append(__create_alert_div('success', message));
}

function add_error_alert(message) {
    __get_alerts_container_create_if_not_exists().append(__create_alert_div('danger', message));
}

function __create_alert_div(level, message) {
    return '' +
        `<div class="alert alert-${level} alert-dismissible fade show" role="alert">` +
        `${message}` +
        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">' +
        '</button>' +
        '</div>'
}

function __get_alerts_container_create_if_not_exists() {
    if (!$('#alerts').length) {
        $('header:first').after('' +
            '<div class="container">' +
            '   <div id="alerts">' +
            '   </div>' +
            '</div>');
    }
    return $("#alerts");
}