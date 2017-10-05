from django import template

register = template.Library()

@register.filter(name='getattr', is_safe=True)
def getattr(obj, attr):
    return getattr(obj, attr)