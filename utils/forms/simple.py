from django.forms import Select


class SelectWithFormControlClass(Select):
    """
    when rendering with {% crispy %} form select widget has no form-control,
    so this class adds it
    """

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        ctx['widget']['attrs']['class'] = 'form-control'
        return ctx
