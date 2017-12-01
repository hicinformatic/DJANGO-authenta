from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token

from django.views.generic.edit import (CreateView, UpdateView)
from django.views.generic import DetailView
from django.middleware.csrf import get_token
from django.urls import reverse

from .apps import AuthentaConfig as  conf
import csv
logger = conf.logger

class FakeModel(object):
    def __init__(self, d):
        self.__dict__ = d
    class _meta:
        def get_field(self):
            return FakeModel._meta()
        def get_internal_type(self):
            return None

class Hybrid(object):
    fields_detail = []
    object_list = conf.App.hybrid_list
    object_fields = conf.App.hybrid_fields
    kwarg_extension = conf.Extension.kwarg_extension
    extension = conf.Extension.default_extension
    authorized = conf.Extension.authorized
    meta_accepted = conf.App.meta_accepted

    def dispatch(self, request, *args, **kwargs):
        if self.kwarg_extension in self.kwargs and self.kwargs[self.kwarg_extension] is not None:
            self.extension = self.kwargs[self.kwarg_extension]
        self.response = 'response_{}'.format(self.extension)
        logger('debug', self.extension)
        return super(Hybrid, self).dispatch(request)

    def get_context_data(self, **kwargs):
        logger('debug', 'method: {}, view: {}'.format(self.request.method, self.request.resolver_match.view_name))
        return super(Hybrid, self).get_context_data(**kwargs)

    def render_to_response(self, context):
        response = super(Hybrid, self).render_to_response(context)
        if self.extension in self.authorized:
            if hasattr(self, self.response):
                response = getattr(self, self.response)(context)
        return response

#██████╗ ███████╗████████╗ █████╗ ██╗██╗     
#██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██║     
#██║  ██║█████╗     ██║   ███████║██║██║     
#██║  ██║██╔══╝     ██║   ██╔══██║██║██║     
#██████╔╝███████╗   ██║   ██║  ██║██║███████╗
#╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝
    def detail_json(self, context, obj):
        return { field: self.related_json(context, field)
            if hasattr(obj, conf.App.meta) and obj._meta.get_field(field).get_internal_type() in self.meta_accepted else
            getattr(obj, field) for field in self.fields_detail }

    def detail_txt(self, context, obj):
        return conf.ContentType.txt_detail_separator.join([
            conf.ContentType.txt_related_template.format(field, self.related_txt(context, obj, field))
            if obj._meta.get_field(field).get_internal_type() in self.meta_accepted else 
            conf.ContentType.txt_detail_template.format(field, getattr(obj, field)) for field in self.fields_detail ])

    def detail_csv(self, context, obj):
        return [ self.related_csv(context, obj, field)
            if hasattr(obj, conf.App.meta) and obj._meta.get_field(field).get_internal_type() in self.meta_accepted else
            getattr(obj, field) for field in self.fields_detail ]

#██████╗ ███████╗██╗      █████╗ ████████╗███████╗██████╗ 
#██╔══██╗██╔════╝██║     ██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
#██████╔╝█████╗  ██║     ███████║   ██║   █████╗  ██║  ██║
#██╔══██╗██╔══╝  ██║     ██╔══██║   ██║   ██╔══╝  ██║  ██║
#██║  ██║███████╗███████╗██║  ██║   ██║   ███████╗██████╔╝
#╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═════╝
    def related_json(self, context, obj, field):
        relations = getattr(obj, field).all()
        return [{ u:getattr(rel, u)() if callable(getattr(rel, u)) else getattr(rel, u) for u in context[field] } for rel in relations] if relations else False

    def related_txt(self, context, obj, field):
        relations = getattr(obj, field).all()
        return conf.ContentType.txt_related_separator.join([ 
            conf.ContentType.txt_related_subseparator.join([
                conf.txt_related_subtemplate.format(u, str(getattr(rel, u)())) 
                if callable(getattr(rel, u)) else conf.txt_related_subtemplate.format(u, str(getattr(rel, u))) for u in context[field] 
            ]) for rel in relations ] ) if relations else False

    def related_json(self, context, obj, field):
        relations = getattr(obj, field).all()
        return conf.ContentType.csv_related_template.format(
            conf.ContentType.csv_related_join.join([ getattr(rel, u)() if callable(getattr(rel, u)) else getattr(rel, u) for u in context[field] for rel in relations])
            ) if relations else False

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.update_by = getattr(self.request.user, conf.User.unique_identity)
        return super(Hybrid, self).post(request)

#██╗  ██╗██╗   ██╗██████╗ ██████╗ ██╗██████╗ ██████╗ ███████╗████████╗ █████╗ ██╗██╗     
#██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██║██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██║     
#███████║ ╚████╔╝ ██████╔╝██████╔╝██║██║  ██║██║  ██║█████╗     ██║   ███████║██║██║     
#██╔══██║  ╚██╔╝  ██╔══██╗██╔══██╗██║██║  ██║██║  ██║██╔══╝     ██║   ██╔══██║██║██║     
#██║  ██║   ██║   ██████╔╝██║  ██║██║██████╔╝██████╔╝███████╗   ██║   ██║  ██║██║███████╗
#╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝
class HybridDetailView(Hybrid, DetailView):
    template_name = conf.App.template_detail

    def get_context_data(self, **kwargs):
        context = super(HybridDetailView, self).get_context_data(**kwargs)
        context[self.object_fields] = self.fields_detail
        return context

    def response_json(self, context):
        return JsonResponse(self.detail_json(context, self.object), safe=False)

    def response_txt(self, context):
        return HttpResponse(self.detail_txt(context, self.object), content_type=conf.ContentType.txt)

    def response_csv(self, context):
        response = HttpResponse(content_type=conf.ContentType.csv)
        writer = csv.writer(response)
        writer.writerow(self.fields_detail)
        writer.writerow(self.detail_csv(context, self.object))
        return response

#██╗  ██╗██╗   ██╗██████╗ ██████╗ ██╗██████╗  ██████╗██████╗ ███████╗ █████╗ ████████╗███████╗
#██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝
#███████║ ╚████╔╝ ██████╔╝██████╔╝██║██║  ██║██║     ██████╔╝█████╗  ███████║   ██║   █████╗  
#██╔══██║  ╚██╔╝  ██╔══██╗██╔══██╗██║██║  ██║██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔══╝  
#██║  ██║   ██║   ██████╔╝██║  ██║██║██████╔╝╚██████╗██║  ██║███████╗██║  ██║   ██║   ███████╗
#╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
class HybridCreateUpdateDelete(Hybrid):
    template_name = conf.App.template_form
    token = None
    view_absolute = None

    def get_context_data(self, **kwargs):
        context = super(HybridCreateUpdateDelete, self).get_context_data(**kwargs)
        self.token = get_token(self.request)
        logger('debug', 'token: {}'.format(self.token))
        return context
  
    def get_success_url(self):
        if self.view_absolute is not None:
            return reverse(self.view_absolute, kwargs={'pk': self.object.id, self.kwarg_extension: conf.Extension.url_template.format(self.extension)})
        return super(HybridCreateUpdateDelete, self).get_success_url()
  
    def response_json(self, context):
        data = { field.html_name: field.help_text for field in context[conf.App.form] }
        data[conf.App.form_token] = self.token
        return JsonResponse(data, safe=False)
  
    def response_txt(self, context):
        data = [conf.ContentType.txt_detail_template.format(field.html_name, field.help_text) for field in context[conf.App.form]]
        data.append(conf.ContentType.txt_detail_template.format(conf.App.form_token, self.token))
        return HttpResponse(conf.ContentType.txt_detail_separator.join(data), content_type=conf.ContentType.txt)
  
    def response_csv(self, context):
        response = HttpResponse(content_type=conf.ContentType.csv)
        writer = csv.writer(response)
        writer.writerow(self.fields + [conf.App.form_token])
        writer.writerow([ field.help_text for field in context[conf.App.form] ] + [ self.token ])
        return response

class HybridCreateView(HybridCreateUpdateDelete, CreateView):
    pass

class HybridUpdateView(HybridCreateUpdateDelete, UpdateView):
    pass