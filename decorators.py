from django.http import HttpResponseForbidden
from .apps import AuthentaConfig

def howtoaccess(authorized=None):
    def _howtoaccess(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if 'is_authenticated' in authorized and request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            if 'is_staff' in authorized and request.user.is_staff:
                return view_func(request, *args, **kwargs)
            if 'is_superuser' in authorized and request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if request.META['HTTP_HOST'] in authorized:
                setattr(request.user, AuthentaConfig.uniqidentity, AuthentaConfig.localcallname)
                return view_func(request, *args, **kwargs)
            if request.META['HTTP_X_REAL_IP'] in authorized:
                setattr(request.user, AuthentaConfig.uniqidentity, AuthentaConfig.localcallname)
                return view_func(request, *args, **kwargs)
            if request.META[ 'HTTP_X_FORWARDED_FOR'] in authorized:
                setattr(request.user, AuthentaConfig.uniqidentity, AuthentaConfig.localcallname)
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return _wrapped_view
    return _howtoaccess