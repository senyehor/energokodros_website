function include_search_parameter_if_present_on_page_change(caller_button) {
    let search_parameter = __get_search_parameter();
    if (search_parameter) {
        let new_url = add_search_parameter_to_url(caller_button.href, search_parameter);
        window.location.replace(new_url);
        return false;
    }
}


function add_search_parameter_to_url(url_string, search_value) {
    let url = new URL(url_string)
    url.searchParams.append('search_value', search_value)
    return url
}

function __get_search_parameter() {
    return __get_current_url().searchParams.get('search_value');
}

function __get_current_url() {
    return new URL(window.location.href);
}

function __get_paginator_buttons_div() {
    return $('#pagination_buttons');
}