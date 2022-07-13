from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def show_messages_if_any(context: dict) -> str:
    messages = context.get('messages', None)
    output = ''
    if messages:
        for message in messages:
            output += render_to_string(
                'common/message.html',
                {
                    'message_class': message.tags,
                    'message_text':  message.message
                }
            )
    return mark_safe(output)
