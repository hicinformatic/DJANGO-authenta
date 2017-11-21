from django.conf.urls import url

from . import views
from .apps import AuthentaConfig
urlpatterns = []

if AuthentaConfig.vsignup:
    urlpatterns.append(url(
        r'^accounts/({})(.|/)?$'.format(AuthentaConfig.viewregister_regex, AuthentaConfig.extensions_regex),
        views.SignUp.as_view(),
        name='SignUp'))
    urlpatterns.append(url(
        r'^accounts/({})(.|/)?(?P<extension>({}))/?$'.format(AuthentaConfig.viewregister_regex, AuthentaConfig.extensions_regex),
        views.SignUp.as_view(),
        name='SignUp'))
if AuthentaConfig.vsignin:
    urlpatterns.append(url(
        r'^accounts/({})(.|/)?(?P<extension>({}))/?$'.format(AuthentaConfig.viewlogin_regex, AuthentaConfig.extensions_regex),
        views.SignIn.as_view(),
        name='SignIn'))
if AuthentaConfig.vsignout:
    urlpatterns.append(url(
        r'^accounts/({})(.|/)?(?P<extension>({}))/?$'.format(AuthentaConfig.viewlogout_regex, AuthentaConfig.extensions_regex),
        views.SignOut.as_view(),
        name='SignOut'))
if AuthentaConfig.vprofilelist:
    urlpatterns.append(url(
        r'^profile/?.?(?P<extension>({}))$'.format(AuthentaConfig.extensions_regex),
        views.ProfileList.as_view(),
        name='ProfileList'))
if AuthentaConfig.vprofile:
    urlpatterns.append(url(
        r'^profile/(?P<pk>\d+).?(?P<extension>({}))/?$'.format(AuthentaConfig.extensions_regex),
        views.Profile.as_view(),
        name='Profile'))
urlpatterns.append(url(r'^authenta/method/?\.?$', views.MethodList.as_view(), name='MethodList'))
urlpatterns.append(url(r'^authenta/method/?\.?(?P<extension>({}))$'.format(AuthentaConfig.extensions_regex), views.MethodList.as_view(), name='MethodList'))
urlpatterns.append(url(r'^authenta/method/details/(?P<pk>\d+)\.?(?P<extension>({}))$'.format(AuthentaConfig.extensions_regex), views.MethodDetail.as_view(), name='MethodDetail'))
urlpatterns.append(url(r'^authenta/method/function/(?P<pk>\d+)\.?(?P<extension>({}))$'.format(AuthentaConfig.extensions_regex), views.MethodFunction.as_view(), name='MethodFunction'))
urlpatterns.append(url(r'^authenta/task/create\.?(?P<extension>({}))?/?$'.format(AuthentaConfig.extensions_regex), views.TaskCreate.as_view(), name='TaskCreate'))
urlpatterns.append(url(r'^authenta/task/details/(?P<pk>\d+)\.?(?P<extension>({}))$'.format(AuthentaConfig.extensions_regex), views.TaskDetail.as_view(), name='TaskDetail'))
urlpatterns.append(url(r'^authenta/task/update/(?P<pk>\d+)\.?(?P<extension>({}))/?$'.format(AuthentaConfig.extensions_regex), views.TaskUpdate.as_view(), name='TaskUpdate'))
urlpatterns.append(url(r'^authenta/task/purge\.?(?P<extension>({}))/?$'.format(AuthentaConfig.extensions_regex), views.TaskPurge.as_view(), name='TaskPurge'))