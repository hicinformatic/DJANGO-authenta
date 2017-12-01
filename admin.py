from .apps import AuthentaConfig as conf
from django.contrib import admin
from django.contrib.admin import sites
#from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from .forms import MethodAdminAdminForm
from .models import (Method, Group as CustomGroup, User as CustomUser, Task)

class AuthentaAdminSite(admin.AdminSite):
    site_header = conf.Admin.site_header
    index_title = conf.Admin.index_title
mysite = AuthentaAdminSite()
admin.site = mysite
sites.site = mysite

class StatusAdmin(admin.ModelAdmin):
    def status(self, obj):
        return obj.status()
    status.boolean = True

class OverAdmin(object):
    def save_model(self, request, obj, form, change):
        if hasattr(obj, conf.User.field_method) and obj.method is None:
            obj.authentication_method = conf.User.method_backend
        obj.update_by = getattr(request.user, conf.User.unique_identity)
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
class CustomGroup(OverAdmin, GroupAdmin):
    list_display = [field.name for field in CustomGroup._meta.fields]
    filter_horizontal = conf.Group.filter_horizontal
    readonly_fields = conf.Group.readonly_fields
    fieldsets = conf.Group.fieldsets

@admin.register(Method)
class MethodAdmin(OverAdmin, StatusAdmin):
    form = MethodAdminAdminForm
    fieldsets = conf.Method.fieldsets
    filter_horizontal = conf.Method.filter_horizontal
    list_display = conf.Method.list_display
    list_filter = conf.Method.list_filter
    search_fields = conf.Method.search_fields
    readonly_fields = conf.Method.readonly_fields
    if conf.ldap.activate: readonly_fields += conf.ldap.readonly_fields

@admin.register(Task)
class TaskAdmin(OverAdmin, StatusAdmin):
    fieldsets = conf.Task.fieldsets
    list_display = conf.Task.list_display
    readonly_fields = conf.Task.readonly_fields