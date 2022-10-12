$(document).ready(function () {
    set_width_for_all_selects();
    update_parent_facility_select();
    __get_institution_select().change(update_parent_facility_select);
})

function update_parent_facility_select() {
    let id = __get_selected_institution_id();
    $.ajax({
        url: __get_url_to_get_facilities_options_data_for_institution(),
        type: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        data: {
            institution_id: id
        },
        success: (ids_and_labels) => {
            let parent_facility_select = __get_parent_facility_select();
            parent_facility_select.prop('disabled', false);
            parent_facility_select.empty();
            for (const id_label_object_index in (ids_and_labels)) {
                let hashed_id = ids_and_labels[id_label_object_index][0];
                let label = ids_and_labels[id_label_object_index][1];
                parent_facility_select.append(
                    `<option value="${hashed_id}">${label}</option>`
                )
            }
        },
        error: (error) => {
            window.alert('Під час оновлення даних виникла помилка. ' +
                'Якщо після перезавантаження сторінки вона не зникне, ' +
                'зверніться до адміністратора')
        }
    });
}

function set_width_for_all_selects() {
    __get_parent_facility_select().addClass('w-100');
    __get_institution_select().addClass('w-100');
}

function __get_url_to_get_facilities_options_data_for_institution() {
    return $('#get_institution_facilities_url').text();
}


function __get_selected_institution_id() {
    return __get_institution_select().find('option:selected').val();
}

function __get_institution_select() {
    return $('#id_institution');
}

function __get_parent_facility_select() {
    return $('#id_parent_facility');
}