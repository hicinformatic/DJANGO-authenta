from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib import messages

from .apps import AuthentaConfig as  conf
from .decorators import howtoaccess
from .hybridmixin import (HybridDetailView, HybridTemplateView, HybridListView, HybridCreateView, HybridUpdateView, FakeModel, HybridAdminView)
from .models import (Method, Task)
from .forms import MethodFormFunction

from datetime import timedelta

#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
@method_decorator(howtoaccess(['is_local_robot',]), name='dispatch')
class MethodCheck(HybridDetailView):
    model = Method
    fields_detail = conf.Method.fields_detail
    groups = conf.Method.fields_groups
    permissions = conf.Method.fields_permissions

    def get_context_data(self, **kwargs):
        context = super(MethodCheck, self).get_context_data(**kwargs)
        method = self.object.method_get()
        try:
            method.check()
            if self.object.error is not None:
                self.object.error = None
                self.object.save()
        except Exception as error:
            self.object.error = error
            self.object.save()
        return context

@method_decorator(howtoaccess(['is_superuser',]), name='dispatch')
class MethodAdminCheck(HybridAdminView, MethodCheck):
    template_name = conf.Method.template_name_admin_check

    def get_context_data(self, **kwargs):
        context = super(MethodAdminCheck, self).get_context_data(**kwargs)
        if self.extension == conf.Extension.default_extension:
            if self.object.error is None: messages.info(self.request, self.object.method_conf.info_method_check) 
            else: messages.error(self.request, self.object.method_conf.error_method_check)
        context.update({ 'title': '{}: {}'.format(conf.Method.vn_check, self.get_object()), 'method_fields': getattr(conf, self.object.method.lower()).fields ,})
        return context

@method_decorator(howtoaccess(['is_local_robot',]), name='dispatch')
class MethodFunction(HybridUpdateView):
    model = Method
    form_class = MethodFormFunction
    view_absolute = conf.Method.view_absolute

@method_decorator(howtoaccess(['is_local_robot',]), name='dispatch')
class MethodDetail(HybridDetailView):
    model = Method
    fields_detail = conf.Method.fields_detail
    groups = conf.Method.fields_groups
    permissions = conf.Method.fields_permissions

    def get_context_data(self, **kwargs):
        if conf.ldap.activate:
            self.fields_detail = self.fields_detail + conf.ldap.fields
        return super(MethodDetail, self).get_context_data(**kwargs)

@method_decorator(howtoaccess(['is_local_robot',]), name='dispatch')
class MethodList(HybridListView):
    model = Method
    template_name = conf.App.template_list
    fields_detail = conf.Method.fields_detail
    groups = conf.Method.fields_groups
    permissions = conf.Method.fields_permissions

    def get_context_data(self, **kwargs):
        if conf.ldap.activate:
            self.fields_detail = self.fields_detail + conf.ldap.fields
        return super(MethodList, self).get_context_data(**kwargs)

#████████╗ █████╗ ███████╗██╗  ██╗
#╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
#   ██║   ███████║███████╗█████╔╝ 
#   ██║   ██╔══██║╚════██║██╔═██╗ 
#   ██║   ██║  ██║███████║██║  ██╗
#   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
@method_decorator(howtoaccess(['is_local_robot',]), name='dispatch')
class TaskCreate(HybridCreateView):
    model = Task
    view_absolute = conf.Task.view_absolute
    fields = conf.Task.fields_create

@method_decorator(howtoaccess(['is_local_robot',]), name='dispatch')
class TaskUpdate(HybridUpdateView):
    model = Task
    view_absolute = conf.Task.view_absolute
    fields = conf.Task.fields_update

@method_decorator(howtoaccess(['is_local_robot',]), name='dispatch')
class TaskDetail(HybridDetailView):
    model = Task
    fields_detail = conf.Task.fields_detail

@method_decorator(howtoaccess(['is_local_robot',]), name='dispatch')
class TaskPurge(HybridTemplateView):
    template_name = conf.App.template_detail
    fields_detail = conf.Task.fields_purge
    object = FakeModel()

    def get_context_data(self, **kwargs):
        context = super(TaskPurge, self).get_context_data(**kwargs)
        delta = timezone.now()-timedelta(days=conf.Task.purge_day)
        tasks = Task.objects.filter(date_update__lte=delta).order_by('-id')[:conf.Task.purge_number]
        self.object.number = tasks.count()
        tasks = tasks.values_list('pk', flat=True)
        if self.object.number > 0:
            self.object.number = self.object.number-1
            Task.objects.filter(pk__in=tasks).exclude(pk=list(tasks)[0]).delete()
        return context