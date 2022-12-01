function redirect_to_object(redirect_url, id) {
    $.ajax({
        url: reverse_url(redirect_url),
        type: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        data: {id: id},
        success: (data) => {
            window.open(data.url, '_self');
        },
        error: (data) => {
            add_error_alert(DEFAULT_UNEXPECTED_ERROR_MESSAGE);
        }
    });
}

function redirect_from_selected_option_and_clear_selected_on_click(redirect_url) {
    // clearing selected as when users go back to page option remains selected
    return function () {
        let select = $(this);
        let id = get_selected_option_for_select(select);
        redirect_to_object(redirect_url, id);
    }
}