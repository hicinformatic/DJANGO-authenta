from django.shortcuts import render
from django.http import (HttpResponse, JsonResponse)
from django.middleware.csrf import get_token

from django.views.generic import (DetailView, TemplateView)
from django.views.generic.edit import (CreateView, UpdateView)
from django.views.generic.list import ListView
from django.middleware.csrf import get_token
from django.urls import reverse

from .apps import AuthentaConfig as  conf
import csv
logger = conf.logger

#███████╗ █████╗ ██╗  ██╗███████╗███╗   ███╗ ██████╗ ██████╗ ███████╗██╗     
#██╔════╝██╔══██╗██║ ██╔╝██╔════╝████╗ ████║██╔═══██╗██╔══██╗██╔════╝██║     
#█████╗  ███████║█████╔╝ █████╗  ██╔████╔██║██║   ██║██║  ██║█████╗  ██║     
#██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  ██║     
#██║     ██║  ██║██║  ██╗███████╗██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗███████╗
#╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝
class FakeModel(object):
    class _meta:
        def get_field(self):
            return FakeModel._meta()
        def get_internal_type(self):
            return None

#██╗  ██╗██╗   ██╗██████╗ ██████╗ ██╗██████╗ 
#██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██║██╔══██╗
#███████║ ╚████╔╝ ██████╔╝██████╔╝██║██║  ██║
#██╔══██║  ╚██╔╝  ██╔══██╗██╔══██╗██║██║  ██║
#██║  ██║   ██║   ██████╔╝██║  ██║██║██████╔╝
#╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝
class Hybrid(object):
    contenttype = conf.ContentType
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
        context = super(Hybrid, self).get_context_data(**kwargs)
        context[self.object_fields] = self.fields_detail
        return context

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
    def detail_json(self, obj):
        return { field: self.related_json(obj, field)
            if hasattr(obj, conf.App.meta) and obj._meta.get_field(field).get_internal_type() in self.meta_accepted else
            getattr(obj, field) for field in self.fields_detail }

    def detail_txt(self, obj):
        return conf.ContentType.txt_detail_separator.join([
            self.contenttype.txt_related_template.format(field, self.related_txt(obj, field))
            if obj._meta.get_field(field).get_internal_type() in self.meta_accepted else 
            self.contenttype.txt_detail_template.format(field, getattr(obj, field)) for field in self.fields_detail ])

    def detail_csv(self, obj):
        return [ self.related_csv(obj, field)
            if hasattr(obj, conf.App.meta) and obj._meta.get_field(field).get_internal_type() in self.meta_accepted else
            getattr(obj, field) for field in self.fields_detail ]

#██████╗ ███████╗██╗      █████╗ ████████╗███████╗██████╗ 
#██╔══██╗██╔════╝██║     ██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
#██████╔╝█████╗  ██║     ███████║   ██║   █████╗  ██║  ██║
#██╔══██╗██╔══╝  ██║     ██╔══██║   ██║   ██╔══╝  ██║  ██║
#██║  ██║███████╗███████╗██║  ██║   ██║   ███████╗██████╔╝
#╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═════╝
    def related_json(self, obj, field):
        relations = getattr(obj, field).all()
        return [{ u:getattr(rel, u)() if callable(getattr(rel, u)) else getattr(rel, u) for u in getattr(self, field) } for rel in relations] if relations else False

    def related_txt(self, obj, field):
        relations = getattr(obj, field).all()
        return self.contenttype.txt_related_container.format(self.contenttype.txt_related_separator.join([ 
            self.contenttype.txt_related_subseparator.join([
                self.contenttype.txt_related_subtemplate.format(u, str(getattr(rel, u)())) 
                if callable(getattr(rel, u)) else self.contenttype.txt_related_subtemplate.format(u, str(getattr(rel, u))) for u in getattr(self, field)
            ]) for rel in relations ])) if relations else False

    def related_csv(self,  obj, field):
        relations = getattr(obj, field).all()
        return self.contenttype.csv_related_container.format(self.contenttype.csv_related_separator.join([
            self.contenttype.csv_related_subseparator.join([
                self.contenttype.csv_related_subtemplate.format(u, getattr(rel, u)()
                if callable(getattr(rel, u)) else getattr(rel, u) ) for u in getattr(self, field)
            ]) for rel in relations ])) if relations else False

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.update_by = getattr(self.request.user, conf.User.unique_identity)
        return super(Hybrid, self).post(request)

#██╗  ██╗██╗   ██╗██████╗ ██████╗ ██╗██████╗ ███████╗ ██████╗ ██████╗ ███╗   ███╗
#██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔═══██╗██╔══██╗████╗ ████║
#███████║ ╚████╔╝ ██████╔╝██████╔╝██║██║  ██║█████╗  ██║   ██║██████╔╝██╔████╔██║
#██╔══██║  ╚██╔╝  ██╔══██╗██╔══██╗██║██║  ██║██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║
#██║  ██║   ██║   ██████╔╝██║  ██║██║██████╔╝██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║
#╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝
class HybridForm(Hybrid):
    template_name = conf.App.template_form
    token = None
    view_absolute = None

    def get_context_data(self, **kwargs):
        context = super(HybridForm, self).get_context_data(**kwargs)
        self.token = get_token(self.request)
        logger('debug', 'token: {}'.format(self.token))
        return context
  
    def get_success_url(self):
        if self.view_absolute is not None:
            print('tototo')
            return reverse(self.view_absolute, kwargs={'pk': self.object.id, self.kwarg_extension: conf.Extension.url_template.format(self.extension)})
        return super(HybridForm, self).get_success_url()
  
    def response_json(self, context):
        data = { field.html_name: field.help_text for field in context[conf.App.form] }
        data[conf.App.form_token] = self.token
        return JsonResponse(data, safe=False)
  
    def response_txt(self, context):
        data = [self.contenttype.txt_detail_template.format(field.html_name, field.help_text) for field in context[conf.App.form]]
        data.append(self.contenttype.txt_detail_template.format(conf.App.form_token, self.token))
        return HttpResponse(self.contenttype.txt_detail_separator.join(data), content_type=self.contenttype.txt)
  
    def response_csv(self, context):
        response = HttpResponse(content_type=self.contenttype.csv)
        writer = csv.writer(response)
        writer.writerow(self.fields + [conf.App.form_token])
        writer.writerow([ field.help_text for field in context[conf.App.form] ] + [ self.token ])
        return response

#██████╗ ███████╗████████╗ █████╗ ██╗██╗    ██╗   ██╗██╗███████╗██╗    ██╗
#██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██║    ██║   ██║██║██╔════╝██║    ██║
#██║  ██║█████╗     ██║   ███████║██║██║    ██║   ██║██║█████╗  ██║ █╗ ██║
#██║  ██║██╔══╝     ██║   ██╔══██║██║██║    ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
#██████╔╝███████╗   ██║   ██║  ██║██║███████╗╚████╔╝ ██║███████╗╚███╔███╔╝
#╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝ ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝
class HybridDetailView(Hybrid, DetailView):
    template_name = conf.App.template_detail

    def response_json(self, context):
        return JsonResponse(self.detail_json(self.object), safe=False)

    def response_txt(self, context):
        return HttpResponse(self.detail_txt(self.object), content_type=self.contenttype.txt)

    def response_csv(self, context):
        response = HttpResponse(content_type=self.contenttype.csv)
        writer = csv.writer(response)
        writer.writerow(self.fields_detail)
        writer.writerow(self.detail_csv(self.object))
        return response

#████████╗███████╗███╗   ███╗██████╗ ██╗      █████╗ ████████╗███████╗██╗   ██╗██╗███████╗██╗    ██╗
#╚══██╔══╝██╔════╝████╗ ████║██╔══██╗██║     ██╔══██╗╚══██╔══╝██╔════╝██║   ██║██║██╔════╝██║    ██║
#   ██║   █████╗  ██╔████╔██║██████╔╝██║     ███████║   ██║   █████╗  ██║   ██║██║█████╗  ██║ █╗ ██║
#   ██║   ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║     ██╔══██║   ██║   ██╔══╝  ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
#   ██║   ███████╗██║ ╚═╝ ██║██║     ███████╗██║  ██║   ██║   ███████╗ ╚████╔╝ ██║███████╗╚███╔███╔╝
#   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝ 
class HybridTemplateView(HybridDetailView, TemplateView):
    template_name = conf.App.template_detail

#██╗     ██╗███████╗████████╗██╗   ██╗██╗███████╗██╗    ██╗
#██║     ██║██╔════╝╚══██╔══╝██║   ██║██║██╔════╝██║    ██║
#██║     ██║███████╗   ██║   ██║   ██║██║█████╗  ██║ █╗ ██║
#██║     ██║╚════██║   ██║   ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
#███████╗██║███████║   ██║    ╚████╔╝ ██║███████╗╚███╔███╔╝
#╚══════╝╚═╝╚══════╝   ╚═╝     ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝
class HybridListView(Hybrid, ListView):
    def response_json(self, context):
        return JsonResponse([self.detail_json(obj) for obj in self.object_list], safe=False)

    def response_txt(self, context):
        return HttpResponse([self.detail_txt(obj) for obj in self.object_list], content_type=self.contenttype.txt)

    def response_csv(self, context):
        response = HttpResponse(content_type=self.contenttype.csv)
        writer = csv.writer(response)
        writer.writerow(self.fields_detail)
        for obj in self.object_list:
            writer.writerow(self.detail_csv(obj))
        return response

# ██████╗██████╗ ███████╗ █████╗ ████████╗███████╗██╗   ██╗██╗███████╗██╗    ██╗
#██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝██║   ██║██║██╔════╝██║    ██║
#██║     ██████╔╝█████╗  ███████║   ██║   █████╗  ██║   ██║██║█████╗  ██║ █╗ ██║
#██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔══╝  ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
#╚██████╗██║  ██║███████╗██║  ██║   ██║   ███████╗ ╚████╔╝ ██║███████╗╚███╔███╔╝
# ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝
class HybridCreateView(HybridForm, CreateView):
    pass

#██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██╗   ██╗██╗███████╗██╗    ██╗
#██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║   ██║██║██╔════╝██║    ██║
#██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║   ██║██║█████╗  ██║ █╗ ██║
#██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
#╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗ ╚████╔╝ ██║███████╗╚███╔███╔╝
# ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝
class HybridUpdateView(HybridForm, UpdateView):
    pass

class HybridAdminView(object):
    def get_context_data(self, **kwargs):
        from django.contrib import admin
        from django.contrib.auth import get_permission_codename
        context = super(HybridAdminView, self).get_context_data(**kwargs)
        opts = self.model._meta
        has_change_permission = self.request.user.has_perm(opts.app_label + '.' + get_permission_codename('change', opts))
        context.update({
            'title': 'Check: {}'.format(self.get_object()),
            'opts': opts,
            'app_label': opts.app_label,
            'original': self.get_object(),
            'has_change_permission': has_change_permission
        })
        context.update(admin.site.each_context(self.request))
        return context