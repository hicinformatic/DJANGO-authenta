from django import forms
from .apps import AuthentaConfig as conf

class MethodAdminAdminForm(forms.ModelForm):
    ldap_cert = forms.FileField(required=False)

    def clean(self):
        cleaned_data = super(MethodAdminAdminForm, self).clean()
        if conf.ldap.activate and hasattr(cleaned_data['ldap_cert'], 'read'):
            cleaned_data['ldap_cert'] = cleaned_data['ldap_cert'].read()
        return cleaned_data


from django.forms.models import modelformset_factory
from .models import Task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
TaskFormset = modelformset_factory(Task, form=TaskForm, fields='__all__', extra=1)