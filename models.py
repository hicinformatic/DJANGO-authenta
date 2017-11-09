from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
#from django.core.mail import send_mail
from django.core import serializers

from .manager import UserManager
from .apps import AuthentaConfig, logmethis

import unicodedata

if AuthentaConfig.ldap_activated: from .methods.ldap import methodLDAP

class Group(Group):
    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')

def ldap_certsdir(instance, filename):
    return '{}/{}'.format(AuthentaConfig.dir_ldapcerts, instance.name)

class Method(models.Model):
    method = models.CharField(_('Method'), choices=AuthentaConfig.additional_methods, default='LDAP', help_text=_('Authentication type'), max_length=4)
    name = models.CharField(_('Authentication Name'), help_text=_('Naming your authentication'), max_length=254)
    status = models.BooleanField(_('Activated'), default=True, help_text=_('Authentication enable or disable'))
    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff'), default=False)
    is_superuser = models.BooleanField(_('Superuser'), default=False)
    groups = models.ManyToManyField(Group, verbose_name=_('Groups associated'), blank=True)
    permissions = models.ManyToManyField(Permission, verbose_name=_('Permissions associated'), blank=True)
    date_create = models.DateTimeField(_('Creation date'), auto_now_add=True, editable=False)
    date_update = models.DateTimeField(_('Last modification date'), auto_now=True, editable=False)
    update_by = models.CharField(_('Update by'), editable=False, max_length=254)
    error = models.TextField(_('Error encountered'), blank=True, editable=False, null=True)
    obj = None

    vn_ldaphost = _('Use hostname or IP address')
    ht_ldaphost = _('Hostname/IP')
    vn_ldapport = _('Port')
    ht_ldapport = _('Keep 389 to use default port')
    vn_ldaptls = _('Option TLS')
    ht_ldaptls = _('Use option TLS')
    vn_ldapcert = _('Certificat LDAP')
    ht_ldapcert = _('Uploade here the certificat to check')
    vn_ldapdefine = _('Base DN ex: dc=domain,dc=com')
    ht_ldapdefine = _('Base DN')
    vn_ldapscope = _('Scope')
    ht_ldapscope = _('Choice a scope. The command will be like "scope=***"')
    vn_ldapversion = _('Version')
    ht_ldapversion = _('Choice a version')
    vn_ldapbind = _('Root DN')
    ht_ldapbind = _('Bind for override user permission, ex: cn=manager,dc=domain,dc=com (Keep null if not used)')
    vn_ldappassword = _('Root password')
    ht_ldappassword = _('Password used by the bind')
    vn_ldapuser = _('User DN')
    ht_ldapuser = _('Replace root DN by a User DN. <strong>Do not use with root DN</strong> | user DN ex : uid={{tag}},ou=my-ou,dc=domain,dc=com | Available tags: username,email')
    nv_ldapsearch = _('Search DN')
    ht_ldapsearch = _('search DN (LDAP filter) ex : (&(uid={{tag}})(memberof=cn=my-cn,ou=groups,dc=hub-t,dc=net)) | Available tags: username,email')
    ldap_host = models.CharField(vn_ldaphost, blank=True, default='localhost', help_text=ht_ldaphost, max_length=254, null=True)
    ldap_port = models.PositiveIntegerField(vn_ldapport, blank=True, default=389, help_text=ht_ldapport, null=True, validators=[ MinValueValidator(0), MaxValueValidator(65535)])
    ldap_tls = models.BooleanField(vn_ldaptls, default=False, help_text=ht_ldaptls)
    ldap_cert = models.FileField(vn_ldapcert, blank=True, help_text=ht_ldapcert, null=True, upload_to=ldap_certsdir)
    ldap_define = models.CharField(vn_ldapdefine, blank=True, help_text=ht_ldapdefine, max_length=254, null=True)
    ldap_scope = models.CharField(vn_ldapscope, choices=AuthentaConfig.choices_ldapscope, default='SCOPE_BASE', help_text=ht_ldapscope, max_length=14)
    ldap_version = models.CharField(ht_ldapversion, choices=AuthentaConfig.choices_ldapversion, default='VERSION3', help_text=ht_ldapversion, max_length=8)
    ldap_bind = models.CharField(vn_ldapbind, blank=True, help_text=ht_ldapbind, max_length=254, null=True)
    ldap_password = models.CharField(vn_ldappassword, blank=True, help_text=ht_ldappassword, max_length=254, null=True)
    ldap_user = models.TextField(vn_ldapuser, blank=True, help_text=ht_ldapuser, null=True)
    ldap_search = models.TextField(nv_ldapsearch, help_text=ht_ldapsearch, blank=True, null=True)

    class Meta:
        verbose_name = AuthentaConfig.vn_method
        verbose_name_plural = AuthentaConfig.vpn_method

    def __str__(self):
        return '%s | %s' % (self.method, self.name)

    def get(self, *args, **kwargs):
        logmethis(7, 'get=%s, method=%s' % (self.name, self.method))
        if self.method == 'LDAP': self.obj = methodLDAP(self)
        return self.obj

    def failed(self, error):
        logmethis(5, 'error=%s' % str(error))
        self.error = str(error)
        self.save()
        return False

    def success(self):
        self.error = None
        self.save()
        return True

    def generateCache():
        for method in AuthentaConfig.additional_methods:
            methods = Method.objects.filter(status=True, method=method[0])
            file_json = '{}/{}_{}'.format(AuthentaConfig.dir_json, method[0], AuthentaConfig.cache_methods)
            with open(file_json, 'w') as outfile:
                json_serializer = serializers.get_serializer('json')()
                json_serializer.serialize(methods, stream=outfile, indent=4)

    def save(self, *args, **kwargs):
        super(Method, self).save(*args, **kwargs)
        #self.generateCache()

class User(AbstractUser):
    username = models.CharField(_('Username'), blank=AuthentaConfig.usernamenull, max_length=254, null=AuthentaConfig.usernamenull, unique=AuthentaConfig.usernameuniq, validators=[AbstractUser.username_validator],)
    email = models.EmailField(_('Email address'), blank=AuthentaConfig.emailnull, null=AuthentaConfig.emailnull, unique=AuthentaConfig.emailuniq)
    is_active = models.BooleanField(_('Active'), default=AuthentaConfig.isactivedefault)
    is_staff = models.BooleanField(_('Staff'), default=AuthentaConfig.isstaffdefault)
    first_name = models.CharField(_('First name'), blank=AuthentaConfig.firstnamenull, max_length=30, null=AuthentaConfig.firstnamenull)
    last_name = models.CharField(_('Last name'), blank=AuthentaConfig.lastnamenull, max_length=30, null=AuthentaConfig.lastnamenull)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True, editable=False)
    date_update = models.DateTimeField(_('Last modification date'), auto_now=True, editable=False)
    update_by = models.CharField(_('Update by'), editable=False, max_length=254)
    authentication_method = models.CharField(_('Authentication method'), choices=AuthentaConfig.choices_method, default='FRONTEND', max_length=15)
    additional_method = models.ManyToManyField(Method, blank=True)

    objects = UserManager()
    USERNAME_FIELD = AuthentaConfig.uniqidentity
    REQUIRED_FIELDS = AuthentaConfig.requiredfields

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super(AbstractUser, self).clean()
        if 'username' in AuthentaConfig.requiredfields or self.username is not None:
            self.username = unicodedata.normalize('NFKC', self.username) 
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_absolute_url(self):
        return reverse(AuthentaConfig.vuser_absolute, args=[str(self.id), AuthentaConfig.vextension])

    def sendMail(self, subject, tpl_html, tpl_txt):
        htmly     = get_template(tpl_html)
        plaintext = get_template(tpl_txt)
        d = Context(self)
        subject, from_email, to = subject, AuthentaConfig.mail_from, self.email
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, AuthentaConfig.contenttype_html)
        msg.send()

from datetime import datetime, timedelta
import json, subprocess, sys, urllib.parse
class Task(models.Model):
    task = models.CharField(_('Task'), max_length=254, choices=AuthentaConfig.tasks, help_text=_('Task to be done'))
    info = models.TextField(_('Information about the task'), blank=True, null=True, help_text=_('More informations'))
    status = models.CharField(_('Status'), max_length=8, choices=AuthentaConfig.status, default='order', help_text=_('Can be: {}'.format(', '.join([s[0] for s in AuthentaConfig.status]))))
    error = models.TextField(_('Error encountered'), blank=True, null=True, help_text=_('Error returned'))
    updateby = models.CharField(_('Last update by'), blank=True, editable=False, max_length=254, null=True)
    datecreate = models.DateTimeField(_('Creation date'), auto_now_add=True, editable=False)
    dateupdate = models.DateTimeField(_('Last modification date'), auto_now=True, editable=False)

    class Meta:
        verbose_name        = AuthentaConfig.vn_task
        verbose_name_plural = AuthentaConfig.vpn_task

    def __str__(self):
        return self.get_task_display()

    @models.permalink
    def get_absolute_url(self):
        return AuthentaConfig.vtask_absolute, (), {'pk': self.id, 'extension': AuthentaConfig.vextension}

    #def get_absolute_url(self):
    #    return reverse(AuthentaConfig.vtask_absolute, args=[str(self.id), AuthentaConfig.vextension])

    def failed(self, error):
        logmethis(5, 'error=%s' % str(error))
        self.error = str(error)
        self.save()
        return False

    def success(self):
        self.error = None
        self.save()
        return True

    def save(self, *args, **kwargs):
        response = super(Task, self).save(*args, **kwargs)
        self.start_task()
        return response

    def update_by(self, request):
        self.updateby = request.user.username

    def check_task(self):
        if self.status == 'order':
            check = '{0} {1}/{2}{3} {5}'.format(
                AuthentaConfig.binary,
                AuthentaConfig.dir_task,
                AuthentaConfig.tasks[0][0], 
                AuthentaConfig.binary_ext,
                self.task,
                AuthentaConfig.killscript)
            try: 
                subprocess.check_call(check, shell=True)
                self.status = 'ready'
                return True
            except subprocess.CalledProcessError as error:
                self.error = error
        else:
            self.error = _('Not ordered, check status')
        return False


    def start_task(self):
        if self.check_task():
            bgtask = '{0} {1} {2}/{3}{4} {5} {6}'.format(
                AuthentaConfig.python_start,
                AuthentaConfig.python,
                AuthentaConfig.dir_task,
                self.task,
                AuthentaConfig.python_ext,
                self.id,
                AuthentaConfig.python_end)
            logmethis(1, bgtask)
            try:
                subprocess.check_call(bgtask, shell=True)
            except subprocess.CalledProcessError as Error:
                self.error = error
            return False