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

from .apps import (AuthentaConfig as conf, logmethis)
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
#        if self.kwarg_extension in kwargs: self.extension = conf.extensions[kwargs[self.kwarg_extension]]
#        return super(UpdateView, self).dispatch(request, *args, **kwargs)

"""
██╗   ██╗███████╗███████╗██████╗ 
██║   ██║██╔════╝██╔════╝██╔══██╗
██║   ██║███████╗█████╗  ██████╔╝
██║   ██║╚════██║██╔══╝  ██╔══██╗
╚██████╔╝███████║███████╗██║  ██║
 ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
"""

if conf.vsignup:
    class SignUp(HybridResponseMixin, CreateView):
        is_form = True
        has_token = True
        form_class = SignUpForm
        template_name = conf.template_form

        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated():
                if conf.vprofile: 
                    return redirect(
                        reverse(
                            conf.vuser_absolute,
                            kwargs={'pk': request.user.id, self.kwarg_extension: conf.extensions[self.extension]})
                        )
                raise Http404
            return super(SignUp, self).dispatch(request, *args, **kwargs)

        def get_success_url(self):
            return reverse(conf.vuser_absolute, kwargs={'pk': self.object.id, self.kwarg_extension: conf.extensions[self.extension]})

if conf.vsignin:
    class SignIn(HybridResponseMixin, LoginView):
        is_form = True
        has_token = True
        template_name = conf.template_form

        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated():
                if conf.vprofile: 
                    return redirect(
                        reverse(
                            conf.vuser_absolute,
                            kwargs={
                                'pk': request.user.id,
                                self.kwarg_extension: conf.extensions[self.extension]
                            })
                        )
                raise Http404
            return super(SignIn, self).dispatch(request, *args, **kwargs)

        def get_success_url(self):
            return reverse(conf.vuser_absolute, kwargs={'pk': self.object.id, self.kwarg_extension: conf.extensions[self.extension]})
            #if self.request.user.is_authenticated:
            #    return reverse('authenta:Profile', args=[str(self.request.user.id), '.html'])

if conf.vsignout:
    class SignOut(HybridResponseMixin, LogoutView):
        template_name = 'authenta/profile.html'

        def get_context_data(self, **kwargs):
            context = super(SignOut, self).get_context_data(**kwargs)
            context[conf.object_fields] = ['status', ]
            context[conf.object_list] = [objectDict({ 'status': 'disconnected' })]
            return context

if conf.vprofilelist:
    class ProfileList(HybridResponseMixin, ListView):
        model = User
        template_name = 'authenta/profilelist.html'
        paginate_by = 26
        slug = None

        def get_context_data(self, **kwargs):
            context = super(ProfileList, self).get_context_data(**kwargs)
            context[conf.object_fields] = ['id', 'username']
            return context

if conf.vprofile:
    class Profile(HybridResponseMixin, DetailView):
        model = User
        template_name = 'authenta/profile.html'

        def get_context_data(self, **kwargs):
            context = super(Profile, self).get_context_data(**kwargs)
            context[conf.object_fields] = ['username', ]
            context[conf.object_list] = [self.object]
            return context


"""
███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  
"""

@method_decorator(howtoaccess(conf.host+['is_superuser','is_staff']), name='dispatch')
class MethodList(HybridResponseMixin, ListView):
    model = Method
    template_name = 'authenta/method/list.html'
    slug = id

    def get_context_data(self, **kwargs):
        context = super(MethodList, self).get_context_data(**kwargs)
        context[conf.object_fields] = ['id', 'method', 'name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'permissions']
        context['groups'] = ['id', 'name']
        context['permissions'] = ['id', '__str__']
        return context

@method_decorator(howtoaccess(conf.host+['is_superuser','is_staff']), name='dispatch')
class MethodDetail(HybridResponseMixin, DetailView):
    model = Method
    template_name = conf.template_detail

    def get_context_data(self, **kwargs):
        context = super(MethodDetail, self).get_context_data(**kwargs)
        context[conf.object_fields] = ['id', 'name', 'status', 'error']
        context[conf.object_list] = [self.object]
        return context

@method_decorator(howtoaccess(conf.host+['is_superuser','is_staff']), name='dispatch')
class MethodFunction(HybridResponseMixin, UpdateView):
    is_form = True
    has_token = True
    model = Method
    template_name = conf.template_form
    form_class = MethodFormFunction
    slug = id

    def get_success_url(self):
        return reverse (conf.vmethod_absolute, kwargs={'pk': self.object.id, self.kwarg_extension: conf.extensions[self.extension]})

"""
████████╗ █████╗ ███████╗██╗  ██╗
╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
   ██║   ███████║███████╗█████╔╝ 
   ██║   ██╔══██║╚════██║██╔═██╗ 
   ██║   ██║  ██║███████║██║  ██╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""

@method_decorator(howtoaccess(conf.host+['is_superuser','is_staff']), name='dispatch')
class TaskCreate(HybridResponseMixin, CreateView):
    is_form = True
    has_token = True
    model = Task
    fields = ['task', 'info']
    template_name = conf.template_form

    def get_success_url(self):
        return reverse (conf.vtask_absolute, kwargs={'pk': self.object.id, self.kwarg_extension: self.extension() })

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.update_by = getattr(self.request.user, conf.uniqidentity)
        return self.form_valid(form)  if form.is_valid() else self.form_invalid(form)

@method_decorator(howtoaccess(conf.host+['is_superuser','is_staff']), name='dispatch')
class TaskDetail(HybridResponseMixin, DetailView):
    model = Task
    template_name = conf.template_detail

    def get_context_data(self, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)
        context[conf.object_fields] = ['task', 'info', 'status', 'error']
        context[conf.object_list] = [self.object]
        return context

@method_decorator(howtoaccess(conf.host+['is_superuser','is_staff']), name='dispatch')
class TaskUpdate(HybridResponseMixin, UpdateView):
    model = Task
    fields = ['task', 'status', 'info', 'error']
    template_name = conf.template_form
    has_token = True
    is_form = True

    def get_success_url(self):
        return reverse(conf.vtask_absolute, kwargs={'pk': self.object.id, self.kwarg_extension: conf.extensions[self.extension]})

    def form_valid(self, form):
        self.object.update_by = getattr(self.request.user, conf.uniqidentity)
        return super(TaskUpdate, self).form_valid(form)

@method_decorator(howtoaccess(conf.host+['is_superuser','is_staff']), name='dispatch')
class TaskPurge(HybridResponseMixin, TemplateView):
    template_name = conf.template_detail

    def get_context_data(self, **kwargs):
        context = super(TaskPurge, self).get_context_data(**kwargs)
        tasks = Task.objects.all().order_by('-id')[1000:0].values_list('id', flat=True)
        tasks.first()
        number = tasks.count()
        Task.objects.exclude(pk__in=list(tasks)).delete()
        context[conf.object_fields] = ['number', ]
        context[conf.object_list] = [objectDict({ 'number': number })]
        return context