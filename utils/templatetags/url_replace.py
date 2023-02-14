from typing import Any

from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag
def url_replace(request: HttpRequest, field: str, value: Any):
    query_string = request.GET.copy()
    query_string[field] = value
    return query_string.urlencode()
