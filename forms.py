from django import forms
from .apps import AuthentaConfig as conf

class MethodAdminAdminForm(forms.ModelForm):
    ldap_cert = forms.FileField(required=False)

    def clean(self):
        cleaned_data = super(MethodAdminAdminForm, self).clean()
        if conf.ldap.activate:
            cleaned_data['ldap_cert'] = cleaned_data['ldap_cert'].read()
        return cleaned_data