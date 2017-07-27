from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^signup.(?P<extension>(html|json|txt))/?$', views.SignUpEXT.as_view(), name='SignUpEXT'),
    url(r'^profile/(?P<pk>\d+).(?P<extension>(html|json|txt))/?$', views.ProfileEXT.as_view(), name='ProfileEXT'),
]