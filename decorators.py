from django.http import HttpResponseForbidden
from .apps import AuthentaConfig as  conf

logger = conf.logger

def howtoaccess(authorized=None):
    def _howtoaccess(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if conf.User.field_is_authenticated in authorized and request.user.is_authenticated:
                logger('debug', 'how to access: is_authenticated, id: %s' % request.user.id)
                return view_func(request, *args, **kwargs)
            if conf.api.field_is_api in authorized and request.user.has_perm('authenta.is_api'):
                logger('debug', 'how to access: is_api, id: %s' % request.user.id)
                return view_func(request, *args, **kwargs)
            if conf.robot.field_is_local_robot in authorized and request.user.has_perm('authenta.is_local_robot'):
                logger('debug', 'how to access: is_local_robot, id: %s' % request.user.id)
                return view_func(request, *args, **kwargs)
            if conf.User.field_is_staff in authorized and request.user.is_staff:
                logger('debug', 'how to access: is_staff, id: %s' % request.user.id)
                return view_func(request, *args, **kwargs)
            if request.user.is_superuser:
                logger('debug', 'how to access: is_superuser, id: %s' % request.user.id)
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return _wrapped_view
    return _howtoaccess