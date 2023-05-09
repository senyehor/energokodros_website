$(document).ready(function () {
    __get_run_aggregation_button().click(send_start_aggregation_request);
})

function send_start_aggregation_request() {
    $.ajax({
        url: reverse_url('run-aggregation'),
        type: 'POST',
        dataType: 'json',
        headers: get_headers_for_ajax_object(),
        success: (response) => {
            add_success_alert('Агрегацію було успішно запущено');
        },
        error: (response) => {
            add_error_alert('Виникла помилка при запуску агрегації');
        }
    });
}


function __get_run_aggregation_button() {
    return $('#run_aggregation_button')
}