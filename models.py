from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator

from .apps import AuthentaConfig as conf
from .manager import UserManager

import unicodedata
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
    update_by = models.CharField(conf.App.vn_update_by, blank=True, editable=False, max_length=254, null=True)
    error = models.TextField(conf.App.vn_error, blank=True, null=True)

    class Meta:
        abstract = True

    def status(self):
        return True if self.error is None else False

class Group(Group, Update):
    pass

#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
class Method(Update):
    conf_method = conf.Method
    method = models.CharField(conf_method.vn_method, choices=conf_method.choices, default=conf_method.default, help_text=conf_method.ht_method, max_length=4)
    name = models.CharField(conf_method.vn_name, help_text=conf_method.ht_name, max_length=254)
    enable = models.BooleanField(conf_method.vn_enable, default=True, help_text=conf_method.ht_enable)
    is_active = models.BooleanField(conf_method.vn_is_active, default=True)
    is_staff = models.BooleanField(conf_method.vn_is_staff, default=False)
    is_superuser = models.BooleanField(conf_method.vn_superuser, default=False)
    groups = models.ManyToManyField(Group, verbose_name=conf_method.vn_groups, blank=True)
    permissions = models.ManyToManyField(Permission, verbose_name=conf_method.vn_permissions, blank=True)

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
    method = models.CharField(conf_user.vn_method, choices=conf_user.choices_user_create_method, default=conf_user.default_method, max_length=15)
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

    def save(self, *args, **kwargs):
        self.prepare()
        super(Task, self).save(*args, **kwargs)
        logger('notice', 'local_check: {}'.format(self.local_check))
        logger('notice', 'command: {}'.format(self.command))

    def prepare(self):
        prepare = {}
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

    def can_run(self):
        if self.status != self.conf_task.status_order:
            self.error = self.conf_task.error_not_order
            self.save()
            logger('debug', 'can_run failed: {}'.format(self.error))
            return False
        try: 
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
            subprocess.check_call(self.command, shell=True)
            logger('debug', 'start_task success')
            return True
        except subprocess.CalledProcessError as error:
            self.error = error
            logger('debug', 'start_task failed: {}'.format(error))
        return False
        
