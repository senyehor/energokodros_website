from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def create_url_name_id_p_tag_with_link_content(url_name: str) -> str:
    """provides a way to include links in template dynamically"""
    return mark_safe(f"<p id='{url_name}'>{reverse(url_name)}</p>")
