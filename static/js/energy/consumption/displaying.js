$(document).ready(function () {
    __get_set_view_mode_to_table_button().click(__set_display_mode_to_table_and_update_if_data_is_present);
    __get_set_view_mode_to_chart_button().click(__set_display_mode_to_chart_and_update_if_data_is_present);
})

const DRAW_TABLE = 'table';
const DRAW_CHART = 'chart';

const CHOSEN_BUTTON_CLASS = 'btn-outline-secondary';
const AVAILABLE_BUTTON_CLASS = 'btn-outline-primary';

let CHOSEN_DISPLAYING_OPTION = DRAW_TABLE;

let CONSUMPTION = null, TOTAL_CONSUMPTION = null;

let CONSUMPTION_INDEX_IN_RAW_DATA = 1, LABEL_INDEX_IN_RAW_DATA = 0, CONSUMPTION_FORECAST_INDEX_IN_RAW_DATA = 2;

function draw_content() {
    if (CONSUMPTION) {
        if (CHOSEN_DISPLAYING_OPTION === DRAW_TABLE) {
            _draw_table(CONSUMPTION);
            return;
        }
        if (CHOSEN_DISPLAYING_OPTION === DRAW_CHART) {
            _draw_chart(CONSUMPTION);
        }
    }
    throw new Error('consumption is not set')
}

function _draw_chart(data) {
    __get_aggregated_consumption_data_div().empty();
    __get_aggregated_consumption_data_div().append(
        '<canvas id="energy_chart"></canvas>'
    );
    let datasets = __generate_chart_data(data);
    const config = {
        type: 'bar',
        data: datasets,
        options: {
            plugins: {
                zoom: {
                    zoom: {
                        wheel: {
                            enabled: true,
                        },
                        pinch: {
                            enabled: true
                        },
                        mode: 'x',
                    }
                },
                title: {
                    display: true,
                    text: 'Дані у кіловат годинах',
                }
            },
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: false,
                    beginAtZero: true
                }
            }
        }
    }
    const myChart = new Chart(
        $('#energy_chart'),
        config
    );
}

function _draw_table(data) {
    __set_energy_html_content(__generate_table(data))
}

function __generate_chart_data(raw_consumption_data) {
    let labels = [];
    let consumption = [];
    let consumption_forecast = [];
    if (_check_consumption_forecast_is_present(raw_consumption_data)) {
        for (const line of raw_consumption_data) {
            labels.push(line[LABEL_INDEX_IN_RAW_DATA]);
            consumption.push(parseFloat(line[CONSUMPTION_INDEX_IN_RAW_DATA]));
            consumption_forecast.push(parseFloat(line[CONSUMPTION_FORECAST_INDEX_IN_RAW_DATA]))
        }
    } else {
        consumption_forecast = null;
        for (const line of raw_consumption_data) {
            labels.push(line[LABEL_INDEX_IN_RAW_DATA]);
            consumption.push(parseFloat(line[CONSUMPTION_INDEX_IN_RAW_DATA]));
        }
    }
    let data = {
        labels: labels,
        datasets: [
            {
                label: 'Споживання',
                backgroundColor: 'rgb(255, 99, 132, 0.7)',
                data: consumption,
            }
        ]
    };
    if (consumption_forecast) {
        data.datasets.push({
            label: 'Прогнозоване споживання',
            backgroundColor: 'rgba(152,255,134,0.7)',
            data: consumption_forecast,
        })
    }
    return data;
}


function __set_energy_html_content(content) {
    __get_aggregated_consumption_data_div().html(content);
}

function __generate_table(raw_consumption_data) {
    let data_rows = '';
    for (const item of raw_consumption_data) {
        data_rows += `
            <tr>
            <td>${item[LABEL_INDEX_IN_RAW_DATA]}</td>
            <td>${item[CONSUMPTION_INDEX_IN_RAW_DATA]}</td>
            </tr>`
    }
    return '' +
        '<table class="table">' +
        '<thead>' +
        '<tr>' +
        '<th scope="col">Час</th>' +
        '<th scope="col">Кіловат години</th>' +
        '</tr>' +
        '</thead>' +
        '<tbody>' +
        data_rows +
        '</tbody>' +
        '</table>'
}

function _check_consumption_forecast_is_present(raw_consumption_data) {
    return raw_consumption_data[0][CONSUMPTION_FORECAST_INDEX_IN_RAW_DATA] !== undefined
}

function __set_display_mode_to_table_and_update_if_data_is_present() {
    __set_button_to_chosen(__get_set_view_mode_to_table_button());
    __set_button_to_can_be_chosen(__get_set_view_mode_to_chart_button());
    CHOSEN_DISPLAYING_OPTION = DRAW_TABLE;
    if (CONSUMPTION) {
        _draw_table(CONSUMPTION);
    }
}

function __set_display_mode_to_chart_and_update_if_data_is_present() {
    __set_button_to_chosen(__get_set_view_mode_to_chart_button());
    __set_button_to_can_be_chosen(__get_set_view_mode_to_table_button());
    CHOSEN_DISPLAYING_OPTION = DRAW_CHART;
    if (CONSUMPTION) {
        _draw_chart(CONSUMPTION);
    }
}

function __set_button_to_chosen(button) {
    button.removeClass(AVAILABLE_BUTTON_CLASS);
    button.addClass(CHOSEN_BUTTON_CLASS);
}

function __set_button_to_can_be_chosen(button) {
    button.removeClass(CHOSEN_BUTTON_CLASS);
    button.addClass(AVAILABLE_BUTTON_CLASS);
}

function __remove_chosen_class(button) {
    button.removeClass(CHOSEN_BUTTON_CLASS);
}

