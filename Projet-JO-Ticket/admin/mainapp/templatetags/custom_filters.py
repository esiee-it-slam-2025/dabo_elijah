from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Splits the value at the given argument and returns the list
    """
    return value.split(arg)