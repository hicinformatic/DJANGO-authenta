#from django.contrib.auth.backends import ModelBackend
#from django.contrib.auth import get_user_model
#
#UserModel = get_user_model()
#
#class ModelBackend(ModelBackend):
#    def authenticate(self, request, username=None, password=None, **kwargs):
#        if username is None:
#            username = kwargs.get(UserModel.USERNAME_FIELD)
#        try:
#            user = UserModel._default_manager.get_by_natural_key(username)
#            if user.authentication_method == 'LDAP':
#                UserModel().set_password(password)    
#        except UserModel.DoesNotExist:
#            # Run the default password hasher once to reduce the timing
#            # difference between an existing and a non-existing user (#20760).
#            UserModel().set_password(password)
#        else:
#            if user.check_password(password) and self.user_can_authenticate(user):
#                return user