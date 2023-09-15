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
    let previous_interval = CURRENT_INTERVAL_CHOSEN;
    CURRENT_INTERVAL_CHOSEN = __get_current_interval();
    if (check_interval_filtering_does_not_need_to_be_changed(
        previous_interval,
        CURRENT_INTERVAL_CHOSEN
    )) {
        return;
    }
    update_interval_filters(CURRENT_INTERVAL_CHOSEN);
}

function update_interval_filters(interval) {
    __get_interval_filtering_div().empty();
    if (interval === ONE_HOUR_IN_SECONDS || interval === ONE_DAY_IN_SECONDS) {
        if (interval === ONE_HOUR_IN_SECONDS) {
            __get_interval_filtering_div().append(make_hour_filters());
            set_default_hour_filtering_choices();
        }
        __get_interval_filtering_div().append(
            make_date_filtration_for_one_hour_or_one_day_intervals
        );
        set_date_inputs_now();
    } else if (check_interval_is_week_month_or_year(interval)) {
        __get_interval_filtering_div().append(create_filters_for_week_month_or_year(interval));
    } else {
        throw UNRECOGNIZED_INTERVAL;
    }
}

function set_default_hour_filtering_choices() {
    __get_hour_filtering_start_select()
        .val(DEFAULT_START_HOUR_FILTER_OPTION)
        .attr('selected', true);
    __get_hour_filtering_end_select()
        .val(DEFAULT_END_HOUR_FILTER_OPTION)
        .attr('selected', true);
}

function check_interval_filtering_does_not_need_to_be_changed(previous_interval, current_interval) {
    return check_interval_is_week_month_or_year(previous_interval)
        && check_interval_is_week_month_or_year(current_interval);
}

function check_interval_is_hour_or_day(interval) {
    return (interval === ONE_HOUR_IN_SECONDS) || (interval === ONE_DAY_IN_SECONDS)
}

function check_interval_is_week_month_or_year(interval) {
    return (interval === ONE_WEEK_IN_SECONDS)
        || (interval === ONE_MONTH_IN_SECONDS)
        || (interval === ONE_YEAR_IN_SECONDS)
}

function __get_current_interval() {
    return parseInt(
        get_selected_option_for_select(__get_aggregation_interval_select())
    );
}

function get_data_input_epoch_value_seconds_by_id(date_input) {
    // converting to seconds from milliseconds
    return Date.parse(date_input.val()) / 1000;
}