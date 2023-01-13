$(document).ready(function () {
    __get_institution_select().change(
        update_facility_choices_for_chosen_institution_callback(
            __get_institution_select,
            update_facility_selects
        )
    );
    __get_institution_select().trigger('change');
});


function update_facility_selects(ids_and_labels) {
    __get_facilities_selects().forEach(
        (facility_select) => {
            update_select_with_options(facility_select, ids_and_labels);
        }
    );
}

function __get_institution_select() {
    return $('#id_institution');
}

function __get_facilities_selects() {
    let selects_count = $('.multiField').length;
    let selects = [];
    for (let i = 0; i < selects_count; i++) {
        selects.push($(`#id_box_sensor_set-${i}-facility`))
    }
    return selects;
}