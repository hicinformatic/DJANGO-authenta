from django.conf.urls import url

from . import views
from .apps import AuthentaConfig

urlpatterns = []
if AuthentaConfig.vsignup:
    urlpatterns.append(url(r'^(signup|register)(.|/)?(?P<extension>(html|json|txt))?/?$', views.SignUp.as_view(), name='SignUp'))
if AuthentaConfig.vsignin:
    urlpatterns.append(url(r'^(signin|login)(.|/)?(?P<extension>(html|json|txt))?/?$', views.SignIn.as_view(), name='SignIn'))
if AuthentaConfig.vsignout:
    urlpatterns.append(url(r'^(signout|logout)(.|/)?(?P<extension>(html|json|txt))?/?$', views.SignOut.as_view(), name='SignOut'))
if AuthentaConfig.vprofilelist:
    urlpatterns.append(url(r'^profile/?.?(?P<extension>(html|json|txt))?$', views.ProfileList.as_view(), name='ProfileList'))
if AuthentaConfig.vprofile:
    urlpatterns.append(url(r'^profile/(?P<pk>\d+).?(?P<extension>(html|json|txt))?/?$', views.Profile.as_view(), name='Profile'))
urlpatterns.append(url(r'^test/?$', views.TestView, name='TestView'))