$(document).ready(function () {
    add_spacing_between_form_group();
})

function add_spacing_between_form_group() {
    $('form > div.form-group').each(
        function () {
            $(this).addClass('pb-2');
        }
    )
}