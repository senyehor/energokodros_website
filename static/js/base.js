$(document).ready(function () {
    $('input').each(function () {
            $(this)[0].setCustomValidity('Це поле необхідно заповнити');
        }
    );
});