from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.core.validators import MinValueValidator, MaxValueValidator

from .apps import AuthentaConfig 
# Create your models here.

class Update(models.Model):
    date_create = models.DateTimeField(_('Creation date'), auto_now_add=True, editable=False)
    date_update = models.DateTimeField(_('Last modification date'), auto_now=True, editable=False)
    update_by = models.CharField(_('Update by'), blank=True, editable=False, max_length=254, null=True)
    error = models.TextField(_('Error encountered'), blank=True, null=True)

    class Meta:
        abstract = True

class Method(Update):
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
