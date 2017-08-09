from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import datetime, syslog, os

class AuthentaConfig(AppConfig):
    name = 'authenta'
    verbose_name = _('Authentication and Authorization')

    dir_task = os.path.dirname(os.path.realpath(__file__))+'/tasks'
    dir_logs = os.path.dirname(os.path.realpath(__file__))+'/logs'
    taskdir = None
    logsdir = None
    python = '/bin/python3.6'
    binary = '/bin/bash'
    backstart =  '/bin/nohup'
    backend = '&'
    backext = '.sh'
    locallog = True
    syslog = False
    loglvl = 7
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

    usernameuniq = True
    usernamenull = False
    emailuniq = True
    emailnull = False
    firstnamenull = True
    lastnamenull = True
    isactivedefault = False
    isstaffdefault = False
    uniqidentity = 'email'
    adminnone = (None, {'fields': ('username', 'password')})
    adminpersonnal = (_('Personal info'), {'fields': ('email', 'first_name', 'last_name')})
    requiredfields = ['username']
    choices_method = (('CREATESUPERUSER', _('Create Super User')),('BACKEND', _('Back-end')),('FRONTEND', _('Front-end')))
    additional_methods = []

    ldap_activated = True
    choices_ldapscope = (('SCOPE_BASE', 'SCOPE_BASE'), ('SCOPE_ONELEVEL', 'SCOPE_ONELEVEL'), ('SCOPE_SUBTREE', 'SCOPE_SUBTREE'))
    choices_ldapversion = (('VERSION2', 'VERSION2'), ('VERSION3', 'VERSION3'))
    dir_ldapcerts = os.path.dirname(os.path.realpath(__file__))+'/ldapcerts'

    def ready(self):
        if hasattr(settings, 'AUTHENTA_SETTINGS'):
            for k,v in settings.AUTHENTA_SETTINGS.items():
                if hasattr(self, k): setattr(self, k, v)
        self.taskdir = self.path + self.dir_task
        self.logsdir = self.path + self.dir_logs
        if not os.path.exists(self.logsdir): os.makedirs(self.logsdir)
        if self.ldap_activated:
            if not os.path.exists(self.dir_ldapcerts): os.makedirs(self.dir_ldapcerts)
        from . import signals

if AuthentaConfig.ldap_activated:
    AuthentaConfig.additional_methods += (('LDAP', 'ldap'),)

def logmethis(lvl, msg):
    if AuthentaConfig.loglvl >= lvl:
        if AuthentaConfig.syslog is True:
            syslog.openlog(logoption=syslog.LOG_PID)
            syslog.syslog(lvl, msg)
            syslog.closelog()
        if AuthentaConfig.locallog is True:
            now = datetime.datetime.now()
            logfile = '{}/AuthentaConfig_{}_{}_{}.log'.format(AuthentaConfig.dir_logs, now.year, now.month, now.day)
            log = open(logfile, 'a')
            log.write("{}:{}:{}.{} - {} | {}\n".format(now.hour, now.minute, now.second, now.microsecond, lvl, msg))
            log.close()