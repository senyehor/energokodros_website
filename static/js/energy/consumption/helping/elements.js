function __get_interval_filtering_div() {
    return $('#interval_filtering_div_id');
}

function get_hour_or_day_period_input(start_or_end) {
    return $(`#hour_or_day_period_${start_or_end}_id`)
}

function get_hour_filters_select(start_or_end) {
    return $(`#id_hour_filter_${start_or_end}`)
}


function __get_aggregation_interval_select() {
    return $('#id_aggregation_interval_seconds');
}

function __get_year_select(start_or_end) {
    return $(`#${INTERVAL_TO_INTERVAL_NAME.get(ONE_YEAR_IN_SECONDS)}_select_${start_or_end}_id`);
}

function __get_month_select(start_or_end) {
    return $(`#${INTERVAL_TO_INTERVAL_NAME.get(ONE_MONTH_IN_SECONDS)}_${start_or_end}_id`);
}