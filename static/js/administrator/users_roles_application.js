$(document).ready(function () {
        // disable client-side decline button validation
        let button = $('button[type="submit"][value="decline"]');
        button.click(function () {
            let form = $(this).parents('form:first');
            form.attr('novalidate', '');
            form.submit();
        });
    }
)