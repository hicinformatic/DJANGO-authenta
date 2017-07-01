from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .settings import _authenta
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
       (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name')}),
        ('Permissions', {'fields': ('groups',)}),
    )
    readonly_fields = ( 'date_joined', )


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .settings import _authenta
# Register your models here.

admin.site.register(User, UserAdmin)