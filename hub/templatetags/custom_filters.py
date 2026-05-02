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


@register.filter(name='add_class')
def add_class(field, css):
    """Ajoute une ou plusieurs classes CSS à un champ de formulaire Django"""
    if not field:
        return ''
    return field.as_widget(attrs={'class': css})