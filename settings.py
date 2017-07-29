from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import datetime, syslog, os

class _authenta:
    appdir = os.path.dirname(os.path.realpath(__file__))
    taskdir = os.path.dirname(os.path.realpath(__file__))+'/tasks'
    logsdir = os.path.dirname(os.path.realpath(__file__))+'/logs'
    python = '/bin/python3.6'
    binary = '/bin/bash'
    backstart =  '/bin/nohup'
    backend = '&'
    backext = '.sh'
    syslog = False
    locallog = True
    loglvl = 7
    killscript = 3600
    host = 'localhost'
    ip = '127.0.0.1'
    contenttype_txt = 'text/plain'
    charset = 'utf-8'
    adminheader = 'Authentication and Authorization'
    usernameuniq = True
    usernamenull = False
    emailuniq = True
    emailnull = False
    firstnamenull = True
    lastnamenull = True
    isactivedefault = False
    isstaffdefault = False
    uniqidentity = 'email'
    adminnone = (None, {'fields': ('email', 'password')})
    adminpersonnal = (_('Personal info'), {'fields': ('username', 'first_name', 'last_name')})
    requiredfields = ['username']
    methods = (
        (0, 'Create Super User'),
        (1, 'Back-end'),
        (2, 'Front-end'),
    )

if hasattr(settings, 'AUTHENTA_SETTINGS'):
    for k,v in settings.AUTHENTA_SETTINGS.items():
        if hasattr(_authenta, k):
            setattr(_authenta, k, v)

if not os.path.exists(_authenta.logsdir):
    os.makedirs(_authenta.logsdir)

def logmethis(lvl, msg):
    if _authenta.loglvl >= lvl:
        if _authenta.syslog is True:
            syslog.openlog(logoption=syslog.LOG_PID)
            syslog.syslog(lvl, msg)
            syslog.closelog()
        if _authenta.locallog is True:
            now = datetime.datetime.now()
            logfile = '{}/{}_{}_{}_authenta.log'.format(_authenta.logsdir, now.year, now.month, now.day)
            log = open(logfile, 'a')
            log.write('{}:{}:{}.{} - {} | {}'.format(now.hour, now.minute, now.second, now.microsecond, lvl, msg))
            log.close()