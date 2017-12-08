from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator

from .apps import AuthentaConfig as conf
from .manager import UserManager
from . import methods

if conf.ldap.activate: from .methods import ldap as method_ldap

import os, subprocess, unicodedata, time

logger = conf.logger

#██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗
#██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
#██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  
#██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  
#╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗
# ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
class Update(models.Model):
    date_create = models.DateTimeField(conf.App.vn_date_create, auto_now_add=True, editable=False)
    date_update = models.DateTimeField(conf.App.vn_date_update, auto_now=True, editable=False)
    update_by = models.CharField(conf.App.vn_update_by, blank=True, editable=False, max_length=254, null=True, help_text=conf.App.ht_update_by)
    error = models.TextField(conf.App.vn_error, blank=True, null=True, help_text=conf.App.ht_error)

    class Meta:
        abstract = True

    def status(self):
        return True if self.error is None else False
    status.boolean = True

class Group(Group, Update):
    pass

#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
class Method(Update):
    method_conf = conf.Method
    method = models.CharField(method_conf.vn_method, choices=tuple(method_conf.choices), default=method_conf.default, help_text=method_conf.ht_method, max_length=4)
    name = models.CharField(method_conf.vn_name, help_text=method_conf.ht_name, max_length=254)
    enable = models.BooleanField(method_conf.vn_enable, default=True, help_text=method_conf.ht_enable)
    port = models.PositiveIntegerField(method_conf.vn_port, blank=True, default=method_conf.port, help_text=method_conf.ht_port, null=True, validators=[MinValueValidator(0), MaxValueValidator(65535)])
    
    tls = models.BooleanField(method_conf.vn_tls, default=False, help_text=method_conf.ht_tls)
    certificate = models.TextField(method_conf.vn_certificate, blank=True, help_text=method_conf.ht_certificate, null=True)
    self_signed = models.BooleanField(method_conf.vn_self_signed, default=False, help_text=method_conf.ht_self_signed)
    
    is_active = models.BooleanField(method_conf.vn_is_active, default=True)
    is_staff = models.BooleanField(method_conf.vn_is_staff, default=False)
    is_superuser = models.BooleanField(method_conf.vn_superuser, default=False)
    groups = models.ManyToManyField(Group, verbose_name=method_conf.vn_groups, blank=True)
    permissions = models.ManyToManyField(Permission, verbose_name=method_conf.vn_permissions, blank=True)

    if conf.ldap.activate:
        ldap_conf = conf.ldap
        ldap_host = models.CharField(ldap_conf.vn_ldap_host, blank=True, default=ldap_conf.host, help_text=ldap_conf.ht_ldap_host, max_length=254, null=True)
        ldap_define = models.CharField(ldap_conf.vn_ldap_define, blank=True, help_text=ldap_conf.ht_ldap_define, max_length=254, null=True)
        ldap_scope = models.CharField(ldap_conf.vn_ldap_scope, choices=ldap_conf.choices_scope, default=ldap_conf.scope, help_text=ldap_conf.ht_ldap_scope, max_length=14)
        ldap_version = models.CharField(ldap_conf.ht_ldap_version, choices=ldap_conf.choices_version, default=ldap_conf.version, help_text=ldap_conf.ht_ldap_version, max_length=8)
        ldap_bind = models.CharField(ldap_conf.vn_ldap_bind, blank=True, help_text=ldap_conf.ht_ldap_bind, max_length=254, null=True)
        ldap_password = models.CharField(ldap_conf.vn_ldap_password, blank=True, help_text=ldap_conf.ht_ldap_password, max_length=254, null=True)
        ldap_user = models.TextField(ldap_conf.vn_ldap_user, blank=True, help_text=ldap_conf.ht_ldap_user, null=True)
        ldap_search = models.TextField(ldap_conf.vn_ldap_search, help_text=ldap_conf.ht_ldap_search, blank=True, null=True)
        ldap_tls_cacertfile = ldap_conf.tls_cacertfile
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Method, self).save(*args, **kwargs)
        self.certificate_content()

    def certificate_path(self):
        if self.certificate is not None:
            return '{}/{}_{}.crt'.format(conf.App.dir_cert, self.name, self.method)
        return None
    certificate_path.short_description = method_conf.ht_certificate_path

    def certificate_content(self):
        certificate = self.certificate_path()
        if certificate is not None:
            if not os.path.isfile(certificate):
                self.certificate_write(certificate)
            else:
                timestamp_file = os.path.getctime(certificate)
                timestamp_date_update = int(time.mktime(self.date_update.timetuple()))
                if timestamp_file < timestamp_date_update:
                    self.certificate_write(certificate)
                content = open(certificate, 'r').read()
            return content
        return None
    certificate_content.short_description = method_conf.ht_certificate_content

    def certificate_write(self, certificate):
        with open(certificate, 'w') as cert_file:
            cert_file.write(self.certificate)
        cert_file.closed

    class Meta:
        verbose_name = conf.Method.verbose_name
        verbose_name_plural = conf.Method.verbose_name_plural

    def method_get(self):
        logger('debug', 'method getting: {}'.format(self.method))
        return getattr(getattr(methods, '{}'.format(self.method.lower())), 'method_{}'.format(self.method.lower()))(self)

    def admin_button_check(self):
        from django.urls import reverse
        url = reverse('admin:{}_method_check'.format(conf.App.namespace, self._meta.model_name),  args=[self.id])
        return '<a class="button" href="{}">{}</a>'.format(url, self.method_conf.vn_check)
    admin_button_check.allow_tags = True
    admin_button_check.short_description = method_conf.vn_check

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
    method = models.CharField(conf_user.vn_method, choices=conf_user.choices_user_create_method, default=conf_user.default_method, max_length=15)
    additional = models.ManyToManyField(Method, blank=True)
    key = models.CharField(default=conf.User.key, max_length=32, unique=True, validators=[MaxLengthValidator(conf_user.key_max_length), MinLengthValidator(conf_user.key_min_length),], verbose_name=_('Authentication key'),)

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

#████████╗ █████╗ ███████╗██╗  ██╗
#╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
#   ██║   ███████║███████╗█████╔╝ 
#   ██║   ██╔══██║╚════██║██╔═██╗ 
#   ██║   ██║  ██║███████║██║  ██╗
#   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
class Task(Update):
    conf_task = conf.Task
    task = models.CharField(conf_task.vn_task, max_length=254, choices=conf_task.script_tasks, help_text=conf_task.ht_task)
    info = models.TextField(conf_task.vn_info, blank=True, null=True, help_text=conf_task.ht_info)
    status = models.CharField(conf_task.vn_status, max_length=8, choices=conf_task.status, default=conf_task.status_order, help_text=conf_task.ht_status)
    command = models.CharField(conf_task.vn_commmand, max_length=254, blank=True, null=True, help_text=conf_task.ht_commmand, editable=False)
    local_check = models.CharField(conf_task.vn_local_check, max_length=254, blank=True, null=True, help_text=conf_task.ht_local_check, editable=False)

    class Meta:
        verbose_name        = conf.Task.verbose_name
        verbose_name_plural = conf.Task.verbose_name_plural

    def __str__(self):
        return self.get_task_display()

    def prepare(self):
        prepare = {}
        prepare['namespace'] = conf.App.namespace
        prepare['port'] = self.conf_task.django_port
        prepare['background'] = self.conf_task.background
        prepare['python'] = self.conf_task.python
        prepare['directory'] = conf.App.dir_task
        prepare['task'] = self.task
        prepare['extension'] = self.conf_task.python_extension
        prepare['id'] = self.id
        prepare['background_end'] = self.conf_task.background_end
        self.command = self.conf_task.template_command.format(**prepare)
        prepare['binary'] = self.conf_task.binary
        prepare['script'] = self.conf_task.script_can_run
        prepare['script_extension'] = self.conf_task.script_can_run_extension
        prepare['timeout'] = self.conf_task.kill_timeout
        self.local_check = self.conf_task.template_local_check.format(**prepare)
        self.save()

    def can_run(self):
        if self.status != self.conf_task.status_order:
            self.error = self.conf_task.error_not_order
            self.save()
            logger('debug', 'can_run failed: {}'.format(self.error))
            return False
        try: 
            logger('notice', 'local_check: {}'.format(self.local_check))
            subprocess.check_call(self.local_check, shell=True)
            logger('debug', 'can_run success')
            return True
        except subprocess.CalledProcessError as error:
            self.error = error
            logger('debug', 'can_run failed: {}'.format(error))
        return False

    def start_task(self):
        if self.status != self.conf_task.status_ready:
            self.error = self.conf_task.error_not_ready
            self.save()
            logger('debug', 'start_task failed: {}'.format(self.error))
            return False
        try: 
            logger('notice', 'command: {}'.format(self.command))
            subprocess.check_call(self.command, shell=True)
            logger('debug', 'start_task success')
            return True
        except subprocess.CalledProcessError as error:
            self.error = error
            logger('debug', 'start_task failed: {}'.format(error))
        return False
        
