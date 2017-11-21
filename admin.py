from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group

from django.utils.safestring import mark_safe
from django.template.defaultfilters import escape
from django.core.urlresolvers import reverse

from .models import User as CustomUser
from .models import Group as CustomGroup
from .models import Method, Task
from .apps import AuthentaConfig as conf

import unicodedata

class UsernameField(forms.CharField):
    def to_python(self, value):
        username = super(UsernameField, self).to_python(value)
        return username if conf.uniqidentity != 'username' and username is None and conf.usernamenull is True else unicodedata.normalize('NFKC', username) 
UserChangeForm._meta.field_classes['username'] = UsernameField

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (conf.uniqidentity, 'is_active', 'is_staff', 'date_joined')
    filter_horizontal = ('groups', 'user_permissions', 'additional_method',)
    readonly_fields = ('date_joined', 'date_update', 'update_by')
    add_fieldsets = (( None, { 'fields': (conf.uniqidentity, conf.requiredfields, 'password1', 'password2') }),)
    fieldsets = [conf.adminnone, conf.adminpersonnal]
    fieldsets = (
       (conf.adminnone),
       (conf.adminpersonnal),
       (_('Authentication method'), {'fields': ('authentication_method', 'additional_method')}),
       (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
       (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
       (_('Log informations'), {'fields': ('date_update', 'update_by')}),
    )

    def save_model(self, request, obj, form, change):
        if obj.authentication_method is None: obj.authentication_method = 'BACKEND'
        obj.update_by = getattr(request.user, conf.uniqidentity)
        super(CustomUserAdmin, self).save_model(request, obj, form, change)

admin.site.unregister(Group)
@admin.register(CustomGroup)
class CustomGroup(GroupAdmin):
    pass

class MethodAdminForm(forms.ModelForm):
    ldap_password = forms.CharField(label=_('Root password'), required=False, widget=forms.PasswordInput(render_value=True))

def error_status(obj):
    return True if obj.error is None else False
error_status.short_description = _('In error')
error_status.boolean = True

@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
    change_list_template = conf.template_method_admin_changelist
    form = MethodAdminForm
    fieldsets = ((_('Globals'), { 'fields': ('method', 'name', 'status'), }),)
    filter_horizontal = ('groups', 'permissions')
    list_display = ('name', 'method', 'status', error_status, 'is_staff', 'is_superuser')
    list_filter = ('method', 'status',)
    search_fields = ('name',)
    readonly_fields = ('update_by', 'date_create', 'date_update', 'error')
    if conf.ldap_activated:
        fieldsets += ((_('LDAP method'), {
            'classes': ('collapse',),
            'fields': ('ldap_host', 'ldap_port', 'ldap_tls', 'ldap_cert', 'ldap_define', 'ldap_scope', 'ldap_version', 'ldap_bind', 'ldap_password', 'ldap_user', 'ldap_search',),}),
        )
    fieldsets += ((_('Groups and permissions'), {
        'classes': ('wide',),
        'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'permissions' ),}),
    )
    fieldsets += ((_('Logs'), {
        'classes': ('wide',),
        'fields': ('update_by', 'date_create', 'date_update', 'error'),}),
    )

    def save_model(self, request, obj, form, change):
        obj.update_by = getattr(request.user, conf.uniqidentity)
        super(MethodAdmin, self).save_model(request, obj, form, change)

    actions = ['checkAuthentications']
    def checkAuthentications(self, request, queryset):
        for authent in queryset:
            authent.get()
            if authent.obj.check():
                authent.success()
            else:
                link = u'<a href="%s">%s</a>' % (reverse('admin:authenta_method_change', args=(authent.id,)) , authent.name)
                try: msg_warning = msg_warning+_('<br/>%s: <span style=\'color: red\'>%s</span>') % (link, authent.error)
                except NameError: msg_warning = _('Verification failed for the following authentications:<br/>%s: <span style=\'color: red\'>%s</span>') % (link, authent.error)
        try: self.message_user(request, mark_safe(msg_warning), 'warning')
        except NameError: self.message_user(request, _('All authentications are ready'), 'success')
    checkAuthentications.short_description = _('Check the authentications status')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ( '__str__', 'info', 'status', 'date_update', )

    def save_model(self, request, obj, form, change):
        obj.update_by = getattr(request.user, conf.uniqidentity)
        super(TaskAdmin, self).save_model(request, obj, form, change)