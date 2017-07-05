from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

from .manager import UserManager
from .settings import _authenta

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Username'), max_length=254, unique=_authenta.usernameuniq, blank=_authenta.usernameblank, null=_authenta.usernamenull)
    email = models.EmailField(_('Email address'), unique=_authenta.emailuniq, blank=_authenta.emailblank, null=_authenta.emailnull)
    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Active'), default=True)
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True, editable=False)
    date_update = models.DateTimeField(_('Last modification date'), auto_now=True, editable=False)
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


class Group(Group):

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')