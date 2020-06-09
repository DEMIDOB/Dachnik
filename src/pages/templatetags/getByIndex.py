from django import template

register = template.Library()

@register.filter
def get_by_index(f, i):
    return f[i]
