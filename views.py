from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator

from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import Http404  

from .apps import AuthentaConfig
from .conversion import HybridFormResponseMixin, HybridResponseMixin
from .models import User, Method, Task
from .forms import SignUpForm

from .decorators import localcall, localcalloradmin, localcalloradminorstaff, localcalloradminorstafforlogin
from .functions import order, start, running, complete, error, subtask

from django.core import serializers

class objectDict(object):
    def __init__(self, d):
        self.__dict__ = d

#@localcalloradminorstaff
#def Task(request, command, task, extension, message=''):
#    if command == 'order': return order(extension, task, message)
#    if command == 'start': return start(extension, task, message)
#    if command == 'running': return running(extension, task, message)
#    if command == 'complete': return complete(extension, task, message)
#    if command == 'error': return error(extension, task, message)

class GenerateCache(HybridResponseMixin, TemplateView):
    template_name = 'authenta/method/method.html'

    def get_context_data(self, **kwargs):
        context = super(GenerateCache, self).get_context_data(**kwargs)
        methods = Method.objects.filter(status=True)
        context['object'] = {m.name : m.method for m in methods}
        file_json = '{}/{}'.format(AuthentaConfig.dir_json, AuthentaConfig.cache_methods)
        with open(file_json, 'w') as outfile:
            json_serializer = serializers.get_serializer('json')()
            json_serializer.serialize(methods, stream=outfile, indent=4)
        return context


class TaskCreate(HybridResponseMixin, CreateView):
    model = Task
#class TaskCreate(HybridResponseMixin, View):
#    def get(self, request, *args, **kwargs):
#        extension = '.{}'.format(self.kwargs['extension']) if self.kwargs['extension'] is not None else '.html'
#        info = self.kwargs['info'] if self.kwargs['info'] is not None else None
#        task = Task(task=self.kwargs['tasktype'], info=info)
#        task.save()
#        return redirect(reverse('authenta:TaskDetail', args=[str(task.pk), extension]))
#
#class TaskUpdate(HybridResponseMixin, View):
#    def get(self, request, *args, **kwargs):
#        extension = '.{}'.format(self.kwargs['extension']) if self.kwargs['extension'] is not None else '.html'
#        info = self.kwargs['info'] if self.kwargs['info'] is not None else None
#        error = self.kwargs['error'] if self.kwargs['error'] is not None else None
#        task = Task(task=self.kwargs['tasktype'], info=info, error=error)
#        task.save()
#        return redirect(reverse('authenta:TaskDetail', args=[str(task.pk), extension]))

if AuthentaConfig.vsignup:
    class SignUp(HybridFormResponseMixin, CreateView):
        form_class = SignUpForm
        template_name = 'authenta/form.html'

        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated():
                if AuthentaConfig.vprofile: return redirect(reverse('authenta:Profile', args=[str(request.user.id), '.html']))
                else: raise Http404
            return super(SignUp, self).dispatch(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
            context = super(SignUp, self).get_context_data(**kwargs)
            return context

if AuthentaConfig.vsignin:
    class SignIn(HybridFormResponseMixin, LoginView):
        template_name = 'authenta/form.html'

        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated():
                if AuthentaConfig.vprofile: return redirect(reverse('authenta:Profile', args=[str(request.user.id), '.html']))
                else: raise Http404
            return super(SignIn, self).dispatch(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
            context = super(SignIn, self).get_context_data(**kwargs)
            return context

        def get_success_url(self):
            if self.request.user.is_authenticated:
                return reverse('authenta:Profile', args=[str(self.request.user.id), '.html'])

if AuthentaConfig.vprofilelist:
    class ProfileList(HybridResponseMixin, ListView):
        model = User
        template_name = 'authenta/profilelist.html'
        paginate_by = 26
        slug = None

        def get_context_data(self, **kwargs):
            context = super(ProfileList, self).get_context_data(**kwargs)
            context['fields'] = ['id', 'username']
            return context

if AuthentaConfig.vprofile:
    class Profile(HybridResponseMixin, DetailView):
        model = User
        template_name = 'authenta/profile.html'

        def get_context_data(self, **kwargs):
            context = super(Profile, self).get_context_data(**kwargs)
            context['fields'] = ['username', ]
            context['object_list'] = [self.object]
            return context

if AuthentaConfig.vsignout:
    class SignOut(HybridResponseMixin, LogoutView):
        template_name = 'authenta/profile.html'

        def get_context_data(self, **kwargs):
            context = super(SignOut, self).get_context_data(**kwargs)
            context['fields'] = ['status', ]
            context['object_list'] = [objectDict({ 'status': 'disconnected' })]
            return context

@method_decorator(localcalloradminorstaff, name='dispatch')
class MethodList(HybridResponseMixin, ListView):
    model = Method
    template_name = 'authenta/method/list.html'
    slug = None

    def get_context_data(self, **kwargs):
        context = super(MethodList, self).get_context_data(**kwargs)
        context['fields'] = ['id', 'method', 'name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'permissions']
        context['groups'] = ['id', 'name']
        context['permissions'] = ['id', '__str__']
        return context

@method_decorator(localcalloradminorstaff, name='dispatch')
class TaskDetail(HybridResponseMixin, DetailView):
    model = Task
    template_name = 'authenta/method/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)
        context['fields'] = ['task', 'info', 'status', 'error']
        context['object_list'] = [self.object]
        return context

def TestView(request):
    from django.core.mail import send_mail
    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['charlesdelencre@gmail.com'],
        fail_silently=False,
    )