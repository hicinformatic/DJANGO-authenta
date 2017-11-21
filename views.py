from django.views.generic.edit import (CreateView, UpdateView)
from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.views import (LoginView, LogoutView)
from django.utils.decorators import method_decorator
from django.views import View

from django.middleware.csrf import get_token

from django.urls import reverse
from django.shortcuts import redirect
from django.http import Http404  

from .apps import AuthentaConfig, logmethis
from .conversion import HybridResponseMixin, objectDict
from .models import User, Method, Task
from .forms import SignUpForm, MethodFormFunction
from .decorators import howtoaccess

"""
██╗   ██╗██╗███████╗██╗    ██╗     ██████╗ ██╗   ██╗███████╗██████╗ ██████╗ ██╗██████╗ ███████╗
██║   ██║██║██╔════╝██║    ██║    ██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔══██╗██║██╔══██╗██╔════╝
██║   ██║██║█████╗  ██║ █╗ ██║    ██║   ██║██║   ██║█████╗  ██████╔╝██████╔╝██║██║  ██║█████╗  
╚██╗ ██╔╝██║██╔══╝  ██║███╗██║    ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══██╗██║██║  ██║██╔══╝  
 ╚████╔╝ ██║███████╗╚███╔███╔╝    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║██║  ██║██║██████╔╝███████╗
  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝      ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝
"""

#class UpdateView(OriginalUpdateView):
#    def dispatch(self, request, *args, **kwargs):
#        if AuthentaConfig.kwarg_extension in kwargs: self.extension = AuthentaConfig.extensions[kwargs[AuthentaConfig.kwarg_extension]]
#        return super(UpdateView, self).dispatch(request, *args, **kwargs)

"""
██╗   ██╗███████╗███████╗██████╗ 
██║   ██║██╔════╝██╔════╝██╔══██╗
██║   ██║███████╗█████╗  ██████╔╝
██║   ██║╚════██║██╔══╝  ██╔══██╗
╚██████╔╝███████║███████╗██║  ██║
 ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
"""

if AuthentaConfig.vsignup:
    class SignUp(HybridResponseMixin, CreateView):
        is_form = True
        has_token = True
        form_class = SignUpForm
        template_name = AuthentaConfig.template_form

        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated():
                if AuthentaConfig.vprofile: 
                    return redirect(
                        reverse(
                            AuthentaConfig.vuser_absolute,
                            kwargs={'pk': request.user.id, AuthentaConfig.kwarg_extension: AuthentaConfig.extensions[self.extension]})
                        )
                raise Http404
            return super(SignUp, self).dispatch(request, *args, **kwargs)

        def get_success_url(self):
            return reverse(AuthentaConfig.vuser_absolute, kwargs={'pk': self.object.id, AuthentaConfig.kwarg_extension: AuthentaConfig.extensions[self.extension]})

if AuthentaConfig.vsignin:
    class SignIn(HybridResponseMixin, LoginView):
        is_form = True
        has_token = True
        template_name = AuthentaConfig.template_form

        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated():
                if AuthentaConfig.vprofile: 
                    return redirect(
                        reverse(
                            AuthentaConfig.vuser_absolute,
                            kwargs={
                                'pk': request.user.id,
                                AuthentaConfig.kwarg_extension: AuthentaConfig.extensions[self.extension]
                            })
                        )
                raise Http404
            return super(SignIn, self).dispatch(request, *args, **kwargs)

        def get_success_url(self):
            return reverse(AuthentaConfig.vuser_absolute, kwargs={'pk': self.object.id, AuthentaConfig.kwarg_extension: AuthentaConfig.extensions[self.extension]})
            #if self.request.user.is_authenticated:
            #    return reverse('authenta:Profile', args=[str(self.request.user.id), '.html'])

if AuthentaConfig.vsignout:
    class SignOut(HybridResponseMixin, LogoutView):
        template_name = 'authenta/profile.html'

        def get_context_data(self, **kwargs):
            context = super(SignOut, self).get_context_data(**kwargs)
            context[AuthentaConfig.object_fields] = ['status', ]
            context[AuthentaConfig.object_list] = [objectDict({ 'status': 'disconnected' })]
            return context

if AuthentaConfig.vprofilelist:
    class ProfileList(HybridResponseMixin, ListView):
        model = User
        template_name = 'authenta/profilelist.html'
        paginate_by = 26
        slug = None

        def get_context_data(self, **kwargs):
            context = super(ProfileList, self).get_context_data(**kwargs)
            context[AuthentaConfig.object_fields] = ['id', 'username']
            return context

if AuthentaConfig.vprofile:
    class Profile(HybridResponseMixin, DetailView):
        model = User
        template_name = 'authenta/profile.html'

        def get_context_data(self, **kwargs):
            context = super(Profile, self).get_context_data(**kwargs)
            context[AuthentaConfig.object_fields] = ['username', ]
            context[AuthentaConfig.object_list] = [self.object]
            return context


"""
███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  
"""

@method_decorator(howtoaccess(AuthentaConfig.host+['is_superuser','is_staff']), name='dispatch')
class MethodList(HybridResponseMixin, ListView):
    model = Method
    template_name = 'authenta/method/list.html'
    slug = id

    def get_context_data(self, **kwargs):
        context = super(MethodList, self).get_context_data(**kwargs)
        context[AuthentaConfig.object_fields] = ['id', 'method', 'name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'permissions']
        context['groups'] = ['id', 'name']
        context['permissions'] = ['id', '__str__']
        return context

@method_decorator(howtoaccess(AuthentaConfig.host+['is_superuser','is_staff']), name='dispatch')
class MethodDetail(HybridResponseMixin, DetailView):
    model = Method
    template_name = AuthentaConfig.template_detail

    def get_context_data(self, **kwargs):
        context = super(MethodDetail, self).get_context_data(**kwargs)
        context[AuthentaConfig.object_fields] = ['id', 'name', 'status', 'error']
        context[AuthentaConfig.object_list] = [self.object]
        return context

@method_decorator(howtoaccess(AuthentaConfig.host+['is_superuser','is_staff']), name='dispatch')
class MethodFunction(HybridResponseMixin, UpdateView):
    is_form = True
    has_token = True
    model = Method
    template_name = AuthentaConfig.template_form
    form_class = MethodFormFunction
    slug = id

    def get_success_url(self):
        return reverse (AuthentaConfig.vmethod_absolute, kwargs={'pk': self.object.id, AuthentaConfig.kwarg_extension: AuthentaConfig.extensions[self.extension]})

"""
████████╗ █████╗ ███████╗██╗  ██╗
╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
   ██║   ███████║███████╗█████╔╝ 
   ██║   ██╔══██║╚════██║██╔═██╗ 
   ██║   ██║  ██║███████║██║  ██╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""

@method_decorator(howtoaccess(AuthentaConfig.host+['is_superuser','is_staff']), name='dispatch')
class TaskCreate(HybridResponseMixin, CreateView):
    is_form = True
    has_token = True
    model = Task
    fields = ['task', 'info']
    template_name = AuthentaConfig.template_form

    def get_success_url(self):
        return reverse (AuthentaConfig.vtask_absolute, kwargs={'pk': self.object.id, AuthentaConfig.kwarg_extension: self.extension})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.update_by = getattr(self.request.user, AuthentaConfig.uniqidentity)
        return self.form_valid(form)  if form.is_valid() else self.form_invalid(form)

@method_decorator(howtoaccess(AuthentaConfig.host+['is_superuser','is_staff']), name='dispatch')
class TaskDetail(HybridResponseMixin, DetailView):
    model = Task
    template_name = AuthentaConfig.template_detail

    def get_context_data(self, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)
        context[AuthentaConfig.object_fields] = ['task', 'info', 'status', 'error']
        context[AuthentaConfig.object_list] = [self.object]
        return context

@method_decorator(howtoaccess(AuthentaConfig.host+['is_superuser','is_staff']), name='dispatch')
class TaskUpdate(HybridResponseMixin, UpdateView):
    model = Task
    fields = ['task', 'status', 'info', 'error']
    template_name = AuthentaConfig.template_form
    token = True
    is_form = True

    def form_valid(self, form):
        self.object.update_by = getattr(self.request.user, AuthentaConfig.uniqidentity)
        return super(TaskUpdate, self).form_valid(form)

@method_decorator(howtoaccess(AuthentaConfig.host+['is_superuser','is_staff']), name='dispatch')
class TaskPurge(HybridResponseMixin, TemplateView):
    template_name = AuthentaConfig.template_detail

    def get_context_data(self, **kwargs):
        context = super(TaskPurge, self).get_context_data(**kwargs)
        tasks = Task.objects.all().order_by('-id')[1000:0].values_list('id', flat=True)
        tasks.first()
        number = tasks.count()
        Task.objects.exclude(pk__in=list(tasks)).delete()
        context[AuthentaConfig.object_fields] = ['number', ]
        context[AuthentaConfig.object_list] = [objectDict({ 'number': number })]
        return context