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
            #if 'HTTP_HOST' in request.META and request.META['HTTP_HOST'] in authorized:
            #    setattr(request.user, conf.User.username_field, conf.Task.update_by_local)
            #    logger('debug', 'how to access: HTTP_HOST, id: %s' % conf.Task.update_by_local)
            #    return view_func(request, *args, **kwargs)
            #if 'HTTP_X_REAL_IP' in request.META and request.META['HTTP_X_REAL_IP'] in authorized:
            #    setattr(request.user, conf.User.username_field, conf.Task.update_by_local)
            #    logger('debug', 'how to access: HTTP_X_REAL_IP, id: %s' % conf.Task.update_by_local)
            #    return view_func(request, *args, **kwargs)
            #if 'HTTP_X_FORWARDED_FOR' in request.META and request.META[ 'HTTP_X_FORWARDED_FOR'] in authorized:
            #    setattr(request.user, conf.User.username_field, conf.Task.update_by_local)
            #    logger('debug', 'how to access: HTTP_X_FORWARDED_FOR, id: %s' % conf.Task.update_by_local)
            #    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return _wrapped_view
    return _howtoaccess