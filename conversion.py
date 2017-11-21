from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from .apps import AuthentaConfig as conf

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
    zero_flat = False
    extension = conf.html_extension
    kwarg_extension = conf.kwarg_extension

    def extension(self):
        self.extension = self.kwargs[conf.kwarg_extension]
        return self.extension

    def render_to_response(self, context):
        response = super(HybridResponseMixin, self).render_to_response(context)
        if conf.kwarg_extension in self.kwargs and self.kwargs[conf.kwarg_extension] in conf.extensions_accepted:
            self.extension = self.kwargs[conf.kwarg_extension]
        if self.extension == conf.json_extension:
            if self.is_form: return JsonResponse(self.jsonFormFields(context)[0] if self.zero_flat else self.jsonFormFields(context), safe=False)
            return JsonResponse(self.jsonFields(context)[0] if self.zero_flat else self.jsonFields(context), safe=False)
        elif self.extension == conf.txt_extension:
            if self.is_form: return HttpResponse(self.textFormFields(context), content_type=conf.contenttype_txt)
            return HttpResponse(self.textFields(context), content_type=conf.contenttype_txt)
        else:
            return response

    def jsonFormFields(self, context):
        jsonData = { field.html_name: field.help_text for field in context['form'] }
        if self.has_token: jsonData[conf.csrftoken_label] = get_token(self.request)
        return jsonData

    def jsonFields(self, context):
        return [{
            f: self.jsonRelated(context, obj, f)
            if hasattr(obj, '_meta') and obj._meta.get_field(f).get_internal_type() in conf.meta_accepted else 
            getattr(obj, f) for f in context[conf.object_fields] 
        } for obj in context[conf.object_list]]

    def jsonRelated(self, context, obj, field):
        relations = getattr(obj, field).all()
        return [{ u:getattr(rel, u)() if callable(getattr(rel, u)) else getattr(rel, u) for u in context[field] } for rel in relations] if relations else False

    def textFormFields(self, context):
        txtData = [conf.template_txt.format(field.html_name, field.help_text) for field in context['form']]
        if self.has_token: txtData.append(conf.template_txt.format(conf.csrftoken_label, get_token(self.request)))
        return conf.separator_txt.join(txtData)

    def textFields(self, context):
        return '\n'.join([
            conf.separator_txt.join([
                conf.manytemplate_txt.format(f, self.textRelated(context, obj, f)) 
                if obj._meta.get_field(f).get_internal_type() in conf.meta_accepted else 
                conf.template_txt.format(f, getattr(obj, f)) for f in context[conf.object_fields] 
            ]) for obj in context[conf.object_list] ])

    def textRelated(self, context, obj, field):
        relations = getattr(obj, field).all()
        return conf.manyseparator_txt.join([ 
            conf.subseparator_txt.join([
                conf.subtemplate_txt.format(u, str(getattr(rel, u)())) 
                if callable(getattr(rel, u)) else conf.subtemplate_txt.format(u, str(getattr(rel, u))) for u in context[field] 
            ]) for rel in relations ] ) if relations else False


class HybridFormResponseMixin:
    extension = conf.extensions['json']
    
    def form_invalid(self, form):
        response = super(HybridFormResponseMixin, self).form_invalid(form)
        if self.kwargs[conf.kwarg_extension] == 'json':
            return JsonResponse(form.errors, status=400)
        elif self.kwargs[conf.kwarg_extension] == 'txt':
            data = '\n'.join([conf.template_txt.format(input, ';'.join(errors)) for input,errors in form.errors.items()])
            return HttpResponse(data, content_type=conf.contenttype_txt)
        else:
            return response

    def form_valid(self, form):
        response = super(HybridFormResponseMixin, self).form_valid(form)
        if self.kwargs[conf.kwarg_extension] == 'json':
            data = { 'pk': self.object.pk, }
            return JsonResponse(data)
        elif self.kwargs[conf.kwarg_extension] == 'txt':
            data = 'pk | ("{}")'.format(self.object.pk)
            return HttpResponse(data, content_type=conf.contenttype_txt)
        else:
            return response

    def render_to_response(self, context):
        response = super(HybridFormResponseMixin, self).render_to_response(context)
        if self.kwargs[conf.kwarg_extension] == 'json':
            data = {field.html_name: field.help_text for field in context['form']}
            if self.token: data[conf.csrftoken_label] = get_token(self.request)
            return JsonResponse(data)
        elif self.kwargs[conf.kwarg_extension] == 'txt':
            data = '\n'.join([conf.template_txt.format(field.html_name, field.help_text) for field in context['form']])
            return HttpResponse(data, content_type=conf.contenttype_txt)
        else:
            return response