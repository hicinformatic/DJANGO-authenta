from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

from .apps import AuthentaConfig, logmethis

class LdapBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None: username = kwargs.get(UserModel.USERNAME_FIELD)
        self.loop_authentication_ldap(username, password)
        try:
            user = UserModel._default_manager.get_by_method_additional(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def loop_authentication_ldap(self, username, password):
        return ""