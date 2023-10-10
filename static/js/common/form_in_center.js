$(document).ready(function () {
    add_spacing_between_form_group();
    add_confirmation_to_all_delete_buttons();
})

function add_spacing_between_form_group() {
    $('form > div.form-group').each(
        function () {
            $(this).addClass('pb-2');
        }
    )
}

function add_confirmation_to_all_delete_buttons() {
    const confirm_deletion_text = 'Підтвердьте видалення';
    let delete_buttons = $('button[type="submit"][value="delete"]');
    delete_buttons.each(
        (index, button) => {
            $(button).on('click',
                (event) => {
                    if (window.confirm(confirm_deletion_text)) {
                        return;
                    }
                    event.preventDefault();
                    event.stopPropagation();
                })
        }
    );
}