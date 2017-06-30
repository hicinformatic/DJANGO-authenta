from django.conf import settings
import syslog, os

class _authenta:
    appdir = os.path.dirname(os.path.realpath(__file__))
    taskdir = os.path.dirname(os.path.realpath(__file__))+'/tasks'
    logsdir = os.path.dirname(os.path.realpath(__file__))+'/logs'
    python = '/bin/python3.5'
    binary = '/bin/bash'
    backstart =  '/bin/nohup'
    backend = '&'
    backext = '.sh'
    syslog = False
    sysloglvl = 5
    killscript = 3600
    host = 'localhost'
    ip = '127.0.0.1
    charset = 'utf-8'
    usernamefield = 'username'
    requiredfieds = ['username']
    emailuniq = False
    emailblank = False
    emailnull = True

if hasattr(settings, 'AUTHENTA_SETTINGS'):
    for k,v in settings.AUTHENTA_SETTINGS.items():
        if hasattr(_authenta, k):
            setattr(_authenta, k, v)

if not os.path.exists(_authenta.logsdir):
    os.makedirs(_authenta.directory)

def logmethis(lvl, msg):
    if conf['syslog'] is True and conf['sysloglvl'] >= lvl:
        syslog.openlog(logoption=syslog.LOG_PID)
        syslog.syslog(lvl, msg)
        syslog.closelog()