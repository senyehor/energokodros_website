$(document).ready(() => {
    __get_download_report_button().click(download_report);
    __get_download_report_button().click(clear_alerts);
})


function download_report() {
    $.ajax({
        url: reverse_url('get-energy-report'),
        type: 'POST',
        xhr: () => {
            let xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 2) {
                    if (xhr.status === 200) {
                        xhr.responseType = "blob";
                    } else {
                        xhr.responseType = "json";
                    }
                }
            };
            return xhr;
        },
        data: __compose_aggregation_query_parameters(),
        headers: get_headers_for_ajax_object(),
        success: (data) => {
            if (data === null) {
                add_warning_alert(NO_DATA_FOR_PARAMETERS_MESSAGE);
                return;
            }
            let a = document.createElement('a');
            let url = window.URL.createObjectURL(data);
            a.href = url;
            a.download = `${create_report_name()}.docx`;
            document.body.append(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        },
        error: (error) => {
            if (error.responseText) {
                add_warning_alert(error.responseText);
                return
            }
            add_error_alert(DEFAULT_UNEXPECTED_ERROR_MESSAGE);
        }
    });
}

function create_report_name() {
    let now = new Date();
    let day_number = now.getUTCDay();
    let month_number = now.getUTCMonth();
    let year_number = now.getUTCFullYear();
    return `energy_report_${day_number}_${month_number}_${year_number}`
}

function __get_download_report_button() {
    return $('#download_report_button');
}