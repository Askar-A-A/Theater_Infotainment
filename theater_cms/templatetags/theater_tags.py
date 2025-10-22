from django import template
import re

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

@register.filter
def translate_to_arabic(value):
    """Translate English text to Arabic for dates and common terms."""
    if not value:
        return value
    
    # Month translations
    month_translations = {
        'January': 'يناير',
        'February': 'فبراير', 
        'March': 'مارس',
        'April': 'أبريل',
        'May': 'مايو',
        'June': 'يونيو',
        'July': 'يوليو',
        'August': 'أغسطس',
        'September': 'سبتمبر',
        'October': 'أكتوبر',
        'November': 'نوفمبر',
        'December': 'ديسمبر'
    }
    
    # Common date terms
    common_translations = {
        'to': 'إلى',
        'and': 'و',
        '-': ' - ',
        ',': '،'
    }
    
    # Convert to string if not already
    text = str(value)
    
    # Replace months
    for english, arabic in month_translations.items():
        text = text.replace(english, arabic)
    
    # Replace common terms
    for english, arabic in common_translations.items():
        text = text.replace(english, arabic)
    
    return text
