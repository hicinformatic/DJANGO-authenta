from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.urls import reverse

from .manager import UserManager
from .settings import _authenta

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Username'), blank=_authenta.usernamenull, max_length=254, null=_authenta.usernamenull, unique=_authenta.usernameuniq)
    email = models.EmailField(_('Email address'), blank=_authenta.emailnull, null=_authenta.emailnull, unique=_authenta.emailuniq)
    is_active = models.BooleanField(_('Active'), default=_authenta.isactivedefault)
    is_staff = models.BooleanField(_('Staff'), default=_authenta.isstaffdefault)
    first_name = models.CharField(_('First name'), blank=_authenta.firstnamenull, max_length=30, null=_authenta.firstnamenull)
    last_name = models.CharField(_('Last name'), blank=_authenta.lastnamenull, max_length=30, null=_authenta.lastnamenull)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True, editable=False)
    date_update = models.DateTimeField(_('Last modification date'), auto_now=True, editable=False)
    update_by = models.CharField(_('Update by'), editable=False, max_length=254)
    authentication_method = models.PositiveSmallIntegerField(_('Authentication method'), choices=_authenta.methods, default=2)

    objects = UserManager()
    USERNAME_FIELD = _authenta.uniqidentity
    REQUIRED_FIELDS = _authenta.requiredfields

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('authenta:ProfileEXT', args=[str(self.id), 'html'])


class Group(Group):
    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')