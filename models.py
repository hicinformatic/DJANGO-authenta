from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator

from .apps import AuthentaConfig as conf
from .manager import UserManager

import unicodedata

#██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗
#██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
#██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  
#██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  
#╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗
# ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
class Update(models.Model):
    date_create = models.DateTimeField(conf.App.vn_date_create, auto_now_add=True, editable=False)
    date_update = models.DateTimeField(conf.App.vn_date_update, auto_now=True, editable=False)
    update_by = models.CharField(conf.App.vn_update_by, blank=True, editable=False, max_length=254, null=True)
    error = models.TextField(conf.App.vn_error, blank=True, null=True)

    class Meta:
        abstract = True

class Group(Group, Update):
    pass

#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
class Method(Update):
    conf_ldap = conf.ldap
    ldap_host = models.CharField(conf_ldap.vn_ldap_host, blank=True, default=conf_ldap.host, help_text=conf_ldap.ht_ldap_host, max_length=254, null=True)
    ldap_port = models.PositiveIntegerField(conf_ldap.vn_ldap_port, blank=True, default=conf_ldap.port, help_text=conf_ldap.ht_ldap_port, null=True, validators=[MinValueValidator(0), MaxValueValidator(65535)])
    ldap_tls = models.BooleanField(conf_ldap.vn_ldap_tls, default=False, help_text=conf_ldap.ht_ldap_tls)
    ldap_cert = models.FileField(conf_ldap.vn_ldap_cert, blank=True, help_text=conf_ldap.ht_ldap_cert, null=True, upload_to=conf_ldap.dir_cert)
    ldap_define = models.CharField(conf_ldap.vn_ldap_define, blank=True, help_text=conf_ldap.ht_ldap_define, max_length=254, null=True)
    ldap_scope = models.CharField(conf_ldap.vn_ldap_scope, choices=conf_ldap.choices_scope, default=conf_ldap.scope, help_text=conf_ldap.ht_ldap_scope, max_length=14)
    ldap_version = models.CharField(conf_ldap.ht_ldap_version, choices=conf_ldap.choices_version, default=conf_ldap.version, help_text=conf_ldap.ht_ldap_version, max_length=8)
    ldap_bind = models.CharField(conf_ldap.vn_ldap_bind, blank=True, help_text=conf_ldap.ht_ldap_bind, max_length=254, null=True)
    ldap_password = models.CharField(conf_ldap.vn_ldap_password, blank=True, help_text=conf_ldap.ht_ldap_password, max_length=254, null=True)
    ldap_user = models.TextField(conf_ldap.vn_ldap_user, blank=True, help_text=conf_ldap.ht_ldap_user, null=True)
    ldap_search = models.TextField(conf_ldap.vn_ldap_search, help_text=conf_ldap.ht_ldap_search, blank=True, null=True)

    class Meta:
        verbose_name = conf.Method.verbose_name
        verbose_name_plural = conf.Method.verbose_name_plural

#██╗   ██╗███████╗███████╗██████╗ 
#██║   ██║██╔════╝██╔════╝██╔══██╗
#██║   ██║███████╗█████╗  ██████╔╝
#██║   ██║╚════██║██╔══╝  ██╔══██╗
#╚██████╔╝███████║███████╗██║  ██║
# ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
class User(AbstractUser):
    conf_user = conf.User
    username = models.CharField(conf_user.vn_username, blank=conf_user.null_username, max_length=254, null=conf_user.null_username, unique=conf_user.unique_username, validators=[AbstractUser.username_validator],)
    email = models.EmailField(conf_user.vn_email, blank=conf_user.null_email, null=conf_user.null_email, unique=conf_user.unique_email)
    is_active = models.BooleanField(conf_user.vn_is_active, default=conf_user.default_is_active)
    is_staff = models.BooleanField(conf_user.vn_is_staff, default=conf_user.default_is_staff)
    first_name = models.CharField(conf_user.vn_firstname, blank=conf_user.null_firstname, max_length=30, null=conf_user.null_firstname)
    last_name = models.CharField(conf_user.vn_lastname, blank=conf_user.null_lastname, max_length=30, null=conf_user.null_lastname)
    date_joined = models.DateTimeField(conf_user.vn_date_joined, auto_now_add=True, editable=False)
    date_update = models.DateTimeField(conf.App.vn_date_update, auto_now=True, editable=False)
    update_by = models.CharField(conf.App.vn_update_by, editable=False, max_length=254)
    method = models.CharField(conf_user.vn_method, choices=conf_user.choices_method, default=conf_user.default_method, max_length=15)
    additional = models.ManyToManyField(Method, blank=True)

    objects = UserManager()
    USERNAME_FIELD = conf_user.unique_identity
    REQUIRED_FIELDS = conf_user.required_fields

    class Meta:
        verbose_name = conf.User.verbose_name
        verbose_name_plural = conf.User.verbose_name_plural

    def clean(self):
        super(AbstractUser, self).clean()
        if self.conf_user.field_username in self.REQUIRED_FIELDS or self.username is not None:
            self.username = unicodedata.normalize(self.conf_user.normalize, self.username) 
        self.email = self.__class__.objects.normalize_email(self.email)

class Task(Update):
    task = models.CharField(conf.Task.vn_task, max_length=254, choices=conf.Task.script_tasks, help_text=conf.Task.ht_task)
    info = models.TextField(conf.Task.vn_info, blank=True, null=True, help_text=conf.Task.ht_info)
    status = models.CharField(conf.Task.vn_status, max_length=8, choices=conf.Task.status, default=conf.Task.status_order, help_text=conf.Task.ht_status)
    command = models.CharField(conf.Task.vn_commmand, max_length=254, blank=True, null=True, help_text=conf.Task.ht_commmand)

    class Meta:
        verbose_name        = conf.Task.verbose_name
        verbose_name_plural = conf.Task.verbose_name_plural

    def __str__(self):
        return self.get_task_display()

    def save(self, *args, **kwargs):
        response = super(Task, self).save(*args, **kwargs)
        self.prepare()
        return response

######################
    def prepare(self):
        prepare = {
            'background' : conf.Task.background,
            'python' : conf.Task.python,
            'directory' : conf.App.dir_task,
            'task' : self.task,
            'extension' : conf.Task.python_extension,
            'id' : self.id,
            'background_end' : conf.Task.background_end,
        }
        self.command = '{background} {python} {directory}/{task}{extension} {id} {background_end}'.format(prepare)