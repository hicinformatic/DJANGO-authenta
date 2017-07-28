from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^signup.?(?P<extension>(html|json|txt))?/?$', views.SignUp.as_view(), name='SignUp'),
    url(r'^profile/(?P<pk>\d+).?(?P<extension>(html|json|txt))?/?$', views.Profile.as_view(), name='Profile'),
]