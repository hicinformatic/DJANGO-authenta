from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.base import TemplateView


from django.urls import reverse
from django.shortcuts import redirect
from django.http import Http404  

from django.contrib.auth.views import LoginView, LogoutView


#from django.contrib.auth.forms import AuthenticationForm




from .apps import AuthentaConfig
from .conversion import HybridResponseMixin
from .models import User
from .forms import SignUpForm#, LDAPAuthenticationForm


class AuthentaLoginView(LoginView):
    pass
    #template_name = 'authenta/login.html'
    #slug = None

    #def get_context_data(self, **kwargs):
    #    context = super(AuthentaLoginView, self).get_context_data(**kwargs)
    #    context['object'] = {field.html_name : field.help_text for field in context['form']}
    #    if AuthentaConfig.ldap_activated:
    #        context['ldapform'] = LDAPAuthenticationForm()
    #    context['app_path'] = self.request.get_full_path()
    #    return context

#class LoginView(SuccessURLAllowedHostsMixin, FormView):
#    """
#    Displays the login form and handles the login action.
#    """
#    form_class = AuthenticationForm
#    authentication_form = None
#    redirect_field_name = REDIRECT_FIELD_NAME
#    template_name = 'registration/login.html'
#    redirect_authenticated_user = False
#    extra_context = None
#
#    @method_decorator(sensitive_post_parameters())
#    @method_decorator(csrf_protect)
#    @method_decorator(never_cache)
#    def dispatch(self, request, *args, **kwargs):
#        if self.redirect_authenticated_user and self.request.user.is_authenticated:
#            redirect_to = self.get_success_url()
#            if redirect_to == self.request.path:
#                raise ValueError(
#                    "Redirection loop for authenticated user detected. Check that "
#                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
#                )
#            return HttpResponseRedirect(redirect_to)
#        return super(LoginView, self).dispatch(request, *args, **kwargs)
#
#    def get_success_url(self):
#        url = self.get_redirect_url()
#        return url or resolve_url(settings.LOGIN_REDIRECT_URL)
#
#    def get_redirect_url(self):
#        """Return the user-originating redirect URL if it's safe."""
#        redirect_to = self.request.POST.get(
#            self.redirect_field_name,
#            self.request.GET.get(self.redirect_field_name, '')
#        )
#        url_is_safe = is_safe_url(
#            url=redirect_to,
#            allowed_hosts=self.get_success_url_allowed_hosts(),
#            require_https=self.request.is_secure(),
#        )
#        return redirect_to if url_is_safe else ''
#
#    def get_form_class(self):
#        return self.authentication_form or self.form_class
#
#    def get_form_kwargs(self):
#        kwargs = super(LoginView, self).get_form_kwargs()
#        kwargs['request'] = self.request
#        return kwargs
#
#    def form_valid(self, form):
#        """Security check complete. Log the user in."""
#        auth_login(self.request, form.get_user())
#        return HttpResponseRedirect(self.get_success_url())
#
#    def get_context_data(self, **kwargs):
#        context = super(LoginView, self).get_context_data(**kwargs)
#        current_site = get_current_site(self.request)
#        context.update({
#            self.redirect_field_name: self.get_redirect_url(),
#            'site': current_site,
#            'site_name': current_site.name,
#        })
#        if self.extra_context is not None:
#            context.update(self.extra_context)
#        return context

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