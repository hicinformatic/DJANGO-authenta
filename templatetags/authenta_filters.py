from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html

import re
numeric_test = re.compile("^\d+$")
register = template.Library()

@register.filter(name='getattribute', is_safe=True)
def getattribute(value, arg):
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    return

@register.filter(name='boolean_icon')
def boolean_icon(field_val):
    svg = {True: 'yes', False: 'no', None: 'unknown'}
    return format_html('<img src="{}" alt="{}" />', static('admin/img/icon-{}.svg'.format(svg[field_val])), field_val) if field_val in svg else field_val