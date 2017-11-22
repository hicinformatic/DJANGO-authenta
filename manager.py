from django.contrib.auth.base_user import BaseUserManager
from .apps import AuthentaConfig as conf

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, **extra_fields):
        for field in conf.User.required_fields:
            if field not in extra_fields: raise ValueError(conf.User.error_required_fields.format(field))
        user = self.model()
        #setattr(user, _authenta.uniqidentity, extra_fields[_authenta.uniqidentity])
        #del extra_fields[_authenta.uniqidentity]
        for field,value in extra_fields.items():
            if field == conf.User.field_email: user.email = self.normalize_email(value)
            elif field == conf.User.field_username: user.username = self.model.normalize_username(value)
            else: setattr(user, field, value)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password=None, **extra_fields):
        extra_fields.setdefault(conf.User.field_is_superuser, False)
        extra_fields.setdefault(conf.User.field_is_active, conf.User.default_is_active)
        extra_fields.setdefault(conf.User.field_is_staff, conf.User.default_is_staff)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault(conf.User.field_is_active, True)
        extra_fields.setdefault(conf.User.field_is_staff, True)
        extra_fields.setdefault(conf.User.field_is_superuser, True)
        extra_fields.setdefault(conf.User.field_method, conf.User.method_createsuperuser)
        extra_fields.setdefault(conf.App.field_update_by, conf.User.manager_update_by)
        if extra_fields.get(conf.User.field_is_superuser) is not True:
            raise ValueError(conf.User.error_is_superuser)
        return self._create_user(password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username}, method__in=[conf.User.method_createsuperuser, conf.User.method_backend, conf.User.method_frontend])

    def get_by_method_additional(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username}, method=conf.User.method_additional)