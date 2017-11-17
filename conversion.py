from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from .apps import AuthentaConfig

class objectDict(object):
    def __init__(self, d):
        self.__dict__ = d

    class _meta:
        def get_field(self):
            return objectDict._meta()

        def get_internal_type(self):
            return None

class HybridResponseMixin:
    is_form = False
    has_token = False
    object_fields = AuthentaConfig.object_fields

    def dispatch(self, request, *args, **kwargs):
        if AuthentaConfig.kwarg_extension in kwargs: self.extension = AuthentaConfig.extensions[kwargs[AuthentaConfig.kwarg_extension]]
        return super(HybridResponseMixin, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context):
        response = super(HybridResponseMixin, self).render_to_response(context)
        if self.kwargs[AuthentaConfig.kwarg_extension] == AuthentaConfig.json_extension:
            return JsonResponse(self.jsonFields(context), safe=False)
        elif self.kwargs[AuthentaConfig.kwarg_extension] == AuthentaConfig.txt_extension:
            return HttpResponse(self.textFields(context), content_type=AuthentaConfig.contenttype_txt)
        else:
            return response

    def jsonFields(self, context):
        return [{
            f: self.jsonRelated(context, obj, f) 
                if obj._meta.get_field(f).get_internal_type() == 'ManyToManyField' else getattr(obj, f) for f in context[self.object_fields] 
            } for obj in context[AuthentaConfig.object_list]]

    def jsonRelated(self, context, obj, field):
        relations = getattr(obj, field).all()
        return [{ u:getattr(rel, u)() if callable(getattr(rel, u)) else getattr(rel, u) for u in context[field] } for rel in relations] if relations else False

    def textFields(self, context):
        return '\n'.join([
            AuthentaConfig.separator_txt.join([
                AuthentaConfig.manytemplate_txt.format(f, self.textRelated(context, obj, f)) 
                if obj._meta.get_field(f).get_internal_type() == 'ManyToManyField' else AuthentaConfig.template_txt.format(f, getattr(obj, f)) for f in context[self.object_fields] 
            ]) for obj in context[AuthentaConfig.object_list] ])

    def textRelated(self, context, obj, field):
        relations = getattr(obj, field).all()
        return AuthentaConfig.manyseparator_txt.join([ 
            AuthentaConfig.subseparator_txt.join([
                AuthentaConfig.subtemplate_txt.format(u, str(getattr(rel, u)())) 
                if callable(getattr(rel, u)) else AuthentaConfig.subtemplate_txt.format(u, str(getattr(rel, u))) for u in context[field] 
            ]) for rel in relations ] ) if relations else False


class HybridFormResponseMixin:
    extension = AuthentaConfig.extensions['json']
    
    def form_invalid(self, form):
        response = super(HybridFormResponseMixin, self).form_invalid(form)
        if self.kwargs[AuthentaConfig.kwarg_extension] == 'json':
            return JsonResponse(form.errors, status=400)
        elif self.kwargs[AuthentaConfig.kwarg_extension] == 'txt':
            data = '\n'.join([AuthentaConfig.template_txt.format(input, ';'.join(errors)) for input,errors in form.errors.items()])
            return HttpResponse(data, content_type=AuthentaConfig.contenttype_txt)
        else:
            return response

    def form_valid(self, form):
        response = super(HybridFormResponseMixin, self).form_valid(form)
        if self.kwargs[AuthentaConfig.kwarg_extension] == 'json':
            data = { 'pk': self.object.pk, }
            return JsonResponse(data)
        elif self.kwargs[AuthentaConfig.kwarg_extension] == 'txt':
            data = 'pk | ("{}")'.format(self.object.pk)
            return HttpResponse(data, content_type=AuthentaConfig.contenttype_txt)
        else:
            return response

    def render_to_response(self, context):
        response = super(HybridFormResponseMixin, self).render_to_response(context)
        if self.kwargs[AuthentaConfig.kwarg_extension] == 'json':
            data = {field.html_name: field.help_text for field in context['form']}
            if self.token: data['csrftoken'] = get_token(self.request)
            return JsonResponse(data)
        elif self.kwargs[AuthentaConfig.kwarg_extension] == 'txt':
            data = '\n'.join([AuthentaConfig.template_txt.format(field.html_name, field.help_text) for field in context['form']])
            return HttpResponse(data, content_type=AuthentaConfig.contenttype_txt)
        else:
            return response