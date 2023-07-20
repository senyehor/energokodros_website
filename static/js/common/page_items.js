$(document).ready(function () {
    $('#items > div').each(
        function () {
            bg_light_on_hover($(this));
        }
    )
})

function bg_light_on_hover(elem) {
    let bg_class = 'bg-light';
    elem.hover(
        function () {
            $(this).addClass(bg_class);
        },
        function () {
            $(this).removeClass(bg_class);
        },
    )
}

