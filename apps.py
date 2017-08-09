from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import datetime, syslog, os

class AuthentaConfig(AppConfig):
    name = 'authenta'
    verbose_name = _('Authentication and Authorization')

    dir_logs = os.path.dirname(os.path.realpath(__file__))+'/logs'
    dir_task = os.path.dirname(os.path.realpath(__file__))+'/tasks'
    loglvl = 7
    locallog = True
    syslog = False

    python = '/bin/python3.6'
    binary = '/bin/bash'
    backstart =  '/bin/nohup'
    backend = '&'
    backext = '.sh'
    killscript = 3600
    host = 'localhost'
    ip = '127.0.0.1'

    vn_method = _('authentication method')
    vpn_method = _('authentication methods')
    contenttype_txt = 'text/plain'
    charset = 'utf-8'
    vsignup = True
    vsignin = True
    vsignout = True
    vprofile = True

    mail_activation = True

    uniqidentity = 'email'
    requiredfields = ['username']
    usernameuniq = True
    usernamenull = False
    emailuniq = True
    emailnull = False
    firstnamenull = True
    lastnamenull = True
    isactivedefault = False
    isstaffdefault = False
    adminnone = (None, {'fields': ('username', 'password')})
    adminpersonnal = (_('Personal info'), {'fields': ('email', 'first_name', 'last_name')})
    choices_method = (('CREATESUPERUSER', _('Create Super User')),('BACKEND', _('Back-end')),('FRONTEND', _('Front-end')))
    additional_methods = []

    ldap_activated = True
    choices_ldapscope = (('SCOPE_BASE', 'SCOPE_BASE'), ('SCOPE_ONELEVEL', 'SCOPE_ONELEVEL'), ('SCOPE_SUBTREE', 'SCOPE_SUBTREE'))
    choices_ldapversion = (('VERSION2', 'VERSION2'), ('VERSION3', 'VERSION3'))
    dir_ldapcerts = os.path.dirname(os.path.realpath(__file__))+'/ldapcerts'

    def ready(self):
        from . import signals

if hasattr(settings, 'AUTHENTA_SETTINGS'):
    for k,v in settings.AUTHENTA_SETTINGS.items():
        if hasattr(AuthentaConfig, k): setattr(AuthentaConfig, k, v)

if AuthentaConfig.ldap_activated:
    AuthentaConfig.additional_methods += (('LDAP', 'ldap'),)

def logmethis(lvl, msg):
    if AuthentaConfig.loglvl >= lvl:
        if AuthentaConfig.syslog is True:
            syslog.openlog(logoption=syslog.LOG_PID)
            syslog.syslog(lvl, '[authenta] {}'.format(msg))
            syslog.closelog()
        if AuthentaConfig.locallog is True:
            now = datetime.datetime.now()
            logfile = '{}/AuthentaConfig_{}_{}_{}.log'.format(AuthentaConfig.dir_logs, now.year, now.month, now.day)
            log = open(logfile, 'a')
            log.write("{}:{}:{}.{} - {} | [authenta] {}\n".format(now.hour, now.minute, now.second, now.microsecond, lvl, msg))
            log.close()