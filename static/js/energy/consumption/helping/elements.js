function __get_interval_filtering_div() {
    return $('#interval_filtering_div_id');
}

function get_hour_or_day_period_input(start_or_end) {
    return $(`#hour_or_day_period_${start_or_end}`)
}