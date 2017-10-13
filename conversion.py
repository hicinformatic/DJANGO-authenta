from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .apps import AuthentaConfig

class HybridFormResponseMixin:
    def form_invalid(self, form):
        response = super(HybridFormResponseMixin, self).form_invalid(form)
        if self.kwargs['extension'] == 'json':
            return JsonResponse(form.errors, status=400)
        elif self.kwargs['extension'] == 'txt':
            data = '\n'.join([AuthentaConfig.template_txt.format(input, ';'.join(errors)) for input,errors in form.errors.items()])
            return HttpResponse(data, content_type=AuthentaConfig.contenttype_txt)
        else:
            return response

    def form_valid(self, form):
        response = super(HybridFormResponseMixin, self).form_valid(form)
        if self.kwargs['extension'] == 'json':
            data = { 'pk': self.object.pk, }
            return JsonResponse(data)
        elif self.kwargs['extension'] == 'txt':
            data = 'pk | ("{}")'.format(self.object.pk)
            return HttpResponse(data, content_type=AuthentaConfig.contenttype_txt)
        else:
            return response

    def render_to_response(self, context):
        response = super(HybridFormResponseMixin, self).render_to_response(context)
        if self.kwargs['extension'] == 'json':
            return JsonResponse({field.html_name: field.help_text for field in context['form']})
        elif self.kwargs['extension'] == 'txt':
            data = '\n'.join([AuthentaConfig.template_txt.format(field.html_name, field.help_text) for field in context['form']])
            return HttpResponse(data, content_type=AuthentaConfig.contenttype_txt)
        else:
            return response

class HybridResponseMixin:
    def render_to_response(self, context):
        response = super(HybridResponseMixin, self).render_to_response(context)
        if self.kwargs['extension'] == 'json':
            return JsonResponse([{f: getattr(obj, f) for f in context['fields']} for obj in context['object_list']], safe=False)
        elif self.kwargs['extension'] == 'txt':
            data = '\n'.join([AuthentaConfig.separator_txt.join([AuthentaConfig.template_txt.format(f, getattr(obj, f)) for f in context['fields']]) for obj in context['object_list']])
            return HttpResponse(data, content_type=AuthentaConfig.contenttype_txt)
        else:
            return response