$(document).ready(function () {
    __get_set_view_mode_to_table_button().click(__set_display_mode_to_table_and_update_if_data_is_present);
    __get_set_view_mode_to_chart_button().click(__set_display_mode_to_chart_and_update_if_data_is_present);
})

const DRAW_TABLE = 'table';
const DRAW_CHART = 'chart';

const CHOSEN_BUTTON_CLASS = 'btn-outline-secondary';
const AVAILABLE_BUTTON_CLASS = 'btn-outline-primary';

let CHOSEN_DISPLAYING_OPTION = DRAW_TABLE;

let LATEST_RECEIVED_DATA = null;


function draw_content(data) {
    if (CHOSEN_DISPLAYING_OPTION === DRAW_TABLE) {
        _draw_table(data);
        return;
    }
    if (CHOSEN_DISPLAYING_OPTION === DRAW_CHART) {
        _draw_chart(data);

    }
}

function _draw_chart(data) {
    __get_aggregated_consumption_data_div().empty();
    __get_aggregated_consumption_data_div().append(
        '<canvas id="energy_chart" style="overflow-x: scroll;"></canvas>'
    );
    let datasets = __generate_chart_datasets(data);
    const config = {
        type: 'bar',
        data: datasets,
        options: {
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true
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

function __generate_chart_datasets(data) {
    const time_index = 0;
    const consumption_index = 1;
    const consumption_forecast_index = 2;
    let labels = [];
    let consumption = [];
    let consumption_forecast = [];
    for (const line of data) {
        labels.push(line[time_index]);
        consumption.push(parseFloat(line[consumption_index]));
        consumption_forecast.push(parseFloat(line[consumption_forecast_index]))
    }
    return {
        labels: labels,
        datasets: [
            {
                label: 'Споживання',
                backgroundColor: 'rgb(255, 99, 132)',
                data: consumption,
            },
            {
                label: 'Прогнозоване споживання',
                backgroundColor: 'rgb(97,97,97)',
                data: consumption_forecast,
            }
        ]
    };
}


function __set_energy_html_content(content) {
    __get_aggregated_consumption_data_div().html(content);
}

function __generate_table(data) {
    let data_rows = '';
    for (const time_and_date of data) {
        data_rows += `
            <tr>
            <td>${time_and_date[0]}</td>
            <td>${time_and_date[1]}</td>
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

function __set_display_mode_to_table_and_update_if_data_is_present() {
    __set_button_to_chosen(__get_set_view_mode_to_table_button());
    __set_button_to_can_be_chosen(__get_set_view_mode_to_chart_button());
    CHOSEN_DISPLAYING_OPTION = DRAW_TABLE;
    if (LATEST_RECEIVED_DATA) {
        _draw_table(LATEST_RECEIVED_DATA);
    }
}

function __set_display_mode_to_chart_and_update_if_data_is_present() {
    __set_button_to_chosen(__get_set_view_mode_to_chart_button());
    __set_button_to_can_be_chosen(__get_set_view_mode_to_table_button());
    CHOSEN_DISPLAYING_OPTION = DRAW_CHART;
    if (LATEST_RECEIVED_DATA) {
        _draw_chart(LATEST_RECEIVED_DATA);
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
