from django.apps import AppConfig
from .settings import _authenta

class AuthentaConfig(AppConfig):
    name = 'authenta'
    verbose_name = _authenta.adminheader
