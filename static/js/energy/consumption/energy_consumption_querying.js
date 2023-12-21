$(document).ready(function () {
    let get_data_button = $('#get_data_button');
    // order of handlers is important here
    get_data_button.on(
        'click',
        check_control_form_required_fields_are_filled
    )
    get_data_button.on(
        'click', validate_hours_filters_if_one_hour_aggregation_interval_is_chosen
    )
    get_data_button.on(
        'click',
        get_consumption_data_and_update
    );
})

function get_consumption_data_and_update() {
    $.ajax({
        url: reverse_url('get-aggregated-consumption-for-facility'),
        type: 'POST',
        dataType: 'json',
        data: __compose_aggregation_query_parameters(),
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        success: (data) => {
            if (data === null) {
                add_error_alert('За заданими фільтрами дані відсутні');
                return;
            }
            LATEST_RECEIVED_DATA = data;
            draw_content(data);
        },
        error: (error) => {
            if (error.message) {
                add_error_alert(error.message);
                return
            }
            add_error_alert(DEFAULT_UNEXPECTED_ERROR_MESSAGE);
        }
    });
}


function __compose_aggregation_query_parameters() {
    let _ = get_selected_option_for_select;
    let facility = _(__get_facility_select());
    let aggregation_interval_seconds = _(__get_aggregation_interval_select());
    let period_start_epoch_seconds = __get_period_start_epoch_seconds();
    let period_end_epoch_seconds = __get_period_end_epoch_seconds();
    let role = _(__get_role_select());
    let base_params = {
        role: role,
        facility: facility,
        period_start_epoch_seconds: period_start_epoch_seconds,
        period_end_epoch_seconds: period_end_epoch_seconds,
        aggregation_interval_seconds: aggregation_interval_seconds
    };
    if (INCLUDE_HOURS_FILTER) {
        base_params.hours_filtering_start_hour = _(__get_hours_filtering_start_select());
        base_params.hours_filtering_end_hour = _(__get_hours_filtering_end_select());
    }
    return base_params;
}

function __get_aggregated_consumption_data_div() {
    return $('#energy_content');
}

function __get_period_start_epoch_seconds() {
    return __get_data_input_epoch_value_seconds_by_id('#period_start');
}

function __get_data_input_epoch_value_seconds_by_id(id) {
    // converting to seconds from milliseconds
    return Date.parse($(`${id}`).val()) / 1000;
}

function __get_period_end_epoch_seconds() {
    return __get_data_input_epoch_value_seconds_by_id('#period_end');
}

function __get_aggregation_interval_select() {
    return $('#id_aggregation_interval_seconds');
}

function __get_role_select() {
    return $('#id_role');
}