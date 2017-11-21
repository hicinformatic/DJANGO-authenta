from django.conf.urls import url

from . import views
from .apps import AuthentaConfig as conf
urlpatterns = []

if conf.vsignup:
    urlpatterns.append(url(r'^accounts/({})(\.|/)?$'.format(conf.viewregister_regex, conf.extensions_regex), views.SignUp.as_view(), name='SignUp'))
    urlpatterns.append(url(r'^accounts/({})(\.|/)?(?P<extension>({}))/?$'.format(conf.viewregister_regex, conf.extensions_regex), views.SignUp.as_view(), name='SignUp'))
if conf.vsignin:
    urlpatterns.append(url(r'^accounts/({})(\.|/)?$'.format(conf.viewlogin_regex, conf.extensions_regex), views.SignIn.as_view(), name='SignIn'))
    urlpatterns.append(url(r'^accounts/({})(\.|/)?(?P<extension>({}))/?$'.format(conf.viewlogin_regex, conf.extensions_regex), views.SignIn.as_view(), name='SignIn'))
if conf.vsignout:
    urlpatterns.append(url(r'^accounts/({})(\.|/)?$'.format(conf.viewlogout_regex, conf.extensions_regex), views.SignOut.as_view(),name='SignOut'))
    urlpatterns.append(url(r'^accounts/({})(\.|/)?(?P<extension>({}))/?$'.format(conf.viewlogout_regex, conf.extensions_regex), views.SignOut.as_view(),name='SignOut'))
if conf.vprofilelist:
    urlpatterns.append(url(r'^profile(\.|/)?(?P<extension>({}))/?$'.format(conf.extensions_regex), views.ProfileList.as_view(), name='ProfileList'))
if conf.vprofile:
    urlpatterns.append(url(r'^profile/(?P<pk>\d+).?(?P<extension>({}))/?$'.format(conf.extensions_regex), views.Profile.as_view(), name='Profile'))
urlpatterns.append(url(r'^authenta/method(\.|/)?$', views.MethodList.as_view(), name='MethodList'))
urlpatterns.append(url(r'^authenta/method(\.|/)?(?P<extension>({}))/?$'.format(conf.extensions_regex), views.MethodList.as_view(), name='MethodList'))
urlpatterns.append(url(r'^authenta/method/details/(?P<pk>\d+)(\.|/)?(?P<extension>({}))/?$'.format(conf.extensions_regex), views.MethodDetail.as_view(), name='MethodDetail'))
urlpatterns.append(url(r'^authenta/method/function/(?P<pk>\d+)(\.|/)?(?P<extension>({}))/?$'.format(conf.extensions_regex), views.MethodFunction.as_view(), name='MethodFunction'))
urlpatterns.append(url(r'^authenta/task/create\.?(?P<extension>({}))?/?$'.format(conf.extensions_regex), views.TaskCreate.as_view(), name='TaskCreate'))
urlpatterns.append(url(r'^authenta/task/details/(?P<pk>\d+)(\.|/)?(?P<extension>({}))/?$'.format(conf.extensions_regex), views.TaskDetail.as_view(), name='TaskDetail'))
urlpatterns.append(url(r'^authenta/task/update/(?P<pk>\d+)(\.|/)?(?P<extension>({}))/?$'.format(conf.extensions_regex), views.TaskUpdate.as_view(), name='TaskUpdate'))
urlpatterns.append(url(r'^authenta/task/purge(\.|/)?(?P<extension>({}))/?$'.format(conf.extensions_regex), views.TaskPurge.as_view(), name='TaskPurge'))