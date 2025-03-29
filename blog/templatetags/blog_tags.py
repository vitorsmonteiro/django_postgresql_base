import markdown
from django import template
from django.utils.safestring import SafeText, mark_safe

register = template.Library()

@register.filter
def markdown_content(value: str) -> SafeText:
    """Convert Markdown content."""
    md = markdown.Markdown(extensions=["fenced_code"])
    content = md.convert(value)
    return mark_safe(content)  # noqa:S308
