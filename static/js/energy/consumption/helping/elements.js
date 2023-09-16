function __get_interval_filtering_div() {
    return $('#interval_filtering_div_id');
}

function get_hour_or_day_or_week_period_input(start_or_end) {
    return $(`#hour_or_day_or_week_period_${start_or_end}_id`)
}

function get_hour_filters_select(start_or_end) {
    return $(`#id_hour_filter_${start_or_end}`)
}


function __get_aggregation_interval_select() {
    return $('#id_aggregation_interval_seconds');
}

function __get_month_select(start_or_end) {
    return __get_year_or_month_select(ONE_MONTH_IN_SECONDS, start_or_end);
}

function __get_year_select(start_or_end) {
    return __get_year_or_month_select(ONE_YEAR_IN_SECONDS, start_or_end)
}

function __get_year_or_month_select(year_or_month_interval, start_or_end) {
    let interval_name = INTERVAL_TO_INTERVAL_NAME.get(year_or_month_interval);
    return $(`#${interval_name}_select_${start_or_end}_id`);
}