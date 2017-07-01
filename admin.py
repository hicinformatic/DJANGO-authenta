from django.contrib import admin

from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from .models import User as CustomUser
from .settings import _authenta

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (_authenta.uniqidentity, 'is_active', 'is_staff', 'date_joined')
    readonly_fields = ('date_joined', )
    add_fieldsets = (( None, { 'fields': (_authenta.uniqidentity, 'password1', 'password2') }),)

#admin.site.unregister(Group)
#Group._meta.app_label = 'authenta'
#admin.site.register(Group, GroupAdmin)