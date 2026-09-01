import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='render_markdown')
def render_markdown(text):
    if not text:
        return ''
    html = markdown.markdown(text, extensions=['fenced_code', 'tables', 'nl2br'])
    return mark_safe(html)
