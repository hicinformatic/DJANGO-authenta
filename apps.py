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
        dir_cert = '{}/certs'.format(dir_app)
        namespace = 'authenta'
        field_update_by = 'update_by'
        vn_date_create = _('Creation date')
        vn_date_update = _('Last modification date')
        vn_update_by = _('Update by')
        vn_error = _('Error encountered')
        vn_method = _('authentication method')
        vpn_method = _('authentication methods')
        vn_task = _('# Task')
        vpn_task = _('# Tasks')
        logger = 'logger_{}'
        
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
        authorized = ['html', 'json', 'text', 'csv']

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
        extension = None


    class Group(OverConfig):
        list_display = None
        filter_horizontal = ('permissions',)
        readonly_fields = ('date_create', 'date_update', 'update_by')
        add_fieldsets = None
        fieldsets = (
            ((None, {'fields': ('name',)})),
            (_('Permissions'), {'fields': ('permissions',)}),
            (_('Log informations'), {'fields': ('date_create', 'date_update', 'update_by')}),
        )

#██╗   ██╗███████╗███████╗██████╗ 
#██║   ██║██╔════╝██╔════╝██╔══██╗
#██║   ██║███████╗█████╗  ██████╔╝
#██║   ██║╚════██║██╔══╝  ██╔══██╗
#╚██████╔╝███████║███████╗██║  ██║
# ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
    class User(OverConfig):
        unique_identity = 'email'
        unique_username = True
        unique_email = True
        null_username = False
        null_email = False
        null_firstname = True
        null_lastname = True
        default_is_active = False
        default_is_staff = False
        method_createsuperuser = 'CREATESUPERUSER'
        method_backend = 'BACKEND'
        method_frontend = 'FRONTEND'
        method_additional = 'ADDITIONAL'
        choices_method = (
            (method_createsuperuser, _('Create Super User')),
            (method_backend, _('Back-end')),
            (method_frontend, _('Front-end')),
            (method_additional, _('Additional method'))
        )
        default_method = method_frontend
        manager_update_by = 'manager.py'
        required_fields = ['username']
        field_username = 'username'
        field_email = 'email'
        field_is_superuser = 'is_superuser'
        field_is_active = 'is_active'
        field_is_staff = 'is_staff'
        field_method = 'method'
        normalize = 'NFKC'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        vn_username = _('Username')
        vn_email = _('Email address')
        vn_is_active = _('Active')
        vn_is_staff = _('Staff')
        vn_firstname = _('Firstname')
        vn_lastname = _('Lastname')
        vn_date_joined = _('Date joined')
        vn_method = _('Authentication method')
        error_required_fields = _('The given field must be set: {}')
        error_is_superuser = _('Superuser must have is_superuser=True.')
        list_display = None
        filter_horizontal = ('groups', 'user_permissions', 'additional',)
        readonly_fields = ('date_joined', 'date_update', 'update_by')
        add_fieldsets = None
        fieldsets = (
            ((None, {'fields': ('username', 'password')})),
            ((_('Personal info'), {'fields': ('email', 'first_name', 'last_name')})),
            (_('Authentication method'), {'fields': ('method', 'additional')}),
            (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
            (_('Log informations'), {'fields': ('date_update', 'update_by')}),
        )

    class Method(OverConfig):
        verbose_name = _('Method')
        verbose_name_plural = _('Methods')

#██╗     ██████╗  █████╗ ██████╗ 
#██║     ██╔══██╗██╔══██╗██╔══██╗
#██║     ██║  ██║███████║██████╔╝
#██║     ██║  ██║██╔══██║██╔═══╝ 
#███████╗██████╔╝██║  ██║██║     
#╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝
    class ldap(OverConfig):
        host = 'localhost'
        port = 389
        scope = 'SCOPE_BASE'
        version = 'VERSION3'
        choices_scope = (('SCOPE_BASE', 'base (scope=base)'), ('SCOPE_ONELEVEL', 'onelevel (scope=onelevel)'), ('SCOPE_SUBTREE', 'subtree (scope=subtree)'))
        choices_version = (('VERSION2', 'Version 2 (LDAPv2)'), ('VERSION3', 'Version 3 (LDAPv3)'))
        certificates = '{}/{}'
        vn_ldap_host = _('Use hostname or IP address')
        vn_ldap_port = _('Port')
        vn_ldap_tls = _('Option TLS')
        vn_ldap_cert = _('Certificat LDAP')
        vn_ldap_define = _('Base DN ex: dc=domain,dc=com')
        vn_ldap_version = _('Version')
        vn_ldap_scope = _('Scope')
        vn_ldap_bind = _('Root DN')
        vn_ldap_password = _('Root password')
        vn_ldap_user = _('User DN')
        vn_ldap_search = _('Search DN')
        ht_ldap_host = _('Hostname/IP')
        ht_ldap_port = _('Keep 389 to use default port')
        ht_ldap_tls = _('Use option TLS')
        ht_ldap_cert = _('Uploade here the certificat to check')
        ht_ldap_define = _('Base DN')
        ht_ldap_scope = _('Choice a scope. The command will be like "scope=***"')
        ht_ldap_version = _('Choice a version')
        ht_ldap_bind = _('Bind for override user permission, ex: cn=manager,dc=domain,dc=com (Keep null if not used)')
        ht_ldap_password = _('Password used by the bind')
        ht_ldap_user = _('Replace root DN by a User DN. <strong>Do not use with root DN</strong> | user DN ex : uid={{tag}},ou=my-ou,dc=domain,dc=com | Available tags: username,email')
        ht_ldap_search = _('search DN (LDAP filter) ex : (&(uid={{tag}})(memberof=cn=my-cn,ou=groups,dc=hub-t,dc=net)) | Available tags: username,email')

        def dir_cert(instance, filename):
            return self.certificates.format(conf.dir_cert, instance.name)

    class Task(OverConfig):
        verbose_name = _('# Task')
        verbose_name_plural = _('# Tasks')
        status_error = 'error'
        status_order = 'order'
        status_ready = 'ready'
        status_start = 'start'
        status_running = 'running'
        status_complete = 'complete'
        status = (
            (status_error, _('In error')),
            (status_order, _('Ordered')),
            (status_ready, _('Ready')),
            (status_start, _('Started')),
            (status_running, _('Running')),
            (status_complete, _('Complete')),
        )
        script_can_start = 'can_start'
        script_tasks = (
            ('purge_tasks',  _('Purge tasks')),
            ('check_methods',  _('Check methods')),
            ('cache_methods',  _('Generate cache')),
        )
        vn_task = _('Task')
        vn_info = _('More informations')
        vn_status = _('Status')
        vn_commmand = _('Command')
        ht_task = _('Task to be done')
        ht_info = _('Information about the task')
        ht_status = _('Can be: {}'.format(', '.join([s[0] for s in status])))
        ht_commmand = _('Command used')

        binary = '/bin/bash'
        binary_extension = '.sh'
        background =  '/bin/nohup'
        background_end = '&'
        python = '/bin/python3.6'
        python_extension = '.py'
        kill_timeout = 3600
        host_authorized = ['localhost', 'localhost:8000']
        ip_authorized = ['127.0.0.1',]
        django_port = 8000
        update_by_local = 'local_robot'

class AuthentaConfig(AppConfig, Config):
    name = 'authenta'

    def ready(self):
        if self.User.add_fieldsets is None:
            self.User.list_display = (self.User.unique_identity, 'is_active', 'is_staff', 'date_joined')
        if self.User.add_fieldsets is None:
            self.User.add_fieldsets = (( None, { 'fields': (self.User.unique_identity, self.User.required_fields, 'password1', 'password2') }),)
        if self.Regex.extension is None:
            self.Regex.extension = '|'.join([ext for ext in self.Extension.authorized])

#██╗      ██████╗  ██████╗  ██████╗ ███████╗██████╗ 
#██║     ██╔═══██╗██╔════╝ ██╔════╝ ██╔════╝██╔══██╗
#██║     ██║   ██║██║  ███╗██║  ███╗█████╗  ██████╔╝
#██║     ██║   ██║██║   ██║██║   ██║██╔══╝  ██╔══██╗
#███████╗╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║
#╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
    def logger(self, lvl, msg):
        getattr(self, self.App.logger.format(self.Log.log_type))(lvl, msg)

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