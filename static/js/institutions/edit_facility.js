$(document).ready(function () {
    style_and_setup_selects();
})

function style_and_setup_selects() {
    // disabled is included in django field to ignore possible input
    // but user can move to facility or role page by clicking a descendant
    remove_disable_set_width_100(__get_descendants_select());
    remove_disable_set_width_100(__get_roles_for_facility_select());

    add_descendants_select_on_click_label();
    add_roles_on_click_label();
    
    __get_descendants_select().change(redirect_on_descendant_click);
}

function redirect_on_descendant_click() {
    let descendant_id = get_selected_option_for_select(__get_descendants_select());
    $.ajax({
        url: reverse_url('edit-facility-link-by-pk-in-post-redirect'),
        type: 'POST',
        dataType:'json',
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        data: {
            'pk': descendant_id
        },
        success: (data) => {
            window.open(data.url, '_self');
        },
        error: (data) => {
          add_error_alert('При спробі переходу сталася помилка, ' +
              'якщо після перезавантаження сторінки проблема не зникне, ' +
              'зверніться до адміністратора.'
          );
        }
    })
}

function add_descendants_select_on_click_label() {
    const on_click_redirects = generate_muted_p(
        'При натисканні на об‘єкт вас перенаправить на його сторінку'
    );
    __get_descendants_label().after(on_click_redirects);
}

function add_roles_on_click_label() {
    const on_click_redirects = generate_muted_p(
        'При натисканні на роль вас перенаправить на її сторінку'
    );
    __get_roles_for_facility_select_label().after(on_click_redirects);
}

function __get_descendants_label() {
    return $('#div_id_descendants label');
}


function __get_descendants_select() {
    return $('#id_descendants')
}

function __get_roles_for_facility_select_label() {
    return $('#div_id_roles_that_have_access_to_this_facility label');
}

function __get_roles_for_facility_select() {
    return $('#id_roles_that_have_access_to_this_facility');
}
