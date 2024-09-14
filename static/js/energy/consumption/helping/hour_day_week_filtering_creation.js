const START = 'start', END = 'end';
const INTERVAL_FILTERING_START_LABEL = '<label class="d-block">Початок</label>';
const INTERVAL_FILTERING_END_LABEL = '<label class="d-block">Кінець</label>'

function make_hour_filters() {
    return `
        <div id="id_hours_filtering">
            ${_make_interval_filter_options()}
            ${_make_hour_filters()}
        </div>
    `
}

function make_date_filtration_for_hour_or_day_or_week_intervals() {
    let start = _make_date_filtration(START, INTERVAL_FILTERING_START_LABEL);
    let end = _make_date_filtration(END, INTERVAL_FILTERING_END_LABEL);
    return start + end;
}

function _make_interval_filter_options() {
    let text = '<div class="d-inline">Фільтрація інтервалу агрегації</div>';
    let filter_every_day_button = `
        <a class="btn ${CHOSEN_BUTTON_CLASS}" id="filter_every_day_button_id">
            Кожен день
        </a>`;
    let filter_whole_interval_button = `
        <a class="btn ${AVAILABLE_BUTTON_CLASS}" id="filter_whole_interval_button_id">
            Увесь інтервал
        </a>`;
    return `
        ${text}
        <div class="d-flex align-items-center py-2">
            <div class="d-inline" id="filter_whole_interval_or_each_day_id">
                ${filter_every_day_button}
                ${filter_whole_interval_button}
            </div>
        </div>
    `
}

function _make_hour_filters() {
    let start_hour_filter_select = __make_hour_filter_select_div('Від', START);
    let end_hour_filter_select = __make_hour_filter_select_div('До', END);
    let reset_button = __make_reset_hour_filters_button(
        'reset_hours_filters_btn', 'Скинути'
    );
    return `
        <div class="d-flex align-items-center">
            <div class="d-inline">
                ${start_hour_filter_select}
                ${end_hour_filter_select}
            </div>
            <div class="d-inline ms-2">
                ${reset_button}
            </div>
        </div>           
    `
}

function __make_reset_hour_filters_button(id, text) {
    return `<a class="btn btn btn-primary" id="${id}">${text}</a>`
}

function __make_hour_filter_select_div(text, start_or_end) {
    let label = `
        <label for="id_hour_filter_${start_or_end}">
            ${text}
        <span class="asteriskField">*</span>
        </label>
    `
    let hours = [...Array(24).keys()];
    let hour_options_0_to_23 = hours.reduce((
        accumulator, e) =>
        accumulator + `<option value="${e}">${String(e).padStart(2, '0')}</option>`, '')
    let hour_select = `
        <select name="hour_filter_${start_or_end}" class="select form-control custom-select w-auto"
                id="id_hour_filter_${start_or_end}">
            ${hour_options_0_to_23}         
        </select>
    `
    return `
        <div class="d-inline form-group w-auto">
            ${label}
            <div class="d-inline-block">
                ${hour_select}
            </div>
        </div>
    `
}

function _make_date_filtration(start_or_end, label) {
    let date_input = `
        <input class="d-block form-control w-auto" type="date"
        name="period_${start_or_end}" id="hour_or_day_or_week_period_${start_or_end}_id">`;
    return `
        <div id="div_id_period_${start_or_end}" class="form-group">
            ${label}
            ${date_input}
        </div>
    `;
}

