from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import datetime, syslog, os, hashlib, sys, random, string

class OverConfig(object):
    allconf = ['Task', 'robot', 'api', 'ldap', 'Method', 'User', 'Group', 'Admin', 'ContentType', 'Extension', 'Log', 'App']
    fieldsets = ((_('Logs'), { 'classes': ('wide',), 'fields': ('update_by', 'date_create', 'date_update', 'error', ),}),)
    readonly_fields = ('update_by', 'date_create', 'date_update', 'error')

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
        dir_cache = '{}/cache'.format(dir_app)
        dir_cert = '{}/certs'.format(dir_app)
        namespace = 'authenta'
        field_update_by = 'update_by'
        vn_date_create = _('Creation date')
        vn_date_update = _('Last modification date')
        vn_update_by = _('Update by')
        ht_update_by = _('Last user who modified')
        vn_error = _('Error encountered')
        ht_error = _('Detail about the error')
        vn_method = _('create method')
        vpn_method = _('authentication methods')
        vn_task = _('# Task')
        vpn_task = _('# Tasks')
        logger = 'logger_{}'
        hybrid_list = 'object_list' 
        hybrid_fields = 'fields'
        meta = '_meta'
        meta_accepted = ['ManyToManyField', 'SimpleField']
        template_detail = 'authenta/detail.html'
        template_form = 'authenta/form.html'
        template_list = 'authenta/list.html'
        form = 'form'
        form_token = 'token'

        bg_light = '#fff'
        bg_dark = '#5d1215'
        bg_darkless = '#9b1f23'
        url_logo = 'authenta/img/your_logo_here.svg'
        url_avatar = 'authenta/img/your_avatar_here.svg'

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
        format_console = '{}{}:{}:{}.{} - {} | [{}] {}{}'
        format_code = '{}_code'
        format_color = '{}_color'
        file_open_method = 'a'
        name_file = '{}/{}_{}_{}_{}.log'
        default_color = '\033[0m'
        emerg_code = 0
        emerg_color = '\033[1;93;5;101m'
        alert_code = 1
        alert_color = '\033[1;30;5;105m'
        crit_code = 2
        crit_color = '\033[1;97;5;101m'
        error_code = 3
        error_color = '\033[1;91;5;107m'
        warning_code = 4
        warning_color = '\033[0;91m'
        notice_code = 5
        notice_color = '\033[0;97m'
        info_code = 6
        info_color = '\033[0;94m'
        debug_code = 7
        debug_color = '\033[0;30;5;100m' 

#███████╗██╗  ██╗████████╗███████╗███╗   ██╗███████╗██╗ ██████╗ ███╗   ██╗
#██╔════╝╚██╗██╔╝╚══██╔══╝██╔════╝████╗  ██║██╔════╝██║██╔═══██╗████╗  ██║
#█████╗   ╚███╔╝    ██║   █████╗  ██╔██╗ ██║███████╗██║██║   ██║██╔██╗ ██║
#██╔══╝   ██╔██╗    ██║   ██╔══╝  ██║╚██╗██║╚════██║██║██║   ██║██║╚██╗██║
#███████╗██╔╝ ██╗   ██║   ███████╗██║ ╚████║███████║██║╚██████╔╝██║ ╚████║
#╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
    class Extension(OverConfig):
        html = '.html'
        js = '.js'
        json = '.json'
        txt = '.txt'
        csv = '.csv'
        encrypted = '.enc'
        shell = '.sh'
        batch = '.bat'
        authorized = ['html', 'js', 'json', 'txt', 'csv']
        kwarg_extension = 'extension'
        default_extension = 'html'
        regex = None
        url_template = '.{}'

# ██████╗ ██████╗ ███╗   ██╗████████╗███████╗███╗   ██╗████████╗████████╗██╗   ██╗██████╗ ███████╗
#██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔════╝████╗  ██║╚══██╔══╝╚══██╔══╝╚██╗ ██╔╝██╔══██╗██╔════╝
#██║     ██║   ██║██╔██╗ ██║   ██║   █████╗  ██╔██╗ ██║   ██║      ██║    ╚████╔╝ ██████╔╝█████╗  
#██║     ██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██║╚██╗██║   ██║      ██║     ╚██╔╝  ██╔═══╝ ██╔══╝  
#╚██████╗╚██████╔╝██║ ╚████║   ██║   ███████╗██║ ╚████║   ██║      ██║      ██║   ██║     ███████╗
# ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝   ╚═╝      ╚═╝      ╚═╝   ╚═╝     ╚══════╝
    class ContentType(OverConfig):
        response = 'response_{}'
        charset = 'utf-8'
        html = 'text/html'
        js = 'application/javascript'
        json = 'application/json'
        txt = 'text/plain'
        csv = 'text/csv'
        xml = 'application/xml'
      
        csv_related_container = '[{}]'
        csv_related_separator = ' && '
        csv_related_subtemplate = '{}={}'
        csv_related_subseparator = ';;'

        txt_object_separator = '\n'
        txt_detail_template = '{}:{}'
        txt_detail_separator = ' // '
        txt_related_template = '{}:{}'
        txt_related_container = '[{}]'
        txt_related_separator = ' && '
        txt_related_subtemplate = '{}={}'
        txt_related_subseparator = ';;'

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
        login = _('Log in')

# ██████╗ ██████╗  ██████╗ ██╗   ██╗██████╗ 
#██╔════╝ ██╔══██╗██╔═══██╗██║   ██║██╔══██╗
#██║  ███╗██████╔╝██║   ██║██║   ██║██████╔╝
#██║   ██║██╔══██╗██║   ██║██║   ██║██╔═══╝ 
#╚██████╔╝██║  ██║╚██████╔╝╚██████╔╝██║     
# ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝   
    class Group(OverConfig):
        list_display = ['name', 'date_create', 'date_update']
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
        username_field = 'username'
        required_fields = []
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
        choices_user_create_method = (
            (method_createsuperuser, _('Create Super User')),
            (method_backend, _('Back-end')),
            (method_frontend, _('Front-end')),
            (method_additional, _('Additional method'))
        )
        default_method = method_frontend
        default_is_robot = False
        manager_update_by = 'manager.py'
        field_username = 'username'
        field_email = 'email'
        field_is_superuser = 'is_superuser'
        field_is_active = 'is_active'
        field_is_staff = 'is_staff'
        field_is_authenticated = 'is_authenticated'
        field_method = 'method'
        fields_groups = ['id', 'name']
        fields_permissions = ['id', '__str__']
        fields_detail = ['username', 'first_name', 'last_name', 'date_joined', 'is_staff', 'is_superuser', 'is_robot', 'groups', 'user_permissions']
        fields_list = ['username', 'date_joined']
        title_list = 'User List'
        url_detail = 'authenta:Profile'
        normalize = 'NFKC'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        vn_username = _('Username')
        vn_email = _('Email address')
        vn_is_active = _('Active')
        vn_is_staff = _('Staff')
        vn_is_robot = _('Robot')
        vn_firstname = _('Firstname')
        vn_lastname = _('Lastname')
        vn_date_joined = _('Date joined')
        vn_method = _('Create method')
        error_required_fields = _('The given field must be set: {}')
        error_is_superuser = _('Superuser must have is_superuser=True.')
        list_display = None
        filter_horizontal = ('groups', 'user_permissions', 'additional',)
        readonly_fields = ('date_joined', 'date_update', 'update_by')
        add_fieldsets = None
        key_min_length = 10
        key_max_length = 32
        template_profile = 'authenta/profile.html'
        fieldsets = (
            ((None, {'fields': ('username', 'password')})),
            ((_('Personal info'), {'fields': ('email', 'first_name', 'last_name')})),
            (_('Authentication method'), {'fields': ('method', 'additional')}),
            (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_robot', 'groups', 'user_permissions')}),
            (_('API'), {'fields': ('key', )}),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
            (_('Log informations'), {'fields': ('date_update', 'update_by')}),
        )

#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  
    class Method(OverConfig):
        login_method = 'login_method'
        verbose_name = _('Method')
        verbose_name_plural = _('Methods')
        choices = ()
        default = 'LDAP'
        port = 389
        view_admin_check = '{}_method_check'
        vn_method = _('Method')
        vn_name = _('Name')
        vn_enable = _('Enable')
        vn_port = _('Port')
        vn_tls = _('Enable TLS')
        vn_is_active = _('Will be active')
        vn_is_staff = _('Will be staff')
        vn_superuser = _('Will be superuser')
        vn_groups = _('Groups associated')
        vn_permissions = _('Permissions associated')
        vn_certificate = _('TLS Certificate')
        vn_check = _('Check')
        vn_self_signed = _('Self-signed')
        vn_field_firstname = _('Firstname correspondence')
        vn_field_lastname = _('Lastname correspondence')
        vn_field_email = _('Email correspondence')
        ht_port = _('Change the port used by the method')
        ht_tls = _('Enable or disable TLS')
        ht_certificate = _('Uploaded here the certificate to check')
        ht_method = _('Method type')
        ht_name = _('Method name')
        ht_enable = _('Enable or disable the method')
        ht_certificate_content = _('Certificate content')
        ht_certificate_path = _('Certificate path')
        ht_self_signed = _('Is the certificate self-signed?')
        ht_field = _('Automatically filled field with key map (Keep null if not used)')
        fieldsets = ((_('Globals'), { 'fields': ('method', 'name', 'port', 'enable',), }),)
        fieldsets += ((_('TLS configuration'), { 'classes': ('collapse',), 'fields': ('tls', 'certificate', 'self_signed', 'certificate_path', 'certificate_content', ),}),)
        fieldsets += ((_('Groups and permissions'), { 'classes': ('collapse',), 'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', ),}),)
        fieldsets_correspondence = ((_('Correspondences'), { 'classes': ('collapse',), 'fields': ('field_firstname', 'field_lastname', 'field_email', ),}),)
        filter_horizontal = ('groups', 'permissions')
        list_display = ('name', 'method', 'enable', 'is_active', 'is_staff', 'is_superuser', 'status','admin_button_check')
        list_filter = ('method', 'enable',)
        search_fields = ('name',)
        readonly_fields = OverConfig.readonly_fields+('certificate_path', 'certificate_content', )
        method_accepted = ['ldap',]
        fields_detail = [
            'id', 'method', 'name', 'port', 
            'tls', 'self_signed', 'certificate', 'certificate_path',
            'is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', 
            'field_firstname', 'field_lastname', 'field_email',
            'error'
        ]
        fields_groups = ['id', 'name']
        fields_permissions = ['id', '__str__']
        template_name_admin_check = 'admin/method_check.html'
        view_absolute = '{}:MethodDetail'
        error_function_invalid = _('Invalid function: %(function)s')
        info_method_check =_('The method works')
        error_method_check =_('The method does not works')

#██╗     ██████╗  █████╗ ██████╗ 
#██║     ██╔══██╗██╔══██╗██╔══██╗
#██║     ██║  ██║███████║██████╔╝
#██║     ██║  ██║██╔══██║██╔═══╝ 
#███████╗██████╔╝██║  ██║██║     
#╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝
    class ldap(OverConfig):
        activate = True
        username_field = 'username'
        name = 'LDAP'
        option = _('LDAP')
        host = 'localhost'
        scope = 'SCOPE_BASE'
        version = 'VERSION3'
        choices_scope = (('SCOPE_BASE', 'base (scope=base)'), ('SCOPE_ONELEVEL', 'onelevel (scope=onelevel)'), ('SCOPE_SUBTREE', 'subtree (scope=subtree)'))
        choices_version = (('VERSION2', 'Version 2 (LDAPv2)'), ('VERSION3', 'Version 3 (LDAPv3)'))
        certificates = '{}/{}'
        tls_cacertfile = False
        fieldsets = ((_('LDAP method'), {
            'classes': ('collapse',),
            'fields': ('ldap_host', 'ldap_define', 'ldap_scope', 'ldap_version', 'ldap_bind', 'ldap_password', 'ldap_user', 'ldap_search',),}),)
        readonly_fields = ('certificate_content', 'certificate_path', )
        #vn_username_field = _('Username field')
        #ht_username_field = _('Identification fields ')
        vn_host = _('Use hostname or IP address')
        vn_define = _('Base DN ex: dc=domain,dc=com')
        vn_version = _('Version')
        vn_scope = _('Scope')
        vn_bind = _('Root DN')
        vn_password = _('Root password')
        vn_user = _('User DN')
        vn_search = _('Search DN')
        ht_host = _('Hostname/IP')
        ht_port = _('Keep 389 to use default port')
        ht_tls = _('Use option TLS')
        ht_define = _('Base DN')
        ht_scope = _('Choice a scope. The command will be like "scope=***"')
        ht_version = _('Choice a version')
        ht_bind = _('Bind for override user permission, ex: cn=manager,dc=domain,dc=com (Keep null if not used)')
        ht_password = _('Password used by the bind')
        ht_user = _('Replace root DN by a User DN. <strong>Do not use with root DN</strong> | user DN ex : uid={{tag}},ou=my-ou,dc=domain,dc=com | Available tags: username')
        ht_search = _('search DN (LDAP filter) ex : (&(uid={{tag}})(memberof=cn=my-cn,ou=groups,dc=hub-t,dc=net)) | Available tags: username')
        err_not_exist = 'UserDoesNotExist'
        fields = ['ldap_host', 'ldap_define', 'ldap_scope', 'ldap_version', 'ldap_bind', 'ldap_password', 'ldap_user', 'ldap_search', 'ldap_tls_cacertfile']

        def dir_cert(instance, filename):
            return self.certificates.format(conf.dir_cert, instance.name)

# █████╗ ██████╗ ██╗
#██╔══██╗██╔══██╗██║
#███████║██████╔╝██║
#██╔══██║██╔═══╝ ██║
#██║  ██║██║     ██║
#╚═╝  ╚═╝╚═╝     ╚═╝
    class api(OverConfig):
        backend = 'user.authenta.api'
        field_is_api = 'is_api'
        ht_is_api = _('can access API mode')

        def key(key_max_length):
            return ''.join(random.choice('-._~+/'+string.hexdigits) for x in range(key_max_length))

#██████╗  ██████╗ ██████╗  ██████╗ ████████╗
#██╔══██╗██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝
#██████╔╝██║   ██║██████╔╝██║   ██║   ██║   
#██╔══██╗██║   ██║██╔══██╗██║   ██║   ██║   
#██║  ██║╚██████╔╝██████╔╝╚██████╔╝   ██║   
#╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝  
    class robot(OverConfig):
        username = 'robot'
        password = 'de76FBE368fAc.9--bfaAaA.af-a7_E5'
        field_is_local_robot = 'is_local_robot'
        ht_is_local_robot = _('can access Robot mode')

#████████╗ █████╗ ███████╗██╗  ██╗
#╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
#   ██║   ███████║███████╗█████╔╝ 
#   ██║   ██╔══██║╚════██║██╔═██╗ 
#   ██║   ██║  ██║███████║██║  ██╗
#   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
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
        script_can_run = 'check_os'
        script_tasks = (
            ('purge_tasks',  _('Purge tasks')),
            ('check_methods',  _('Check methods')),
            ('cache_methods',  _('Generate method caches')),
        )
        list_display = ('task', 'status')
        fieldsets = ((_('Globals'), { 'fields': ('task', 'status', 'info', 'error', 'command', 'local_check'), }),)
        fieldsets += OverConfig.fieldsets
        readonly_fields = OverConfig.readonly_fields
        readonly_fields += ('command', 'local_check')
        vn_task = _('Task')
        vn_info = _('More informations')
        vn_status = _('Status')
        vn_commmand = _('Command')
        vn_local_check = _('Local check')
        ht_task = _('Task to be done. Can be: {}'.format(', '.join([task[0] for task in script_tasks])))
        ht_info = _('Information about the task')
        ht_status = _('Can be: {}'.format(', '.join([s[0] for s in status])))
        ht_commmand = _('Command used to run the script')
        ht_local_check = _('Local check for not duplicate the task')
        error_not_order = _('Not ordered, check status')
        error_not_ready = _('Not ready, check status')
        binary = '/bin/bash'
        script_can_run_extension = '.sh'
        background =  '/bin/nohup'
        background_end = '&'
        python = '/bin/python3.6'
        python_extension = '.py'
        kill_timeout = 3600
        django_port = 8000
        update_by_local = 'local_robot'
        template_command = '{background} {python} {directory}/{task}{extension} {id} {background_end}'
        template_local_check = '{background} {binary} {directory}/{script}{script_extension} {port} {namespace} {timeout} {id} {robot} {password} {background_end}'
        fields_detail = ['task', 'info', 'status', 'error']
        fields_create = ['task', 'info']
        fields_update = ['status', 'info', 'error']
        fields_purge = ['number', ]
        view_absolute = '{}:TaskDetail'
        purge_number = 100
        purge_day = 5

for method in Config.Method.method_accepted:
    if getattr(Config, method).activate is True:
        Config.Method.choices += ((getattr(Config, method).name, getattr(Config, method).option),)
        Config.Method.fieldsets += getattr(Config, method).fieldsets

# ██████╗ ██╗   ██╗███████╗██████╗ ██████╗ ██╗██████╗ ███████╗
#██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔══██╗██║██╔══██╗██╔════╝
#██║   ██║██║   ██║█████╗  ██████╔╝██████╔╝██║██║  ██║█████╗  
#██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══██╗██║██║  ██║██╔══╝  
#╚██████╔╝ ╚████╔╝ ███████╗██║  ██║██║  ██║██║██████╔╝███████╗
# ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝
if hasattr(settings, Config.settings_override):
    settings_class = getattr(settings, Config.settings_override)
    for config in Config.allconf:
        if config in settings_class:
            for conf in settings_class[config]:
                setattr(getattr(Config, config), conf, settings_class[config][conf])
                print(settings_class[config][conf])

class AuthentaConfig(AppConfig, Config):
    name = 'authenta'

    def ready(self):
        from . import signals
        if not os.path.exists(self.App.dir_logs): 
            os.makedirs(self.App.dir_logs)
            self.logger('info', 'Create directory: %s' % self.App.dir_logs)
        if not os.path.exists(self.App.dir_cache): 
            os.makedirs(self.App.dir_cache)
            self.logger('info', 'Create directory: %s' % self.App.dir_cache)
        if not os.path.exists(self.App.dir_cert): 
            os.makedirs(self.App.dir_cert)
            self.logger('info', 'Create directory: %s' % self.App.dir_cert)
        self.logger('info', 'log level: %s' % self.Log.log_level)
        if self.User.add_fieldsets is None:
            self.User.list_display = (self.User.username_field, 'is_active', 'is_staff', 'method', 'date_joined')
        if self.User.add_fieldsets is None:
            self.User.add_fieldsets = (( None, { 'fields': (self.User.username_field, self.User.required_fields, 'password1', 'password2') }),)
        if self.Extension.regex is None:
            self.Extension.regex = '|'.join([ext for ext in self.Extension.authorized])
        self.logger('debug', 'Extensions: %s' % self.Extension.regex)
        self.logger('debug', 'Methodsl: %s' % self.Method.choices)
        self.Task.view_absolute = self.Task.view_absolute.format(self.App.namespace)
        self.Task.purge_number+=1
        self.Method.view_absolute = self.Method.view_absolute.format(self.App.namespace)

    def formatter(self):
        return { 'name': self.name, 'regex_extension': self.Extension.regex }


#██╗      ██████╗  ██████╗  ██████╗ ███████╗██████╗ 
#██║     ██╔═══██╗██╔════╝ ██╔════╝ ██╔════╝██╔══██╗
#██║     ██║   ██║██║  ███╗██║  ███╗█████╗  ██████╔╝
#██║     ██║   ██║██║   ██║██║   ██║██╔══╝  ██╔══██╗
#███████╗╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║
#╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
#0 	Emergency 	  emerg (panic)	 Système inutilisable.
#1 	Alert 	      alert          Une intervention immédiate est nécessaire.
#2 	Critical 	  crit 	         Erreur critique pour le système.
#3 	Error 	      err (error) 	 Erreur de fonctionnement.
#4 	Warning 	  warn (warning) Avertissement (une erreur peut intervenir si aucune action n'est prise).
#5 	Notice 	      notice  	     Evénement normal méritant d'être signalé.
#6 	Informational info 	         Pour information.
#7 	Debugging 	  debug 	     Message de mise au point.
    @staticmethod
    def logger(lvl, msg):
        code = getattr(AuthentaConfig.Log, AuthentaConfig.Log.format_code.format(lvl))
        if code <= AuthentaConfig.Log.log_level:
            getattr(AuthentaConfig, AuthentaConfig.App.logger.format(AuthentaConfig.Log.log_type))(lvl, code, msg)

    @staticmethod
    def logger_syslog(lvl, code, msg):
        syslog.openlog(logoption=syslog.LOG_PID)
        syslog.syslog(code, AuthentaConfig.Log.format_syslog.format(AuthentaConfig.name, msg))
        syslog.closelog()

    @staticmethod
    def logger_file(lvl, code, msg):
        now = datetime.datetime.now()
        logfile = AuthentaConfig.Log.name_file.format(AuthentaConfig.App.dir_logs, AuthentaConfig.name, now.year, now.month, now.day)
        log = open(logfile, AuthentaConfig.Log.file_open_method)
        log.write(AuthentaConfig.Log.format_file.format(now.hour, now.minute, now.second, now.microsecond, lvl, AuthentaConfig.name, msg))
        log.close()

    @staticmethod
    def logger_console(lvl, code, msg):
        color = getattr(AuthentaConfig.Log, AuthentaConfig.Log.format_color.format(lvl))
        now = datetime.datetime.now()
        print(AuthentaConfig.Log.format_console.format(color, now.hour, now.minute, now.second, now.microsecond, lvl, AuthentaConfig.name, msg, AuthentaConfig.Log.default_color))