from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model

from .apps import AuthentaConfig as conf

class UserManager(BaseUserManager):
    use_in_migrations = True

    one_is_true  = False
    methods      = []
    groups       = []
    permissions  = []
    extra_fields = {}

    def _create_user(self, password, **extra_fields):
        for field in conf.User.required_fields:
            if field not in extra_fields: raise ValueError(conf.User.error_required_fields.format(field))
        user = self.model()
        for field,value in extra_fields.items():
            if field == conf.User.field_email: user.email = self.normalize_email(value)
            elif field == conf.User.field_username: user.username = self.model.normalize_username(value)
            else: setattr(user, field, value)
        user.set_password(password)
        user.save(using=self._db)
        user.additional.add(*self.methods)
        user.groups.add(*self.groups)
        user.user_permissions.add(*self.permissions)
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

    def add_method(self, method):
        self.one_is_true = True
        if method not in self.methods: self.methods.append(method)

    def add_group(self, group):
        if group not in self.groups: self.groups.append(group)

    def add_groups(self, groups):
        if groups:
            for group in groups: self.add_group(group['id'])

    def add_permission(self, permission):
        if permission not in self.permissions: self.permissions.append(permission)

    def add_permissions(self, permissions):
        if permissions:
            for permission in permissions: self.add_permission(permission['id'])

    def is_active(self, is_active):
        if is_active: self.extra_fields['is_active'] = True

    def is_staff(self, is_staff):
        if is_staff: self.extra_fields['is_staff'] = True

    def is_superuser(self, is_superuser):
        if is_superuser: self.extra_fields['is_superuser'] = True

    def correspondence(self, field, value=None):
        if value is not None and field not in self.extra_fields:
            self.extra_fields[field] = value

    def manage_additional(self, request, username_field, username, password):
        self.extra_fields['method'] = conf.User.method_additional
        from django.contrib.auth import authenticate
        user = get_user_model().objects.get(**{username_field: username})
        return self.create_user_by_method_additional(username, password) if user is None else self.update_user_by_method_additional(user)

    def create_user_by_method_additional(self, username, password):
        return get_user_model().objects.create_user(username=username, password=password, **self.extra_fields)

    def update_user_by_method_additional(self, user):
        for field,value in self.extra_fields.items():
            if field == conf.User.field_email: user.email = self.normalize_email(value)
            elif field == conf.User.field_username: user.username = self.model.normalize_username(value)
            else: setattr(user, field, value)
        user.additional = [*self.methods]
        user.groups = [*self.groups]
        user.user_permissions = [*self.permissions]
        user.save()
        return user