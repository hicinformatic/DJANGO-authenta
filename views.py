from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib import messages

from .apps import AuthentaConfig as  conf
from .decorators import howtoaccess
from .hybridmixin import (HybridDetailView, HybridTemplateView, HybridListView, HybridCreateView, HybridUpdateView, FakeModel, HybridAdminView)
from .models import (Method, Task)
from .forms import MethodAdminForm

from datetime import datetime, timedelta

#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
class MethodAdminCheck(HybridAdminView, HybridDetailView):
    template_name = conf.Method.template_name_admin_check
    model = Method
    fields_detail = conf.Method.fields_detail_check
    
    def get_context_data(self, **kwargs):
        context = super(MethodAdminCheck, self).get_context_data(**kwargs)
        method = self.object.method_get()
        messages.info(self.request, self.object.method_conf.info_method_check) if method.check() else messages.error(self.request, self.object.method_conf.error_method_check)
        return context

@method_decorator(howtoaccess(conf.Task.host_authorized+['is_superuser','is_staff']), name='dispatch')
class MethodFunction(HybridUpdateView):
    model = Method
    form_class = MethodAdminForm
    view_absolute = conf.Method.view_absolute

@method_decorator(howtoaccess(conf.Task.host_authorized+['is_superuser','is_staff']), name='dispatch')
class MethodDetail(HybridDetailView):
    model = Method
    fields_detail = ['name',]

@method_decorator(howtoaccess(conf.Task.host_authorized+['is_superuser','is_staff']), name='dispatch')
class MethodList(HybridListView):
    model = Method
    template_name = conf.App.template_list
    fields_detail = conf.Method.fields_detail
    groups = conf.Method.fields_groups
    permissins = conf.Method.fields_permissions




#████████╗ █████╗ ███████╗██╗  ██╗
#╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
#   ██║   ███████║███████╗█████╔╝ 
#   ██║   ██╔══██║╚════██║██╔═██╗ 
#   ██║   ██║  ██║███████║██║  ██╗
#   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
@method_decorator(howtoaccess(conf.Task.host_authorized+['is_superuser','is_staff']), name='dispatch')
class TaskCreate(HybridCreateView):
    model = Task
    view_absolute = conf.Task.view_absolute
    fields = conf.Task.fields_create

@method_decorator(howtoaccess(conf.Task.host_authorized+['is_superuser','is_staff']), name='dispatch')
class TaskUpdate(HybridUpdateView):
    model = Task
    view_absolute = conf.Task.view_absolute
    fields = conf.Task.fields_update

@method_decorator(howtoaccess(conf.Task.host_authorized+['is_superuser','is_staff']), name='dispatch')
class TaskDetail(HybridDetailView):
    model = Task
    fields_detail = conf.Task.fields_detail

@method_decorator(howtoaccess(conf.Task.host_authorized+['is_superuser','is_staff']), name='dispatch')
class TaskPurge(HybridTemplateView):
    template_name = conf.App.template_detail
    fields_detail = conf.Task.fields_purge
    object = FakeModel()

    def get_context_data(self, **kwargs):
        context = super(TaskPurge, self).get_context_data(**kwargs)
        delta = timezone.now()-timedelta(days=5)
        tasks = Task.objects.filter(date_update__gte=delta)
        self.object.number = tasks.count()
        tasks = tasks.values_list('pk', flat=True)
        if self.object.number > 0:
            self.object.number = self.object.number-1
            Task.objects.filter(pk__in=tasks, date_update__gte=delta).exclude(pk=list(tasks)[0]).delete()
        return context