$(document).ready(() => {
    setup_interval_to_html_mapping();
})


const EARLIEST_YEAR_CAN_BE_QUERIED = 2022; // project started in 2022

const INTERVAL_TO_HTML_START_WITH_END = new Map();

const INTERVAL_TO_CHOICES = new Map([
    [ONE_WEEK_IN_SECONDS, generate_week_choices()],
    [ONE_MONTH_IN_SECONDS, generate_month_choices()],
    [ONE_YEAR_IN_SECONDS, generate_year_choices()]
])

const INTERVAL_TO_INTERVAL_NAME = new Map([
    [ONE_WEEK_IN_SECONDS, 'week'],
    [ONE_MONTH_IN_SECONDS, 'month'],
    [ONE_YEAR_IN_SECONDS, 'year']
])


function create_filters_for_week_month_or_year(interval) {
    let start_and_end_htmls = INTERVAL_TO_HTML_START_WITH_END.get(interval);
    let html_start = start_and_end_htmls[0], html_end = start_and_end_htmls[1];
    let start_div = `
        <div class="d-block">
            ${INTERVAL_FILTERING_START_LABEL}
            ${html_start}
        </div>
    `;
    let end_div = `
        <div class="d-block">
            ${INTERVAL_FILTERING_END_LABEL}
            ${html_end}
        </div>
    `;
    return `
        <div>
            ${start_div}
            ${end_div}
        </div>
    `
}

function create_year_select(start_or_end) {
    return create_select_for_interval(
        ONE_YEAR_IN_SECONDS, start_or_end
    );
}

function create_month_select(start_or_end) {
    return create_select_for_interval(
        ONE_MONTH_IN_SECONDS, start_or_end
    );
}

function create_week_select(start_or_end) {
    return create_select_for_interval(
        ONE_WEEK_IN_SECONDS, start_or_end
    );
}

function create_select_for_interval(interval, start_or_end) {
    let options = create_html_options(INTERVAL_TO_CHOICES.get(interval));
    let name = INTERVAL_TO_INTERVAL_NAME.get(interval);
    return `
        <select class="d-inline form-select w-auto" id="${name}_select_${start_or_end}_id">
            ${options}
        </select>
    `;
}

function generate_year_choices() {
    let CURRENT_YEAR = new Date().getFullYear();
    let years = Array.from(
        {length: CURRENT_YEAR - EARLIEST_YEAR_CAN_BE_QUERIED + 1},
        (_, i) => i + EARLIEST_YEAR_CAN_BE_QUERIED
    );
    return years.map((e) => {
        return [e, e]
    });
}

function generate_month_choices() {
    return Array.from({length: 12}, (e, i) => {
        let month = new Date(null, i + 1, null);
        return [i + 1, month.toLocaleDateString(navigator.language, {month: "short"})];
    })
}

function generate_week_choices() {
    const WEEK_IN_MONTH_COUNT = 4;
    return [...Array.from({length: WEEK_IN_MONTH_COUNT}).keys()].map((e) => {
        return [e + 1, e + 1]
    })
}

function create_html_options(options_value_then_label) {
    return options_value_then_label.reduce(
        (accumulator, value_with_label) =>
            accumulator + `<option value="${value_with_label[0]}">${value_with_label[1]}</option>`,
        ''
    )
}

function setup_interval_to_html_mapping() {
    let year_create_select_set = [create_year_select];
    let month_create_select_set = [create_year_select, create_month_select];
    let week_create_select_set
        = [create_year_select, create_month_select, create_week_select];

    function create_html_for_set(set, start_or_end) {
        let select_htmls = Array.from(set, (f) => f(start_or_end));
        return select_htmls.reduce((accumulator, e) => accumulator + e, '')
    }

    INTERVAL_TO_HTML_START_WITH_END.set(
        ONE_YEAR_IN_SECONDS,
        [
            create_html_for_set(year_create_select_set, START),
            create_html_for_set(year_create_select_set, END),
        ]
    )
    INTERVAL_TO_HTML_START_WITH_END.set(
        ONE_MONTH_IN_SECONDS,
        [
            create_html_for_set(month_create_select_set, START),
            create_html_for_set(month_create_select_set, END),
        ]
    )
    INTERVAL_TO_HTML_START_WITH_END.set(
        ONE_WEEK_IN_SECONDS,
        [
            create_html_for_set(week_create_select_set, START),
            create_html_for_set(week_create_select_set, END),
        ]
    );

}