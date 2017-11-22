from django.contrib import admin

from .apps import AuthentaConfig as conf
from .models import Method

from django.contrib import admin
from django.contrib.admin import sites
class AuthentaAdminSite(admin.AdminSite):
    site_header = conf.Admin.site_header
    index_title = conf.Admin.index_title
mysite = AuthentaAdminSite()
admin.site = mysite
sites.site = mysite

@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
    pass