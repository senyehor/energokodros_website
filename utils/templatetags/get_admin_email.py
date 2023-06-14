from django import template

from energokodros.settings import DEFAULT_FROM_EMAIL

register = template.Library()


@register.simple_tag
def get_admin_email() -> str:
    return DEFAULT_FROM_EMAIL
