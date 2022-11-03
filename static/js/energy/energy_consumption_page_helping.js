$(document).ready(function () {
    update_facilities_list_for_role();
    __get_roles_select().change(update_facilities_list_for_role);
    __get_aggregation_interval_select().change(
        add_or_remove_hours_filtering_for_aggregation_interval_select
    );
    __get_hours_filtering_reset_button().click(reset_hours_filters);
    __get_hours_filtering_start_select().change(__remove_error_from_hours_select);
    __get_hours_filtering_end_select().change(__remove_error_from_hours_select);
})

let INCLUDE_HOURS_FILTER = false;

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

function add_or_remove_hours_filtering_for_aggregation_interval_select() {
    let hours_filtering_div = __get_hours_filtering_div();
    if (_check_one_hour_interval_is_selected()) {
        hours_filtering_div.removeClass('d-none');
    } else {
        hours_filtering_div.addClass('d-none');
    }
}

function reset_hours_filters() {
    $('#id_hour_filter_start_none_option').prop('selected', true);
    $('#id_hour_filter_end_none_option').prop('selected', true);
}

function check_control_form_required_fields_are_filled(event) {
    let form = __get_control_form();
    let fields = form.find('input:required, select:required').serializeArray();
    $.each(fields, function (i, field) {
        if (!field.value) {
            add_error_alert('Не усі поля були заповнені');
            event.stopImmediatePropagation();
            return false
        }
    })
}

function validate_hours_filters_if_one_hour_aggregation_interval_is_chosen() {
    // both should be selected, or none if aggregation interval is one hour
    INCLUDE_HOURS_FILTER = false;
    if (!_check_one_hour_interval_is_selected()) {
        return;
    }
    const EMPTY_VALUE = '';
    let start_value = get_selected_option_for_select(__get_hours_filtering_start_select());
    let end_value = get_selected_option_for_select(__get_hours_filtering_end_select());
    if (start_value === EMPTY_VALUE && end_value === EMPTY_VALUE) {
        return;
    }
    if (start_value === EMPTY_VALUE) {
        __add_error_for_hours_filtering_select(__get_hours_filtering_start_select());
        return;
    }
    if (end_value === EMPTY_VALUE) {
        __add_error_for_hours_filtering_select(__get_hours_filtering_end_select());
        return;
    }
    INCLUDE_HOURS_FILTER = true;
}

function _check_one_hour_interval_is_selected() {
    let value = parseInt(get_selected_option_for_select(__get_aggregation_interval_select()));
    let seconds_in_hour = 60 * 60;
    return value === seconds_in_hour;
}

function __remove_error_from_hours_select() {
    $(this).removeClass('is-invalid');
}

function __add_error_for_hours_filtering_select(select) {
    select.addClass('is-invalid');
    add_error_alert('Обидва погодинних фільтри повинні бути обрані одночасно, або жоден');
}

function __get_hours_filtering_start_select() {
    return $('#id_hour_filter_start');
}

function __get_hours_filtering_end_select() {
    return $('#id_hour_filter_end');
}

function __get_hours_filtering_reset_button() {
    return $('#reset_hours_filters_btn');
}

function __get_hours_filtering_div() {
    return $('#id_hours_filtering');
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

function __get_control_form() {
    return $('#id_control_form');
}

function __get_set_table_button() {
    return $('#set_table_button')
}

function __get_set_chart_button() {
    return $('#set_chart_button')
}