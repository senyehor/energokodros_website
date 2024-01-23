from django.forms import Form

from utils.forms.crispy_buttons import UPDATE_DELETE_BUTTONS_SET


def set_form_buttons_to_update_delete(form: type(Form)) -> type(Form):
    try:
        form.Meta.buttons = UPDATE_DELETE_BUTTONS_SET
    except AttributeError as e:
        raise ValueError('provided form has no Meta') from e
    return form
