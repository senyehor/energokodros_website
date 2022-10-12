$(document).ready(function () {
    update_facilities_list_for_role();
    __get_roles_select().change(update_facilities_list_for_role);
    $('#get_data_button').click(get_consumption_data_and_update);
})

function get_consumption_data_and_update() {
    $.ajax({
        url: reverse_url('get-aggregated-consumption-for-facility'),
        type: 'POST',
        dataType: 'json',
        data: __compose_aggregation_query_parameters(),
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        success: (data) => {
            draw_table(data);
        },
        error: (error) => {
            window.alert('Під час оновлення даних виникла помилка. ' +
                'Якщо після перезавантаження сторінки вона не зникне, ' +
                'зверніться до адміністратора')
        }
    });
}

function update_facilities_list_for_role() {
    $.ajax({
        url: reverse_url('get-facilities-list-for-role'),
        type: 'POST',
        dataType: 'json',
        data: {
            role_id: __get_selected_role_id()
        },
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        success: (ids_and_labels) => {
            update_select_with_options(__get_facility_select(), ids_and_labels);
        },
        error: (error) => {
            window.alert('Під час оновлення даних виникла помилка. ' +
                'Якщо після перезавантаження сторінки вона не зникне, ' +
                'зверніться до адміністратора')
        }
    });
}


function draw_table(data) {
    let data_rows = '';
    for (const time_and_date of data) {
        data_rows += `
            <tr>
            <td>${time_and_date[0]}</td>
            <td>${time_and_date[1]}</td>
            </tr>`
    }
    __get_aggregated_consumption_data_div().html('' +
        '<table class="table">' +
        '<thead>' +
        '<tr>' +
        '<th scope="col">Час</th>' +
        '<th scope="col">Дані</th>' +
        '</tr>' +
        '</thead>' +
        '<tbody>' +
        data_rows +
        '</tbody>' +
        '</table>'
    );
}

function __get_aggregated_consumption_data_div() {
    return $('#energy_content');
}


function __compose_aggregation_query_parameters() {
    let _ = get_selected_option_for_select
    let facility_id = _(__get_facility_select());
    let aggregation_interval = _(__get_aggregation_interval_select);
    let period_start = __get_period_start_epoch();
    let period_end = __get_period_end_epoch();
    return {
        facility_id: facility_id,
        period_start_epoch: period_start,
        period_end_epoch: period_end,
        aggregation_interval_seconds: aggregation_interval
    }
}


function __get_period_start_epoch() {
    return __get_data_input_epoch_value_by_id('#period_start');
}

function __get_data_input_epoch_value_by_id(id) {
    // converting to seconds from milliseconds
    return Date.parse($(`${id}`).val()) / 1000;
}

function __get_period_end_epoch() {
    return __get_data_input_epoch_value_by_id('#period_end');
}


function __get_aggregation_interval_select() {
    return $('#id_aggregation_interval_seconds');
}

function __get_facility_select() {
    return $('#id_facility_to_get_consumption_for');
}

function __get_selected_role_id() {
    return get_selected_option_for_select(__get_roles_select());
}

function __get_roles_select() {
    return $('#id_role');
}