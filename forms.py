from django import forms
from django.utils.translation import ugettext_lazy as _

from .apps import AuthentaConfig as conf
from .models import Method

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
