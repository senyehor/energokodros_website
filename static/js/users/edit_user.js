$(document).ready(function () {
    style_roles_select();
    __get_roles_select().change(redirect_to_role_on_click);
})

function redirect_to_role_on_click() {
    $.ajax({
       url: reverse_url('edit-user-role-pk-in-post'),
        type: 'POST',
        dataType:'json',
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        data: {
            'pk': get_selected_option_for_select(__get_roles_select())
        },
        success: (data) => {
            window.open(data.url, '_self');
        },
        error: (data) => {
          add_error_alert(DEFAULT_UNEXPECTED_ERROR_MESSAGE);
        }
    });
}

function style_roles_select() {
    remove_disabled_set_width_100(__get_roles_select());
}

function __get_roles_select() {
    return $('#id_roles');
}