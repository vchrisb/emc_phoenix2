from django import template
import markdown
from content import urlify

register = template.Library()

@register.filter
def markdownify(text):
    # safe_mode governs how the function handles raw HTML
    return markdown.markdown(text, safe_mode='escape')

@register.filter
def markdown_urlify(text):
    # safe_mode governs how the function handles raw HTML
    urlify_ext = urlify.URLifyExtension()
    extensions = [urlify_ext]
    return markdown.markdown(text, extensions, safe_mode='escape')
