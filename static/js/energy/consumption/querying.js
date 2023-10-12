$(document).ready(function () {
    let get_data_button = $('#get_data_button');
    get_data_button.on('click', on_get_data_button_click);
})

const NO_DATA_FOR_PARAMETERS_MESSAGE = 'За заданими фільтрами дані відсутні';

function on_get_data_button_click() {
    clear_alerts();
    validate_hours_filters_if_one_hour_aggregation_interval_is_chosen();
    get_consumption_data_and_update();
}


function get_consumption_data_and_update() {
    $.ajax({
        url: reverse_url('get-aggregated-consumption-for-facility'),
        type: 'POST',
        dataType: 'json',
        data: __compose_aggregation_query_parameters(),
        headers: get_headers_for_ajax_object(),
        success: (response) => {
            process_consumption_data_response(response);
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

function process_consumption_data_response(response) {
    CONSUMPTION_WITH_OPTIONAL_FORECAST = response.consumption_with_optional_forecast;
    if (CONSUMPTION_WITH_OPTIONAL_FORECAST === null) {
        add_warning_alert(NO_DATA_FOR_PARAMETERS_MESSAGE);
        return;
    }
    TOTAL_CONSUMPTION = response.total_consumption;
    let metadata = response.metadata;
    LABEL_INDEX_IN_RAW_DATA = metadata.indexes.label_index;
    CONSUMPTION_INDEX_IN_RAW_DATA = metadata.indexes.value_index;
    FORECAST_INCLUDED = metadata.forecast_included === 'true';
    if (FORECAST_INCLUDED) {
        CONSUMPTION_FORECAST_INDEX_IN_RAW_DATA = metadata.indexes.forecast_index;
    }
    draw_content();
}

function __compose_aggregation_query_parameters() {
    let _ = get_selected_option_for_select;
    let facility_pk = _(__get_facility_select());
    let aggregation_interval_seconds = _(__get_aggregation_interval_select());
    let period_start_epoch_seconds_utc = get_period_start_time_epoch_seconds_utc();
    let period_end_epoch_seconds_utc = get_period_end_time_epoch_seconds_utc();
    let role_pk = _(__get_role_select());
    let include_forecast = __get_forecast_checkbox_value();
    let base_parameters = {
        role_pk: role_pk,
        facility_pk: facility_pk,
        period_start_epoch_seconds_utc: period_start_epoch_seconds_utc,
        period_end_epoch_seconds_utc: period_end_epoch_seconds_utc,
        aggregation_interval_seconds: aggregation_interval_seconds,
        include_forecast: include_forecast
    };
    if (INCLUDE_HOURS_FILTER) {
        base_parameters.hour_filtering_start_hour = _(get_hour_filters_select(START));
        base_parameters.hour_filtering_end_hour = _(get_hour_filters_select(END));
        base_parameters.hour_filtering_method = CHOSEN_HOUR_FILTERING_METHOD;
    }
    return base_parameters;
}

function __get_aggregated_consumption_data_div() {
    return $('#energy_content');
}

function __get_role_select() {
    return $('#id_role');
}