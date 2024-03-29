function get_selected_option_for_select(select) {
    return select.find('option:selected').val();
}

function get_int_selected_option_for_select(select) {
    return parseInt(get_selected_option_for_select(select))
}

function reverse_url(url_name) {
    // url name should be included in d-none block with id same as url name
    let url = $(`#${url_name}`).text();
    if (url) {
        return url;
    }
    throw new Error('url not found')
}

function update_select_with_options(select, options) {
    select.empty();
    let options_html = '';
    for (const id_label_object_index in (options)) {
        let value = options[id_label_object_index][0];
        let label = options[id_label_object_index][1];
        options_html += `<option value="${value}">${label}</option>`;
    }
    select.append(options_html);
}

function get_headers_for_ajax_object() {
    return {
        'X-CSRFToken': $.cookie('csrftoken')
    }
}

function add_on_click_redirects_text_after_div_first_label(div) {
    __add_muted_text_after_div_label(div, ON_CLICK_REDIRECTS_TEXT)
}

function __add_muted_text_after_div_label(div, text) {
    div.find('label').after(__generate_muted_p(text));
}

function clear_alerts() {
    __get_alerts_container().empty();
}

function __generate_muted_p(text) {
    return '<p class="fw-light text-muted m-0">' +
        `${text}` +
        '</p>'
}

function add_success_alert(message) {
    __get_alerts_container_create_if_not_exists().append(__create_alert_div('success', message));
}

function add_error_alert(message) {
    __get_alerts_container_create_if_not_exists().append(__create_alert_div('danger', message));
}

function add_warning_alert(message) {
    __get_alerts_container_create_if_not_exists().append(__create_alert_div('warning', message));
}


function get_current_url() {
    return new URL(window.location.href);
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
    if (!__get_alerts_container().length) {
        $('header:first').after('' +
            '<div class="container">' +
            '   <div id="alerts">' +
            '   </div>' +
            '</div>');
    }
    return __get_alerts_container();
}

function __get_alerts_container() {
    return $("#alerts")
}

const DEFAULT_UNEXPECTED_ERROR_MESSAGE = '' +
    'Сталася непередбачена помилка, ' +
    'якщо після перезавантаження сторінки проблема не зникне, ' +
    'зверніться до адміністратора.'

const ON_CLICK_REDIRECTS_TEXT = 'При натисканні вас перенаправить на сторінку'

function redirect_to_object(url_name, id) {
    $.ajax({
        url: reverse_url(url_name),
        type: 'POST',
        dataType: 'json',
        headers: get_headers_for_ajax_object(),
        data: {id: id},
        success: (data) => {
            window.open(data.url, '_self');
        },
        error: (data) => {
            add_error_alert(DEFAULT_UNEXPECTED_ERROR_MESSAGE);
        }
    });
}

function redirect_to_selected_object(url_name) {
    return function () {
        let select = $(this);
        let id = get_selected_option_for_select(select);
        redirect_to_object(url_name, id);
    }
}

function redirect_to_selected_object_with_get_id_callback(url_name, get_id_callback) {
    return function () {
        let id = get_id_callback();
        redirect_to_object(url_name, id);
    }
}