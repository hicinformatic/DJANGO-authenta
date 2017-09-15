from .apps import AuthentaConfig
from .models import Methods


def cache(method):
    Method.objects.filter(status=True, method=method)