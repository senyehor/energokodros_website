$(document).ready(function () {
    let search_form = $('#searchForm');
    submit_on_enter(search_form);
    make_input_fit_placeholder(search_form);
    setup_clear_filter_button(search_form);
})

function submit_on_enter(search_form) {
    search_form.keypress(function (e) {
        if (e.which === 13) {
            search_form.submit();
        }
    })
}

function make_input_fit_placeholder(search_form) {
    let input = search_form.children(':input');
    input.attr('size', input.attr('placeholder').length);
}

function setup_clear_filter_button(search_form) {
    let input = search_form.children(':input');
    $('#clearFilter').click(
        function () {
            input.value = '';
            search_form.submit();
        }
    )
}

