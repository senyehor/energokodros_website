$(document).ready(() => {
    __get_aggregation_interval_select().change(
        on_interval_select_change
    );
    __get_hours_filtering_reset_button().click(__set_default_hour_filtering_choices);
    __get_aggregation_interval_select().trigger('change');
})

const ONE_HOUR_IN_SECONDS = 60 * 60,
    ONE_DAY_IN_SECONDS = ONE_HOUR_IN_SECONDS * 24,
    ONE_WEEK_IN_SECONDS = ONE_DAY_IN_SECONDS * 7,
    ONE_MONTH_IN_SECONDS = ONE_WEEK_IN_SECONDS * 4,
    ONE_YEAR_IN_SECONDS = ONE_MONTH_IN_SECONDS * 12;

const DEFAULT_START_HOUR_FILTER_OPTION = '0', DEFAULT_END_HOUR_FILTER_OPTION = '23';

let CURRENT_INTERVAL_CHOSEN = null;

function on_interval_select_change() {
    let previous_interval = CURRENT_INTERVAL_CHOSEN;
    CURRENT_INTERVAL_CHOSEN = __get_current_interval();
    if (previous_interval === null) {
        set_interval_filters(CURRENT_INTERVAL_CHOSEN);
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
    }
    if (
        interval === ONE_WEEK_IN_SECONDS
        || interval === ONE_MONTH_IN_SECONDS
        || interval === ONE_YEAR_IN_SECONDS
    ) {
        // todo
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

function _check_interval_is_one_hour() {
    return __check_interval_in_seconds_is_selected(ONE_HOUR_IN_SECONDS);
}

function __get_current_interval() {
    return parseInt(
        get_selected_option_for_select(__get_aggregation_interval_select())
    );
}

function __check_interval_in_seconds_is_selected(interval) {
    return __get_current_interval() === interval;
}