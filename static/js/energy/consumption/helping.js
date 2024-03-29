$(document).ready(function () {
    update_facilities_list_for_role();
    __get_roles_select().change(update_facilities_list_for_role);
    add_hour_filtering_filter_day_or_interval_buttons();
})

let INCLUDE_HOURS_FILTER = false;

let FILTER_EVERY_DAY_VALUE = 'filter-every-day', FILTER_WHOLE_INTERVAL_VALUE = 'filter-whole-interval';
let CHOSEN_HOUR_FILTERING_METHOD = FILTER_EVERY_DAY_VALUE;
let FILTER_EVERY_DAY_BUTTON = null, FILTER_WHOLE_INTERVAL_BUTTON = null;

function update_facilities_list_for_role() {
    $.ajax({
        url: reverse_url('get-facilities-list-for-role'),
        type: 'POST',
        dataType: 'json',
        data: {
            role_id: __get_selected_role_id()
        },
        headers: get_headers_for_ajax_object(),
        success: (ids_and_labels) => {
            update_select_with_options(__get_facility_select(), ids_and_labels);
        },
        error: (error) => {
            let message = DEFAULT_UNEXPECTED_ERROR_MESSAGE;
            if (error.message) {
                message = error.message
            }
            add_error_alert(message);
        }
    });
}

function validate_hours_filters_if_one_hour_aggregation_interval_is_chosen() {
    INCLUDE_HOURS_FILTER = false;
    if (CURRENT_INTERVAL_CHOSEN !== ONE_HOUR_IN_SECONDS) {
        return;
    }
    let start_value = get_selected_option_for_select(get_hour_filters_select(START));
    let end_value = get_selected_option_for_select(get_hour_filters_select(END));
    // default values cover everything, so there is no point to pass them
    if (
        start_value === DEFAULT_START_HOUR_FILTER_OPTION
        && end_value === DEFAULT_END_HOUR_FILTER_OPTION
    ) {
        return
    }
    INCLUDE_HOURS_FILTER = true;
}


function add_hour_filtering_filter_day_or_interval_buttons() {
    FILTER_EVERY_DAY_BUTTON = $('#filter_every_day_button_id');
    FILTER_WHOLE_INTERVAL_BUTTON = $('#filter_whole_interval_button_id');
    FILTER_EVERY_DAY_BUTTON.click(() => {
        __set_button_to_chosen(FILTER_EVERY_DAY_BUTTON);
        CHOSEN_HOUR_FILTERING_METHOD = FILTER_EVERY_DAY_VALUE;
        __set_button_to_can_be_chosen(FILTER_WHOLE_INTERVAL_BUTTON);
    });
    FILTER_WHOLE_INTERVAL_BUTTON.click(() => {
        __set_button_to_chosen(FILTER_WHOLE_INTERVAL_BUTTON);
        CHOSEN_HOUR_FILTERING_METHOD = FILTER_WHOLE_INTERVAL_VALUE;
        __set_button_to_can_be_chosen(FILTER_EVERY_DAY_BUTTON);
    })
}

function _get_current_date_for_date_input() {
    let now = new Date();
    let month = String(now.getMonth() + 1).padStart(2, '0');
    let day = String(now.getDate()).padStart(2, '0');
    return now.getFullYear() + '-' + month + '-' + day;
}

function __get_facility_select() {
    return $('#id_facility_to_get_consumption_for');
}

function __get_selected_role_id() {
    return get_selected_option_for_select(__get_roles_select());
}

function __get_roles_select() {
    return $('#id_role');
}


function __get_set_view_mode_to_table_button() {
    return $('#set_table_button')
}

function __get_set_view_mode_to_chart_button() {
    return $('#set_chart_button')
}

function __get_include_forecast_checkbox() {
    return $('#id_include_forecast');
}

function __get_forecast_checkbox_value() {
    return __get_include_forecast_checkbox().is(':checked');
}