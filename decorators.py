from django.http import HttpResponseForbidden
from functools import wraps
from .apps import AuthentaConfig

def localcall(view_func):
    def _wrapped_view(request, *args, **kwargs) :
        if request.META['HTTP_HOST'] in AuthentaConfig.host:
            return view_func(request, *args, **kwargs)
        if request.META['HTTP_X_REAL_IP'] in AuthentaConfig.ip:
            return view_func(request, *args, **kwargs)
        if request.META[ 'HTTP_X_FORWARDED_FOR'] in AuthentaConfig.ip:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return _wrapped_view

def localcalloradmin(view_func):
    def _wrapped_view(request, *args, **kwargs) :
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if request.META['HTTP_HOST'] in AuthentaConfig.host:
            return view_func(request, *args, **kwargs)
        if request.META['HTTP_X_REAL_IP'] in AuthentaConfig.ip:
            return view_func(request, *args, **kwargs)
        if request.META[ 'HTTP_X_FORWARDED_FOR'] in AuthentaConfig.ip:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return _wrapped_view

def localcalloradminorstaff(view_func):
    def _wrapped_view(request, *args, **kwargs) :
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        if request.META['HTTP_HOST'] in AuthentaConfig.host:
            return view_func(request, *args, **kwargs)
        if request.META['HTTP_X_REAL_IP'] in AuthentaConfig.ip:
            return view_func(request, *args, **kwargs)
        if request.META[ 'HTTP_X_FORWARDED_FOR'] in AuthentaConfig.ip:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return _wrapped_view

def localcalloradminorstafforlogin(view_func):
    def _wrapped_view(request, *args, **kwargs) :
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        if request.META['HTTP_HOST'] in AuthentaConfig.host:
            return view_func(request, *args, **kwargs)
        if request.META['HTTP_X_REAL_IP'] in AuthentaConfig.ip:
            return view_func(request, *args, **kwargs)
        if request.META[ 'HTTP_X_FORWARDED_FOR'] in AuthentaConfig.ip:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return _wrapped_view