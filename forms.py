from django import forms

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
    function = forms.CharField(widget=forms.Textarea, help_text='Can access to check()')
    error_messages = {
        'function_invalid': conf.Method.error_function_invalid,
    }

    class Meta:
        model = Method
        fields = ('function',)

    def clean(self):
        self.instance.get()
        if hasattr(self.instance.obj, self.cleaned_data['function']):
            getattr(self.instance.obj, self.cleaned_data['function'])()
        else:
            raise forms.ValidationError(
                self.error_messages['function_invalid'],
                code='function_invalid',
                params={'function': 'test'},
            )
        return super(MethodFormFunction, self).clean()


from django.forms.models import modelformset_factory
from .models import Task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
TaskFormset = modelformset_factory(Task, form=TaskForm, fields='__all__', extra=1)