from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .apps import AuthentaConfig

class HybridResponseMixin:
    def form_invalid(self, form):
        response = super(HybridResponseMixin, self).form_invalid(form)
        if self.kwargs['extension'] == 'json':
            return JsonResponse(form.errors, status=400)
        elif self.kwargs['extension'] == 'txt':
            data = '\n'.join(['{} | ("{}")'.format(input ,';'.join(errors)) for input,errors in form.errors.items()])
            return HttpResponse(str(data), content_type='{}; charset={}'.format(AuthentaConfig.contenttype_txt, AuthentaConfig.charset))
        else:
            return response

    def form_valid(self, form):
        response = super(HybridResponseMixin, self).form_valid(form)
        if self.request.is_ajax() or self.kwargs['extension'] == 'json':
            data = { 'pk': self.object.pk, }
            return JsonResponse(data)
        elif self.kwargs['extension'] == 'txt':
            data = 'pk | ("{}")'.format(self.object.pk)
            return HttpResponse(str(data), content_type='{}; charset={}'.format(AuthentaConfig.contenttype_txt, AuthentaConfig.charset))
        else:
            return response

    def render_to_response(self, context):
        response = super(HybridResponseMixin, self).render_to_response(context)
        if self.kwargs['extension'] == 'json':
            return JsonResponse(context['object'])
        elif self.kwargs['extension'] == 'txt':
            data = '\n'.join(['{} | ("{}")'.format(key, value) for key,value in context['object'].items()])
            return HttpResponse(str(data), content_type='{}; charset={}'.format(AuthentaConfig.contenttype_txt, AuthentaConfig.charset))
        else:
            return response