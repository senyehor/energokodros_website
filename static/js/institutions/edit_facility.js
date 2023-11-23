$(document).ready(function () {
    style_and_setup_descendants_select();
    add_descendants_select_on_click_label();
    __get_descendants_select().change(redirect_on_descendant_click);
})

function style_and_setup_descendants_select() {
    // disabled is included in django field to ignore possible input
    // but user can move to facility page by clicking a descendant
    __get_descendants_select().removeAttr('disabled');
    __get_descendants_select().addClass('w-100');
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
    const on_click_redirects = '' +
        '<p class="fw-light text-muted">' +
        'При натисканні на об‘єкт вас перенаправить на його сторінку' +
        '</p>'
    __get_descendants_label().after(on_click_redirects);
}

function __get_descendants_label() {
    return $('#div_id_descendants label');
}


function __get_descendants_select() {
    return $('#id_descendants')
}
