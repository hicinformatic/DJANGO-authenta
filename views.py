from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import CreateView
from django.views.generic import DetailView

from .settings import _authenta
from .forms import SignUpForm
from .models import User

class AjaxableResponseMixin:
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax() or self.kwargs['extension'] == 'json':
            return JsonResponse(form.errors, status=400)
        elif self.kwargs['extension'] == 'txt':
            data = '\n'.join(['{} | ("{}")'.format(input ,';'.join(errors)) for input,errors in form.errors.items()])
            return HttpResponse(str(data), content_type='{}; charset={}'.format(_authenta.contenttype_txt, _authenta.charset))
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax() or self.kwargs['extension'] == 'json':
            data = { 'pk': self.object.pk, }
            return JsonResponse(data)
        elif self.kwargs['extension'] == 'txt':
            data = 'pk | ("{}")'.format(self.object.pk)
            return HttpResponse(str(data), content_type='{}; charset={}'.format(_authenta.contenttype_txt, _authenta.charset))
        else:
            return resplonse

    def render_to_response(self, context):
        response = super(AjaxableResponseMixin, self).render_to_response(context)
        if self.request.is_ajax() or self.kwargs['extension'] == 'json':
            data = { 'pk': '1', }
            return JsonResponse(data)
        elif self.kwargs['extension'] == 'txt':
            data = 'pk | ("1")'
            return HttpResponse(str(data), content_type='{}; charset={}'.format(_authenta.contenttype_txt, _authenta.charset))
        else:
            return response

class SignUp(AjaxableResponseMixin, CreateView):
    form_class = SignUpForm
    template_name = 'authenta/signup.html'

class Profile(AjaxableResponseMixin, DetailView):
    model = User
    template_name = 'authenta/profile.html'