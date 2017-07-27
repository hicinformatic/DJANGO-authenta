from django.contrib.auth.base_user import BaseUserManager
from .settings import _authenta

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, **extra_fields):
        for field in _authenta.requiredfields:
            if field not in extra_fields:
                raise ValueError('The given'+ field +'must be set')
        user = self.model()
        setattr(user, _authenta.uniqidentity, extra_fields[_authenta.uniqidentity])
        del extra_fields[_authenta.uniqidentity]
        for field,value in extra_fields.items():
            if field == 'email':
                user.email = self.normalize_email(email)
            else:
                setattr(user, field, value)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('authentication_method', 0)
        extra_fields.setdefault('update_by', 'manager.py')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(password, **extra_fields)