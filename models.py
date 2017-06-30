from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager
from .settings import _authenta

class User(AbstractUser, PermissionsMixin):
    username = models.CharField(_('Username'), unique=True)
    email = models.EmailField(_('email address'), unique=_authenta.emailuniq, blank=_authenta.emailblank, null=_authenta.emailnull)
    is_staff = models.BooleanField(_('active'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    firstname = models.CharField(_('first name'), max_length=30, blank=True)
    lastname = models.CharField(_('last name'), max_length=30, blank=True)
    datecreate = models.DateTimeField(_('Creation date'), auto_now_add=True, editable=False)
    dateupdate = models.DateTimeField(_('Last modification date'), auto_now=True, editable=False)

    objects = UserManager()
    USERNAME_FIELD = _authenta.usernamefield
    REQUIRED_FIELDS = _authenta.requiredfieds

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')