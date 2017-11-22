from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import datetime, syslog, os, hashlib, sys

class OverConfig(object):
    def __init__(self):
        if hasattr(settings, self.settings_override):
            settings_class = getattr(settings, self.settings_override)
            if hasattr(settings_class, self.__class__.__name__):
                settings_class = getattr(settings_class, self.__class__.__name__)
                for key, value in settings_class.items():
                    if hasattr(AuthentaConfig, k): setattr(AuthentaConfig, key, value)

class Config(OverConfig):
    settings_override = 'AUTHENTA'

#█████╗ ██████╗ ██████╗ 
#██╔══██╗██╔══██╗██╔══██╗
#███████║██████╔╝██████╔╝
#██╔══██║██╔═══╝ ██╔═══╝ 
#██║  ██║██║     ██║     
#╚═╝  ╚═╝╚═╝     ╚═╝ 
    class App(OverConfig):
        dir_app = os.path.dirname(os.path.realpath(__file__))
        dir_logs = '{}/logs'.format(dir_app)
        dir_task = '{}/tasks'.format(dir_app)
        dir_cache = '{}/caches'.format(dir_app)
        
#██╗      ██████╗  ██████╗ 
#██║     ██╔═══██╗██╔════╝ 
#██║     ██║   ██║██║  ███╗
#██║     ██║   ██║██║   ██║
#███████╗╚██████╔╝╚██████╔╝
#╚══════╝ ╚═════╝  ╚═════╝   
    class Log(OverConfig):
        log_type = 'console'
        log_level = 7
        format_syslog = '[{}] {}'
        format_file = '{}:{}:{}.{} - {} | [{}] {}\n'
        name_file = '{}/{}_{}_{}_{}.log'


#███╗   ██╗ █████╗ ███╗   ███╗██╗███╗   ██╗ ██████╗ 
#████╗  ██║██╔══██╗████╗ ████║██║████╗  ██║██╔════╝ 
#██╔██╗ ██║███████║██╔████╔██║██║██╔██╗ ██║██║  ███╗
#██║╚██╗██║██╔══██║██║╚██╔╝██║██║██║╚██╗██║██║   ██║
#██║ ╚████║██║  ██║██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝
#╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
    class Naming(OverConfig):
        namespace = 'authenta'
        vn_method = _('authentication method')
        vpn_method = _('authentication methods')
        vn_task = _('# Task')
        vpn_task = _('# Tasks')


#███████╗██╗  ██╗████████╗███████╗███╗   ██╗███████╗██╗ ██████╗ ███╗   ██╗
#██╔════╝╚██╗██╔╝╚══██╔══╝██╔════╝████╗  ██║██╔════╝██║██╔═══██╗████╗  ██║
#█████╗   ╚███╔╝    ██║   █████╗  ██╔██╗ ██║███████╗██║██║   ██║██╔██╗ ██║
#██╔══╝   ██╔██╗    ██║   ██╔══╝  ██║╚██╗██║╚════██║██║██║   ██║██║╚██╗██║
#███████╗██╔╝ ██╗   ██║   ███████╗██║ ╚████║███████║██║╚██████╔╝██║ ╚████║
#╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
    class Extension(OverConfig):
        html = '.html'
        json = '.json'
        text = '.txt'
        csv = '.csv'
        javascript = '.js'
        encrypted = '.enc'
        shell = '.sh'
        batch = '.bat'
        front = ['html', 'json', 'text', 'csv']

# ██████╗ ██████╗ ███╗   ██╗████████╗███████╗███╗   ██╗████████╗████████╗██╗   ██╗██████╗ ███████╗
#██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔════╝████╗  ██║╚══██╔══╝╚══██╔══╝╚██╗ ██╔╝██╔══██╗██╔════╝
#██║     ██║   ██║██╔██╗ ██║   ██║   █████╗  ██╔██╗ ██║   ██║      ██║    ╚████╔╝ ██████╔╝█████╗  
#██║     ██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██║╚██╗██║   ██║      ██║     ╚██╔╝  ██╔═══╝ ██╔══╝  
#╚██████╗╚██████╔╝██║ ╚████║   ██║   ███████╗██║ ╚████║   ██║      ██║      ██║   ██║     ███████╗
# ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝   ╚═╝      ╚═╝      ╚═╝   ╚═╝     ╚══════╝
    class ContentType(OverConfig):
        charset = 'utf-8'
        html = 'text/html'
        json = 'application/json'
        text = 'text/plain'
        csv = 'text/csv'
        javascript = 'application/javascript'

# █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗
#██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║
#███████║██║  ██║██╔████╔██║██║██╔██╗ ██║
#██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║
#██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║
#╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝
    class Admin(OverConfig):
        site_header = _('Django administration')
        index_title = _('Site administration (assisted by Authenta)')
        verbose_name = _('Authentication and Authorization')

#██████╗ ███████╗ ██████╗ ███████╗██╗  ██╗
#██╔══██╗██╔════╝██╔════╝ ██╔════╝╚██╗██╔╝
#██████╔╝█████╗  ██║  ███╗█████╗   ╚███╔╝ 
#██╔══██╗██╔══╝  ██║   ██║██╔══╝   ██╔██╗ 
#██║  ██║███████╗╚██████╔╝███████╗██╔╝ ██╗
#╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    class Regex(OverConfig):
        front = '|'

class AuthentaConfig(AppConfig, Config):
    name = 'authenta'

    def ready(self):
        self.logger(1, self.Regex.front)
        pass

    def logger(self, lvl, msg):
        getattr(self, 'logger_{}'.format(self.Log.log_type))(lvl, msg)

    def logger_syslog(self, lvl, msg):
        syslog.openlog(logoption=syslog.LOG_PID)
        syslog.syslog(lvl, self.Log.format_syslog.format(self.name, msg))
        syslog.closelog()

    def logger_file(self, lvl, msg):
        now = datetime.datetime.now()
        logfile = self.Log.name_file.format(self.App.dir_logs, self.name, now.year, now.month, now.day)
        log = open(logfile, 'a')
        log.write(self.Log.format_file.format(now.hour, now.minute, now.second, now.microsecond, lvl, self.name, msg))
        log.close()

    def logger_console(self, lvl, msg):
        now = datetime.datetime.now()
        print(self.Log.format_file.format(now.hour, now.minute, now.second, now.microsecond, lvl, self.name, msg))