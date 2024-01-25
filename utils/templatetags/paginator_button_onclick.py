from django import template

register = template.Library()


@register.simple_tag
def paginator_button_onclick():
    """shortcut to avoid js code in template"""
    return 'include_search_parameter_if_present_on_page_change(this);return false;'
