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
    get_data_button.on(
        'click',
        clear_alerts
    )
})

function get_consumption_data_and_update() {
    $.ajax({
        url: reverse_url('get-aggregated-consumption-for-facility'),
        type: 'POST',
        dataType: 'json',
        data: __compose_aggregation_query_parameters(),
        headers: get_headers_for_ajax_object(),
        success: (data) => {
            if (data === null) {
                add_warning_alert('За заданими фільтрами дані відсутні');
                return;
            }
            LATEST_RECEIVED_DATA = data;
            draw_content(data);
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


function __compose_aggregation_query_parameters() {
    let _ = get_selected_option_for_select;
    let facility_pk = _(__get_facility_select());
    let aggregation_interval_seconds = _(__get_aggregation_interval_select());
    let period_start_epoch_seconds = __get_period_start_epoch_seconds();
    let period_end_epoch_seconds = __get_period_end_epoch_seconds();
    let role_pk = _(__get_role_select());
    let include_forecast = __get_forecast_checkbox_value();
    let base_parameters = {
        role_pk: role_pk,
        facility_pk: facility_pk,
        period_start_epoch_seconds: period_start_epoch_seconds,
        period_end_epoch_seconds: period_end_epoch_seconds,
        aggregation_interval_seconds: aggregation_interval_seconds,
        include_forecast: include_forecast
    };
    if (INCLUDE_HOURS_FILTER) {
        base_parameters.hours_filtering_start_hour = _(__get_hours_filtering_start_select());
        base_parameters.hours_filtering_end_hour = _(__get_hours_filtering_end_select());
    }
    return base_parameters;
}

function __get_aggregated_consumption_data_div() {
    return $('#energy_content');
}

function __get_period_start_epoch_seconds() {
    return __get_data_input_epoch_value_seconds_by_id(__get_period_start_input());
}

function __get_data_input_epoch_value_seconds_by_id(date_input) {
    // converting to seconds from milliseconds
    return Date.parse(date_input.val()) / 1000;
}

function __get_period_end_epoch_seconds() {
    return __get_data_input_epoch_value_seconds_by_id(__get_period_end_input());
}

function __get_aggregation_interval_select() {
    return $('#id_aggregation_interval_seconds');
}

function __get_role_select() {
    return $('#id_role');
}