$(document).ready(() => {
    __get_download_report_button().click(download_report);
    __get_download_report_button().click(clear_alerts);
})


function download_report() {
    $.ajax({
        url: reverse_url('get-energy-report'),
        type: 'POST',
        xhrFields: {
            responseType: 'blob'
        },
        data: __compose_aggregation_query_parameters(),
        headers: get_headers_for_ajax_object(),
        success: (data) => {
            let a = document.createElement('a');
            let url = window.URL.createObjectURL(data);
            a.href = url;
            a.download = 'energy_report.docx';
            document.body.append(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        },
        error: (error) => {
            if (error.responseJSON) {
                add_warning_alert(error.responseJSON);
                return
            }
            add_error_alert(DEFAULT_UNEXPECTED_ERROR_MESSAGE);
        }
    });
}

function __get_download_report_button() {
    return $('#download_report_button');
}