from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.urls import reverse
from django.shortcuts import redirect
from django.http import Http404  

from django.contrib.auth.views import LoginView, LogoutView

from .apps import AuthentaConfig
from .conversion import HybridResponseMixin
from .forms import SignUpForm
from .models import User

if AuthentaConfig.vsignup:
    class SignUp(HybridResponseMixin, CreateView):
        form_class = SignUpForm
        template_name = 'authenta/form.html'

        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated():
                if AuthentaConfig.vprofile: return redirect(reverse('authenta:Profile', args=[str(request.user.id), '.html']))
                else: raise Http404
            return super(SignUp, self).dispatch(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
            context = super(SignUp, self).get_context_data(**kwargs)
            context['object'] = {field.html_name : field.help_text for field in context['form']}
            return context

if AuthentaConfig.vsignin:
    class SignIn(HybridResponseMixin, LoginView):
        template_name = 'authenta/form.html'

        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated():
                if AuthentaConfig.vprofile: return redirect(reverse('authenta:Profile', args=[str(request.user.id), '.html']))
                else: raise Http404
            return super(SignIn, self).dispatch(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
            context = super(SignIn, self).get_context_data(**kwargs)
            context['object'] = {field.html_name : field.help_text for field in context['form']}
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
            context['object'] = {user.id : user.username for user in context['object_list']}
            return context

if AuthentaConfig.vprofile:
    class Profile(HybridResponseMixin, DetailView):
        model = User
        template_name = 'authenta/profile.html'

        def get_context_data(self, **kwargs):
            context = super(Profile, self).get_context_data(**kwargs)
            context['object'] = { "username" : self.object.username, }
            return context

if AuthentaConfig.vsignout:
    class SignOut(HybridResponseMixin, LogoutView):
        template_name = 'authenta/profile.html'

        def get_context_data(self, **kwargs):
            context = super(SignOut, self).get_context_data(**kwargs)
            context['object'] = { "status" : "disconnected" }
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