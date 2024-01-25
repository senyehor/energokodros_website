$(document).ready(function () {
    let search_form = $('#searchForm');
    submit_on_enter(search_form);
    make_input_fit_placeholder();
    setup_clear_filter_button(search_form);
    fill_search_field_after_redirect_if_search_value_present();
})

function submit_on_enter(search_form) {
    search_form.keypress(function (e) {
        if (e.which === 13) {
            search_form.submit();
        }
    })
}

function fill_search_field_after_redirect_if_search_value_present() {
    let url = get_current_url();
    let search_value = url.searchParams.get('search_value');
    if (search_value) {
        __get_form_input().val(search_value);
    }
}

function make_input_fit_placeholder() {
    let input = __get_form_input();
    input.attr('size', input.attr('placeholder').length);
}

function setup_clear_filter_button(search_form) {
    $('#clearFilter').click(
        function () {
            __get_form_input().val('');
            search_form.submit();
        }
    )
}

function __get_form_input() {
    return $('#searchFormInput');
}

