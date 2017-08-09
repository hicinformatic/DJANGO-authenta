from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

from .apps import AuthentaConfig
from .models import User

if AuthentaConfig.vsignup:
    class SignUpForm(UserCreationForm):
        class Meta:
            model = User
            fields = (AuthentaConfig.uniqidentity, ) + tuple(AuthentaConfig.requiredfields) + ('password1', 'password2')