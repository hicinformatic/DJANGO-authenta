from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import datetime, syslog, os

class AuthentaConfig(AppConfig):
    name = 'authenta'
    site_header = _('Django administration')
    index_title = _('Site administration (assisted by Authenta)')
    verbose_name = _('Authentication and Authorization')

    dir_logs = os.path.dirname(os.path.realpath(__file__))+'/logs'
    dir_task = os.path.dirname(os.path.realpath(__file__))+'/tasks'
    dir_json = os.path.dirname(os.path.realpath(__file__))+'/jsons'
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
    vn_task = _('# Task')
    vpn_task = _('# Tasks')
    contenttype_txt = 'text/plain'
    charset = 'utf-8'
    vsignup = True
    vsignin = True
    vsignout = True
    vprofile = True
    vprofilelist = True
    
    template_login = 'authenta/admin/login.html'
    template_changelist = 'authenta/admin/change_list_method.html'
    template_generatecache = 'authenta/admin/generate_cache.html'

    mail_activation = False

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

    tasks = (
        ('TRK_check_os',        _('check(OS)')),
    )
    subtasks = {}
    deltas = {}
    status = (
        (0, _('In error')),
        (1, _('Ordered')),
        (2, _('Started')),
        (3, _('Running')),
        (4, _('Complete')),
    )

    ldap_activated = True
    choices_ldapscope = (('SCOPE_BASE', 'base (scope=base)'), ('SCOPE_ONELEVEL', 'onelevel (scope=onelevel)'), ('SCOPE_SUBTREE', 'subtree (scope=subtree)'))
    choices_ldapversion = (('VERSION2', 'Version 2 (LDAPv2)'), ('VERSION3', 'Version 3 (LDAPv3)'))
    dir_ldapcerts = os.path.dirname(os.path.realpath(__file__))+'/ldapcerts'

    facebook_activated = False

    def ready(self):
        from . import signals

        from django.views.decorators.cache import never_cache
        from django.contrib import admin
        from django.contrib.admin import sites
        from django.urls import reverse
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

            def generateCache(self, request):
                from django.shortcuts import render
                from .models import Method
                context = dict( opts=Method._meta, title='Cache')
                return render(request, AuthentaConfig.template_generatecache, context)

            def get_urls(self):
                urlpatterns = super(AuthentaAdminSite, self).get_urls()
                from django.conf.urls import url
                urlpatterns.append(url(r'^generatecache/$', self.generateCache, name='generateCache'))
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