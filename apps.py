from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from Crypto.Cipher import AES
from Crypto import Random
import datetime, syslog, os, hashlib

class OverConfig(object):
    dir_logs = os.path.dirname(os.path.realpath(__file__))+'/logs'
    dir_task = os.path.dirname(os.path.realpath(__file__))+'/tasks'
    dir_cache = os.path.dirname(os.path.realpath(__file__))+'/caches'
    loglvl = 7
    locallog = True
    syslog = False

    binary = '/bin/bash'
    binary_ext = '.sh'
    python = '/bin/python3.6'
    python_ext = '.py'
    python_start =  '/bin/nohup'
    python_end = '&'
    killscript = 3600
    host = ['localhost', 'localhost:8000']
    ip = ['127.0.0.1',]
    port = 8000
    localcallname = _('local_robot')

    vn_method = _('authentication method')
    vpn_method = _('authentication methods')
    vn_task = _('# Task')
    vpn_task = _('# Tasks')
    contenttype_txt = 'text/plain'
    charset = 'utf-8'
    vsignup = True
    vsignin = True
    vsignout = True
    vprofile = True
    vprofilelist = True
    vuser_absolute = 'authenta:Profile'
    vtask_absolute = 'authenta:TaskDetail'
    vextension = '.html'
    ext_html = 'html'
    ext_encrypted = 'enc'

    contenttype_html = 'text/html'
    contenttype_csv = 'text/csv'
    contenttype_txt = 'text/plain'
    contenttype_svg = 'image/svg+xml'
    contenttype_js = 'application/javascript'

    viewregister_accepted = ['signup', 'register']
    viewlogin_accepted = ['signin', 'login']
    viewlogout_accepted = ['signout', 'logout']
    extensions_accepted = ['html', 'json', 'txt']

    template_login = 'authenta/admin/login.html'
    template_changelist = 'authenta/admin/change_list_method.html'
    template_generatecache = 'authenta/admin/generate_cache.html'

    template_txt = '{}:{}'
    separator_txt = ' // '
    manytemplate_txt = '{}:[ {} ]'
    manyseparator_txt = ' && '
    subtemplate_txt = '{}={}'
    subseparator_txt = ';;'

    cache_methods = 'methods.json'

    mail_activation = False
    mail_from = 'from@example.com'

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
    choices_method = (('CREATESUPERUSER', _('Create Super User')),('BACKEND', _('Back-end')),('FRONTEND', _('Front-end')), ('ADDITIONAL', _('Additional method')))
    additional_methods = []
    admin_override = False

    status = (('error', _('In error')), ('order', _('Ordered')), ('ready', _('Ready')), ('start', _('Started')), ('running', _('Running')), ('complete', _('Complete')), )
    tasks = (
        ('check_os',        _('check(OS)')),
        ('cache_methods',  _('Generate cache')),
    )
    subtasks = {}
    deltas = {
        'cache_methods': 3600,
    }
    ldap_activated = True
    choices_ldapscope = (('SCOPE_BASE', 'base (scope=base)'), ('SCOPE_ONELEVEL', 'onelevel (scope=onelevel)'), ('SCOPE_SUBTREE', 'subtree (scope=subtree)'))
    choices_ldapversion = (('VERSION2', 'Version 2 (LDAPv2)'), ('VERSION3', 'Version 3 (LDAPv3)'))
    dir_ldapcerts = os.path.dirname(os.path.realpath(__file__))+'/ldapcerts'

    facebook_activated = False

    def get_regexarray(attribute):
        return '|'.join([r for r in getattr(AuthentaConfig, attribute)])

    def getRegTask():
        return '|'.join([v[0] for v in AuthentaConfig.tasks])

    def getRegExt():
        return '|'.join([e for e in AuthentaConfig.extensions_accepted])

    def encryptionKey():
        operatsys = os.uname()
        return hashlib.md5(
        '|'.join([
            operatsys.sysname,
            operatsys.nodename ,
            operatsys.release,
            operatsys.version,
            operatsys.machine,
            ''.join(os.listdir('..')),
        ]).encode('ascii')).hexdigest()

    def encryptCache(filename, plaintext):
        key = OverConfig.encryptionKey()
        plaintext = plaintext + b"\0" * (AES.block_size - len(plaintext) % AES.block_size)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = iv + cipher.encrypt(plaintext)
        with open('{}/{}{}'.format(OverConfig.dir_cache, filename, OverConfig.ext_encrypted), 'wb') as fo:
            fo.write(plaintext)

    def decryptCache(filename):
        with open('{}/{}{}'.format(OverConfig.dir_cache, filename, OverConfig.ext_encrypted), 'rb') as fo:
            ciphertext = fo.read()
            key = OverConfig.encryptionKey()
            iv = ciphertext[:AES.block_size]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = cipher.decrypt(ciphertext[AES.block_size:])
            return plaintext.rstrip(b"\0")

class AuthentaConfig(AppConfig, OverConfig):
    name = 'authenta'
    site_header = _('Django administration')
    index_title = _('Site administration (assisted by Authenta)')
    verbose_name = _('Authentication and Authorization')

    def ready(self):
        from . import check
        from . import signals
        from django.views.decorators.cache import never_cache
        from django.contrib import admin
        from django.contrib.admin import sites
        from django.urls import reverse
        from django.conf.urls import url
        
        self.contenttype_txt = '{}; charset={}'.format(AuthentaConfig.contenttype_txt, AuthentaConfig.charset)

        class AuthentaAdminSite(admin.AdminSite):
            login_template = AuthentaConfig.template_login
            site_header = AuthentaConfig.site_header
            index_title = AuthentaConfig.index_title

            @never_cache
            def login(self, request, extra_context=None):
                from django.core.urlresolvers import resolve
                current_url = resolve(request.path_info).url_name

                if request.method == 'GET' and self.has_permission(request):
                    index_path = reverse('admin:index', current_app=self.name)
                    return HttpResponseRedirect(index_path)

                from django.contrib.auth import REDIRECT_FIELD_NAME
                context = dict(self.each_context(request), title=_('Log in'), app_path=request.get_full_path(), username=request.user.get_username(), current_url=current_url)
                if (REDIRECT_FIELD_NAME not in request.GET and REDIRECT_FIELD_NAME not in request.POST): context[REDIRECT_FIELD_NAME] = reverse('admin:index', current_app=self.name)
                context.update({ 'ldap_activated' : AuthentaConfig.ldap_activated })
                context.update(extra_context or {})

                if current_url == 'ldap_login':
                    from .forms import LDAPAuthenticationForm
                    login_form = LDAPAuthenticationForm
                else:
                    from django.contrib.admin.forms import AdminAuthenticationForm
                    login_form = AdminAuthenticationForm

                defaults = {
                    'extra_context': context,
                    'authentication_form': self.login_form or login_form,
                    'template_name': self.login_template or 'admin/login.html',
                }
                request.current_app = self.name

                from django.contrib.auth.views import LoginView
                return LoginView.as_view(**defaults)(request)

            def get_urls(self):
                urlpatterns = super(AuthentaAdminSite, self).get_urls()
                urlpatterns.append(url(r'^login/ldap/$', self.login, name='ldap_login'))
                return urlpatterns

        mysite = AuthentaAdminSite()
        admin.site = mysite
        sites.site = mysite

if hasattr(settings, 'AUTHENTA_SETTINGS'):
    for k,v in settings.AUTHENTA_SETTINGS.items():
        if hasattr(AuthentaConfig, k): setattr(AuthentaConfig, k, v)

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

if AuthentaConfig.ldap_activated:
    AuthentaConfig.additional_methods += (('LDAP', 'LDAP'),)
if AuthentaConfig.facebook_activated:
    AuthentaConfig.additional_methods += (('FACEBOOK', 'Facebook'),)