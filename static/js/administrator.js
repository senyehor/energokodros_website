$(document).ready(
    function () {
        $('#div_id_access_level').before('' +
            '<button id="get-request-message" type="button" class="btn btn-primary my-2">' +
            'Отримати повідомлення із запиту</button>'
        );
        let csrf = $("[name=crsfmiddlewaretoken]").val();

        let button = $('#get-request-message');
        button.click(function () {
            let request_id = $('[name=users_registration_requests] option:selected').val();
            if (typeof request_id === 'string' && request_id.length === 0) {
                alert('Спочатку необхідно обрати запит');
                return;
            }
            $.ajax({
                url: $('#get-message-for-registration-request-link').val(),
                type: 'post',
                data: {
                    crsfmiddlewaretoken: csrf,
                    request_id: request_id
                },
                success: function (response) {
                    let message_div = $('#registration-message-div');
                    if (!message_div) {
                        button.after('<div id="registration-message-div" class="form-group">' +
                            '    <label for="registration-message">' +
                            '        Повідомлення до заяви' +
                            '    </label>' +
                            '    <div>' +
                            '        <textarea name="registration-message" cols="40" class="textarea form-control"' +
                            '                  id="registration-message" readonly>' +
                            '        </textarea>' +
                            '    </div>' +
                            '</div>');
                    }
                    let result;
                    if (response.message.length === 0) {
                        result = 'Повідомлення відсутнє';
                    } else {
                        result = response.message;
                    }
                    $('#registration-message').setValue(result);
                }
            })
        })
    }
)