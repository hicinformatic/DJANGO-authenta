from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _

from .apps import AuthentaConfig
from .models import User

if AuthentaConfig.vsignup:
    class SignUpForm(UserCreationForm):
        class Meta:
            model = User
            fields = (AuthentaConfig.uniqidentity, ) + tuple(AuthentaConfig.requiredfields) + ('password1', 'password2')

if AuthentaConfig.ldap_activated:
    class LDAPAuthenticationForm(AuthenticationForm):
        username = UsernameField(
            label=_('LDAP Login'),
            max_length=254,
            widget=forms.TextInput(attrs={'autofocus': True}),
        )

