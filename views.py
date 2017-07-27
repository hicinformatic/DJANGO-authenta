from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import CreateView
from django.views.generic import DetailView

from .settings import _authenta
from .forms import SignUpForm
from .models import User

class AjaxableFormEXT(object):
    def form_invalid(self, form):
        response = super(AjaxableFormEXT, self).form_invalid(form)
        if self.kwargs['extension'] == 'json':
            return JsonResponse(form.errors, status=400)
        elif self.kwargs['extension'] == 'txt':
            return HttpResponse(form.errors, status=400, content_type='{}'.format(_authenta.contenttype_txt, _authenta.charset))
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableFormEXT, self).form_valid(form)
        if self.kwargs['extension'] == 'json':
            data = { 'pk': self.object.pk, }
            return JsonResponse(data)
            return JsonResponse(form.errors, status=400)
        elif self.kwargs['extension'] == 'txt':
            return HttpResponse(form.errors, status=400, content_type='{}'.format(_authenta.contenttype_txt, _authenta.charset))
        else:
            return response

class SignUpEXT(AjaxableFormEXT, CreateView):
    form_class = SignUpForm
    template_name = 'authenta/signup.html'

class ProfileEXT(DetailView):
    model = User
    template_name = 'authenta/profile.html'