$(document).ready(function () {
    __get_run_aggregation_button().click(send_start_aggregation_request);
    __get_run_aggregation_button().click(clear_alerts);
    update_aggregation_status_and_last_time_run();
})

const FAILED_TO_RETRIEVE_DATA = 'не вдалося отримати дані';
const IDLE = 'idle', RUNNING = 'running';


function send_start_aggregation_request() {
    _set_run_aggregation_button_loading();
    $.ajax({
        url: reverse_url('run-aggregation'),
        type: 'POST',
        dataType: 'json',
        headers: get_headers_for_ajax_object(),
        success: (response) => {
            _set_run_aggregation_button_active();
            add_success_alert('Агрегацію було успішно запущено');
        },
        error: (response) => {
            _set_run_aggregation_button_active();
            add_error_alert('Виникла помилка при запуску агрегації');
        }
    });
}

function update_aggregation_status_and_last_time_run() {
    $.ajax({
        url: reverse_url('get-aggregation-status-and-last-time-run'),
        type: 'POST',
        dataType: 'json',
        headers: get_headers_for_ajax_object(),
        success: (response) => {
            _set_run_aggregation_button_active();
            set_aggregation_last_time_run(response.aggregation_last_rime_run);
            set_aggregation_status_adjust_start_aggregation_button_accordingly(
                response.aggregation_status
            );
        },
        error: (response) => {
            _set_run_aggregation_button_active();
            set_aggregation_last_time_run(null)
            set_aggregation_status_adjust_start_aggregation_button_accordingly(null)
        }
    });
}

function set_aggregation_status_adjust_start_aggregation_button_accordingly(aggregation_status) {
    if (aggregation_status === IDLE) {
        __get_aggregation_status_p().text('не активна')
        _set_start_aggregation_button_active();
    } else if (aggregation_status === RUNNING) {
        __get_aggregation_status_p().text('активна')
        _set_start_aggregation_button_disabled();
    } else {
        throw 'wrong aggregation status'
    }
}

function set_aggregation_last_time_run(value) {
    let display_value = value ? value : FAILED_TO_RETRIEVE_DATA
    __get_aggregation_last_time_run_p().text(display_value)
}

function _set_run_aggregation_button_active() {
    __get_start_aggregation_button_spinner_span().addClass('d-none');
    __get_start_aggregation_button_text_span().removeClass('d-none');
}

function _set_run_aggregation_button_loading() {
    __get_start_aggregation_button_text_span().addClass('d-none');
    __get_start_aggregation_button_spinner_span().removeClass('d-none');
}


function _set_start_aggregation_button_disabled() {
    __get_run_aggregation_button().removeClass('btn-primary');
    __get_run_aggregation_button().addClass('btn-secondary');
}

function _set_start_aggregation_button_active() {
    __get_run_aggregation_button().removeClass('btn-secondary');
    __get_run_aggregation_button().addClass('btn-primary');
}

function __get_start_aggregation_button_text_span() {
    return $('#run_aggregation_button_text')
}

function __get_start_aggregation_button_spinner_span() {
    return $('#start_aggregation_request_processing_spinner')
}

function __get_aggregation_last_time_run_p() {
    return $('#aggregation_last_time_run_id')
}

function __get_aggregation_status_p() {
    return $('#aggregation_status_id')
}

function __get_run_aggregation_button() {
    return $('#run_aggregation_button')
}