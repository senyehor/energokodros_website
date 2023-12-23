$(document).ready(function () {
    set_width_for_all_selects();
    __get_institution_select().change(
        update_facility_choices_for_chosen_institution_callback(
            __get_institution_select,
            update_facility_select
        )
    );
    __get_institution_select().trigger('change');
})

function update_facility_select(ids_and_labels) {
    update_select_with_options(__get_parent_facility_select(), ids_and_labels);
}

function set_width_for_all_selects() {
    __get_parent_facility_select().addClass('w-100');
    __get_institution_select().addClass('w-100');
}


function __get_institution_select() {
    return $('#id_institution');
}

function __get_parent_facility_select() {
    return $('#id_parent_facility');
}