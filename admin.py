from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from .models import User as CustomUser
from .models import Group as CustomGroup
from .settings import _authenta

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (_authenta.uniqidentity, 'is_active', 'is_staff', 'date_joined')
    readonly_fields = ('date_joined', 'date_update')
    add_fieldsets = (( None, { 'fields': (_authenta.uniqidentity, 'password1', 'password2') }),)
    fieldsets = (
       (None, {'fields': ('username', 'password')}),
       (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
       (_('Authentication method'), {'fields': ('authentication_method',)}),
       (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
       (_('Important dates'), {'fields': ('last_login', 'date_joined', 'date_update')}),
    )

    def save_model(self, request, obj, form, change):
        obj.authentication_method = 1
        super(CustomUserAdmin, self).save_model(request, obj, form, change)

admin.site.unregister(Group)
@admin.register(CustomGroup)
class CustomGroup(GroupAdmin):
    pass
