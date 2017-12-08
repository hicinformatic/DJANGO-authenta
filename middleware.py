from django.contrib.auth import login


from .apps import AuthentaConfig as conf
from .models import User
logger = conf.logger

from base64 import b64decode
from pprint import pprint

class ApiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            user = request.META['HTTP_AUTHORIZATION'].split(' ')
            if len(user) == 2:
                user = b64decode(user[1]).decode().split(':')
            try:
                user = User.objects.get(username=user[0], key=user[1], is_active=True)
                user.backend = conf.api.backend
                user.is_staff = False
                user.is_superuser = False
                login(request, user)
            except User.DoesNotExist:
                pass
        response = self.get_response(request)
        return response