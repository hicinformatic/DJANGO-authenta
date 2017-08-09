from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class _authenta:
    def __new__(self):
        self.additional_methods = (('LDAP', 'ldap'),('FACEBOOK', 'Facebook'))
        return super(_authenta, self).__new__(self)
