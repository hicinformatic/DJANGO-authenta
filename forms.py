from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm, UsernameField)

from .apps import AuthentaConfig as conf
from .models import Method

import os, json

class AuthenticationLDAPForm(AuthenticationForm):
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
        self.cycle()
        raise forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )

    def cycle(self):
        cache = '{}/{}.json'.format(conf.App.dir_cache, conf.ldap.name)
        from .methods.ldap import method_ldap

        if os.path.isfile(cache):
            methods = json.load(open(cache))
            for method in methods:
                method = method_ldap(method)
            

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
