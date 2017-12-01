from django.shortcuts import render
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView

from .apps import AuthentaConfig as  conf
from .decorators import howtoaccess
from .hybridmixin import (HybridDetailView, HybridCreateView, HybridUpdateView)
from .models import Task

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