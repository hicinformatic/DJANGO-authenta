from django.contrib.auth.base_user import BaseUserManager
from .apps import AuthentaConfig

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, **extra_fields):
        for field in AuthentaConfig.requiredfields:
            if field not in extra_fields: raise ValueError('The given'+ field +'must be set')
        user = self.model()
        #setattr(user, _authenta.uniqidentity, extra_fields[_authenta.uniqidentity])
        #del extra_fields[_authenta.uniqidentity]
        for field,value in extra_fields.items():
            if field == 'email': user.email = self.normalize_email(value)
            elif field == 'username': user.username = self.model.normalize_username(value)
            else: setattr(user, field, value)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', AuthentaConfig.isactivedefault)
        extra_fields.setdefault('is_staff', AuthentaConfig.isstaffdefault)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('authentication_method', 'CREATESUPERUSER')
        extra_fields.setdefault('update_by', 'manager.py')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username}, authentication_method__in=['CREATESUPERUSER', 'BACKEND', 'FRONTEND'])

    def get_by_method_additional(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username}, authentication_method='ADDITIONAL')