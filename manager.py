from django.contrib.auth.base_user import BaseUserManager

from .settings import _authenta

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, **extra_fields):
        for field in _authenta.requiredfieds:
            if field not in extra_fields:
                raise ValueError('The given'+ field +'must be set')

        user = self.model()
        for field,value in extra_fields.items():
            if field == 'email':
                email = self.normalize_email(email)
            else:
                setattr(user, field, value)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)