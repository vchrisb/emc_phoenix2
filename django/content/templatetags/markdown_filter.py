from django import template
import bleach
import markdown
from content import urlify

register = template.Library()

@register.filter
def markdownify(text):
    tags = ['p'] + bleach.ALLOWED_TAGS
    html = markdown.markdown(text)
    html = bleach.clean(html, tags=tags)
    return html

@register.filter
def markdown_urlify(text):
    tags = ['p'] + bleach.ALLOWED_TAGS
    html = markdown.markdown(text)
    html = bleach.clean(html, tags=tags)
    html = bleach.linkify(html)
    return html

@register.filter
def urlify(text):
    html = bleach.clean(text)
    html = bleach.linkify(html)
    return html
