from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm, UsernameField)
from django.contrib.auth import authenticate

from .apps import AuthentaConfig as conf
from .models import Method, User

from .manager import UserManager as User
import os, json


class AuthenticationLDAPForm(AuthenticationForm):
    user = None
    one_is_true = False
    ldap_errors = []

    username = UsernameField(
        label=_('LDAP Login'),
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    
    error_messages = {
        'invalid_login': _(
            "Please enter a correct LDAP login and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            setattr(self.request, conf.Method.login_method, conf.User.method_additional)
            self.user = User()
            if self.cycle(username, password):
                user = self.user.manage_additional(self.request, conf.ldap.username_field, username, password)
                if user is not None:
                    self.cleaned_data['username'] = getattr(user, user.USERNAME_FIELD)
                    self._errors = None
                    print('okkkkkk')
                    return super(AuthenticationLDAPForm, self).clean()
        return self.cleaned_data


    def cycle(self, username, password):
        from .hybridmixin import FakeModel
        cache = '{}/{}.json'.format(conf.App.dir_cache, conf.ldap.name)
        from .methods.ldap import method_ldap
        import ldap as ldap_orig

        if os.path.isfile(cache):
            methods = json.load(open(cache))
            for method in methods:
                ldap = method_ldap(FakeModel(method))
                try:
                    data = ldap.get(username, password)
                except method_ldap.UserNotFound:
                    self.add_error(None, '{} - {}'.format(method['name'], _('User Not Found')))
                except ldap_orig.INVALID_CREDENTIALS:
                    self.add_error(None, '{} - {}'.format(method['name'], _('Invalid credentials')))
                except Exception as error:
                    self.add_error(None, '{} - {}'.format(method['name'], error))
                else:
                    self.user.add_method(method['id'])
                    self.user.is_active(method['is_active'])
                    self.user.is_staff(method['is_staff'])
                    self.user.is_superuser(method['is_superuser'])
                    self.user.add_groups(method['groups'])
                    self.user.add_permissions(method['permissions'])
                    self.user.correspondence('first_name', ldap.correspondence(method['field_firstname']))
                    self.user.correspondence('last_name', ldap.correspondence(method['field_lastname']))
                    self.user.correspondence('email', ldap.correspondence(method['field_email']))
        return self.user.one_is_true

class MethodAdminForm(forms.ModelForm):
    certificate = forms.FileField(required=False)

    def clean(self):
        cleaned_data = super(MethodAdminForm, self).clean()
        if conf.ldap.activate and hasattr(cleaned_data['certificate'], 'read'):
            cleaned_data['certificate'] = cleaned_data['certificate'].read()
        return cleaned_data

class MethodFormFunction(forms.ModelForm):
    function = forms.CharField(widget=forms.Textarea, help_text=_('Provides access to the methods functions'))
    error_messages = { 'function_invalid': conf.Method.error_function_invalid, }

    class Meta:
        model = Method
        fields = ('function',)

    def clean(self):
        cleaned_data = super(MethodFormFunction, self).clean()
        method = self.instance.method_get()
        function = cleaned_data['function']
        if hasattr(method, function):
            getattr(method, function)()
        else:
            raise forms.ValidationError( self.error_messages['function_invalid'], code='function_invalid', params={'function': function}, )
        return cleaned_data
