from django import template

register = template.Library()


@register.filter(name='split')
def split(value, arg):
    """Divise une chaîne de texte"""
    return value.split(arg) if isinstance(value, str) else ''


@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplie deux nombres"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0