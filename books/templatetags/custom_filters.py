from django import template

register = template.Library()

@register.filter
def get_format(dictionary, key):
    return dictionary.get(key)
