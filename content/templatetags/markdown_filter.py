from django import template
import bleach
import markdown
from content import urlify

register = template.Library()

# add <p> to allowed tags
tags = ['p','h1','h2','h3'] + bleach.ALLOWED_TAGS

@register.filter
def markdownify(text):
    html = markdown.markdown(text)
    html = bleach.clean(html, tags=tags)
    return html

@register.filter
def markdown_urlify(text):
    html = markdown.markdown(text)
    html = bleach.clean(html, tags=tags)
    html = bleach.linkify(html)
    return html

@register.filter
def urlify(text):
    html = bleach.clean(text, tags=tags)
    html = bleach.linkify(html)
    return html
