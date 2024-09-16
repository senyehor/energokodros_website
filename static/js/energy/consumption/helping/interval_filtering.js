$(document).ready(() => {
    __get_aggregation_interval_select().change(
        on_interval_select_change
    );
    __get_hours_filtering_reset_button().click(set_default_hour_filtering_choices);
    __get_aggregation_interval_select().trigger('change');
})

const ONE_HOUR_IN_SECONDS = 60 * 60,
    ONE_DAY_IN_SECONDS = ONE_HOUR_IN_SECONDS * 24,
    ONE_WEEK_IN_SECONDS = ONE_DAY_IN_SECONDS * 7,
    ONE_MONTH_IN_SECONDS = ONE_WEEK_IN_SECONDS * 4,
    ONE_YEAR_IN_SECONDS = ONE_MONTH_IN_SECONDS * 12;

const DEFAULT_START_HOUR_FILTER_OPTION = '0', DEFAULT_END_HOUR_FILTER_OPTION = '23';

const UNRECOGNIZED_INTERVAL = new Error('Unrecognized interval');

let CURRENT_INTERVAL_CHOSEN = null;

function on_interval_select_change() {
    CURRENT_INTERVAL_CHOSEN = __get_current_interval();
    update_interval_filters(CURRENT_INTERVAL_CHOSEN);
}

function get_period_start_time_epoch_seconds() {
    if (check_interval_is_hour_or_day_or_week(CURRENT_INTERVAL_CHOSEN)) {
        return get_period_start_or_end_for_hour_or_day_or_week(START);
    }
    if (CURRENT_INTERVAL_CHOSEN === ONE_MONTH_IN_SECONDS) {
        return get_period_start_for_month();
    }
    if (CURRENT_INTERVAL_CHOSEN === ONE_YEAR_IN_SECONDS) {
        return get_period_start_for_year();
    }
    throw UNRECOGNIZED_INTERVAL;
}

function get_period_end_time_epoch_seconds() {
    if (check_interval_is_hour_or_day_or_week(CURRENT_INTERVAL_CHOSEN)) {
        return get_period_start_or_end_for_hour_or_day_or_week(END)
    }
    if (CURRENT_INTERVAL_CHOSEN === ONE_MONTH_IN_SECONDS) {
        return get_period_end_for_month();
    }
    if (CURRENT_INTERVAL_CHOSEN === ONE_YEAR_IN_SECONDS) {
        return get_period_end_for_year();
    }
    throw UNRECOGNIZED_INTERVAL;
}

function get_period_start_or_end_for_hour_or_day_or_week(start_or_end) {
    return get_data_input_epoch_value_seconds_by_id(
        get_hour_or_day_or_week_period_input(start_or_end)
    );
}

function get_period_start_for_year() {
    let year = get_int_selected_option_for_select(__get_year_select(START));
    let date = create_utc_date(year, 1, 1);
    return convert_date_to_epoch_seconds(date);
}

function get_period_end_for_year() {
    let year = get_int_selected_option_for_select(__get_year_select(END));
    // Date returns previous day of previous month if month = 0 and date = 0,
    // so previous day of the next year is the last day of given year
    let date = create_utc_date(year + 1, 0, 0);
    return convert_date_to_epoch_seconds(date);
}

function get_period_start_for_month() {
    let year = get_int_selected_option_for_select(__get_year_select(START));
    let month_from_zero = get_int_selected_option_for_select(__get_month_select(START));
    let date = create_utc_date(year, month_from_zero, 1);
    return convert_date_to_epoch_seconds(date);
}

function get_period_end_for_month() {
    let year = get_int_selected_option_for_select(__get_year_select(END));
    let month_from_zero = get_int_selected_option_for_select(__get_month_select(END));
    // Date returns previous day if and date = 0, so previous day
    // of the next moth is the last day of given month
    let date = create_utc_date(year, month_from_zero + 1, 0);
    return convert_date_to_epoch_seconds(date);
}


function update_interval_filters(interval) {
    __get_interval_filtering_div().empty();
    if (check_interval_is_hour_or_day_or_week(interval)) {
        if (interval === ONE_HOUR_IN_SECONDS) {
            __get_interval_filtering_div().append(make_hour_filters());
            set_default_hour_filtering_choices();
        }
        __get_interval_filtering_div().append(
            make_date_filtration_for_hour_or_day_or_week_intervals
        );
        set_date_inputs_now();
    } else if (check_interval_is_month_or_year(interval)) {
        __get_interval_filtering_div().append(create_filters_for_month_or_year(interval));
    } else {
        throw UNRECOGNIZED_INTERVAL;
    }
}

function set_date_inputs_now() {
    let now = _get_current_date_for_date_input();
    get_hour_or_day_or_week_period_input(START).val(now);
    get_hour_or_day_or_week_period_input(END).val(now);
}

function set_default_hour_filtering_choices() {
    get_hour_filters_select(START)
        .val(DEFAULT_START_HOUR_FILTER_OPTION)
        .attr('selected', true);
    get_hour_filters_select(END)
        .val(DEFAULT_END_HOUR_FILTER_OPTION)
        .attr('selected', true);
}


function check_interval_is_hour_or_day_or_week(interval) {
    return (interval === ONE_HOUR_IN_SECONDS)
        || (interval === ONE_DAY_IN_SECONDS)
        || (interval === ONE_WEEK_IN_SECONDS)
}

function check_interval_is_month_or_year(interval) {
    return (interval === ONE_MONTH_IN_SECONDS)
        || (interval === ONE_YEAR_IN_SECONDS)
}

function create_utc_date(year, month, day) {
    return new Date(Date.UTC(year, month, day));
}

function convert_date_to_epoch_seconds(date) {
    return date.getTime() / 1000;
}

function __get_current_interval() {
    return get_int_selected_option_for_select(__get_aggregation_interval_select());
}

function get_data_input_epoch_value_seconds_by_id(date_input) {
    // converting to seconds from milliseconds
    return Date.parse(date_input.val()) / 1000;
}