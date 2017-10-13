from django.conf.urls import url

from . import views
from .apps import AuthentaConfig

urlpatterns = []
if AuthentaConfig.vsignup:
    urlpatterns.append(url(r'^accounts/(signup|register)(.|/)?(?P<extension>(html|json|txt))?/?$', views.SignUp.as_view(), name='SignUp'))
if AuthentaConfig.vsignin:
    urlpatterns.append(url(r'^accounts/(signin|login)(.|/)?(?P<extension>(html|json|txt))?/?$', views.SignIn.as_view(), name='SignIn'))
if AuthentaConfig.vsignout:
    urlpatterns.append(url(r'^accounts/(signout|logout)(.|/)?(?P<extension>(html|json|txt))?/?$', views.SignOut.as_view(), name='SignOut'))
if AuthentaConfig.vprofilelist:
    urlpatterns.append(url(r'^profile/?.?(?P<extension>(html|json|txt))?$', views.ProfileList.as_view(), name='ProfileList'))
if AuthentaConfig.vprofile:
    urlpatterns.append(url(r'^profile/(?P<pk>\d+).?(?P<extension>(html|json|txt))?/?$', views.Profile.as_view(), name='Profile'))
urlpatterns.append(url(r'^authenta/(?P<command>(error|order|start|running|complete))/(?P<task>\d{1}).(?P<extension>(html|json|txt))/?$', views.Task, name='Task'))
urlpatterns.append(url(r'^authenta/(?P<command>(error|order|start|running|complete))/(?P<task>\d{1}).(?P<extension>(html|json|txt))/(?P<message>.+)/?$', views.Task, name='Task'))
urlpatterns.append(url(r'^authenta/generatecache.(?P<extension>(html|json|txt))/?$', views.GenerateCache.as_view(), name='GenerateCache'))
urlpatterns.append(url(r'^authenta/method/?.?(?P<extension>(html|json|txt))?$', views.MethodList.as_view(), name='MethodList'))
urlpatterns.append(url(r'^authenta/task/(?P<pk>\d+).?(?P<extension>(html|json|txt))?$', views.TaskDetail.as_view(), name='TaskDetail'))

