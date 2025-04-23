from django import template

register = template.Library()

@register.filter
def get_range(value, start=0):
    """Generate a range of numbers for use in templates."""
    try:
        value = int(value)
        start = int(start)
        return range(start, start + value)
    except (ValueError, TypeError):
        return range(0)
