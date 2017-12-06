from django import template
from django.conf import settings

import re
from pprint import pprint
numeric_test = re.compile("^\d+$")
register = template.Library()

@register.filter(name='getattribute', is_safe=True)
def getattribute(value, arg):
    print(pprint(value))
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    return 