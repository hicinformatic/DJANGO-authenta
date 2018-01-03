from django.contrib import admin
from django.contrib.admin import sites
from django.http import HttpResponseRedirect
#from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.views.decorators.cache import never_cache
from django.http import (HttpResponse, JsonResponse)
from django.conf.urls import url

from .apps import AuthentaConfig as conf
from .forms import MethodAdminForm
from .models import (Method, Group as CustomGroup, User as CustomUser, Task)
from .views import MethodAdminCheck

class AuthentaAdminSite(admin.AdminSite):
    site_header = conf.Admin.site_header
    index_title = conf.Admin.index_title

    @never_cache
    def login(self, request, extra_context=None):
        from django.contrib.auth import REDIRECT_FIELD_NAME
        from django.core.urlresolvers import resolve
        from django.urls import reverse
        from django.contrib.auth.views import LoginView
        from django.contrib.admin.forms import AdminAuthenticationForm

        current_url = resolve(request.path_info).url_name

        if request.method == 'GET' and self.has_permission(request):
            index_path = reverse('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)

        context = dict(
            self.each_context(request),
            title=conf.Admin.login,
            app_path=request.get_full_path(),
            username=request.user.get_username(),
            current_url=current_url,
        )
        if (REDIRECT_FIELD_NAME not in request.GET and REDIRECT_FIELD_NAME not in request.POST):
            context[REDIRECT_FIELD_NAME] = reverse('admin:index', current_app=self.name)
        context.update(extra_context or {})

        from .forms import AuthenticationLDAPForm
        context.update({ 'ldap' : conf.ldap.activate })      
        login_form = AuthenticationLDAPForm if current_url == 'ldap_login' else AdminAuthenticationForm

        defaults = {
            'extra_context': context,
            'authentication_form': self.login_form or login_form,
            'template_name': self.login_template or 'admin/login.html',
        }
        request.current_app = self.name
        return LoginView.as_view(**defaults)(request)

    def get_urls(self):
        urlpatterns = super(AuthentaAdminSite, self).get_urls()
        if conf.ldap.activate:
            urlpatterns.append(url(r'^login/ldap/$', self.login, name='ldap_login'))
        return urlpatterns

mysite = AuthentaAdminSite()
admin.site = mysite
sites.site = mysite

class OverAdmin(object):
    def save_model(self, request, obj, form, change):
        if hasattr(obj, conf.User.field_method) and obj.method is None:
            obj.authentication_method = conf.User.method_backend
        obj.update_by = getattr(request.user, conf.User.username_field)
        super(OverAdmin, self).save_model(request, obj, form, change)

@admin.register(CustomUser)
class CustomUserAdmin(OverAdmin, UserAdmin):
    list_display = conf.User.list_display
    filter_horizontal = conf.User.filter_horizontal
    readonly_fields = conf.User.readonly_fields
    add_fieldsets = conf.User.add_fieldsets
    fieldsets = conf.User.fieldsets

#admin.site.unregister(Group)
@admin.register(CustomGroup)
class CustomGroup(GroupAdmin):
    pass

formatter = conf.formatter(conf)
@admin.register(Method)
class MethodAdmin(OverAdmin, admin.ModelAdmin):
    form = MethodAdminForm
    fieldsets = conf.Method.fieldsets
    filter_horizontal = conf.Method.filter_horizontal
    list_display = conf.Method.list_display
    list_filter = conf.Method.list_filter
    search_fields = conf.Method.search_fields
    readonly_fields = conf.Method.readonly_fields
    if conf.ldap.activate: readonly_fields += conf.ldap.readonly_fields
    fieldsets+=conf.Method.fieldsets_correspondence
    fieldsets+=conf.fieldsets

    def get_urls(self):
        urlpatterns = super(MethodAdmin, self).get_urls()
        urlpatterns = [
            url(r'(?P<pk>\d+)/check(\.|/)?(?P<extension>({regex_extension}))?/?$'.format(**formatter),
                self.admin_site.admin_view(MethodAdminCheck.as_view()),
                name=conf.Method.view_admin_check.format(conf.App.namespace)),
        ]+urlpatterns
        return urlpatterns

@admin.register(Task)
class TaskAdmin(OverAdmin, admin.ModelAdmin):
    fieldsets = conf.Task.fieldsets
    list_display = conf.Task.list_display
    readonly_fields = conf.Task.readonly_fields