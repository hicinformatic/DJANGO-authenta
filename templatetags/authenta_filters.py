from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html
from django.db.models.fields import NOT_PROVIDED

import re
numeric_test = re.compile("^\d+$")
register = template.Library()

@register.filter(name='boolean_icon')
def boolean_icon(field_val):
    svg = {True: 'yes', False: 'no', None: 'unknown', '': 'unknown' }
    return format_html('<img src="{}" alt="{}" />', static('admin/img/icon-{}.svg'.format(svg[field_val])), field_val) if field_val in svg else field_val

@register.simple_tag(name='getattribute_field')
def getattribute_field(instance, field_name, attribute):
    field = instance._meta.get_field(field_name)
    if field and hasattr(field, attribute):
        attr = getattr(field, attribute)
        if attribute == 'verbose_name':
            return attr.title() 
        return attr if attr is not NOT_PROVIDED else boolean_icon(None)
    return boolean_icon(None)

@register.simple_tag(name='getattribute')
def getattribute(obj, attribute):
    if hasattr(obj, str(attribute)):
        return getattr(obj, attribute)
    elif hasattr(obj, 'has_key') and obj.has_key(attribute):
        return obj[attribute]
    elif numeric_test.match(str(attribute)) and len(obj) > int(attribute):
        return obj[int(attribute)]
    return boolean_icon(None)