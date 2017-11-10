from django.conf.urls import url

from . import views
from .apps import AuthentaConfig
urlpatterns = []

extensions_regex = AuthentaConfig.get_regexarray('extensions_accepted')
if AuthentaConfig.vsignup:
    urlpatterns.append(url(
        r'^accounts/({})(.|/)?(?P<extension>({}))?/?$'.format(AuthentaConfig.get_regexarray('viewregister_accepted'), extensions_regex),
        views.SignUp.as_view(),
        name='SignUp'))
if AuthentaConfig.vsignin:
    urlpatterns.append(url(
        r'^accounts/({})(.|/)?(?P<extension>({}))?/?$'.format(AuthentaConfig.get_regexarray('viewlogin_accepted'), extensions_regex),
        views.SignIn.as_view(),
        name='SignIn'))
if AuthentaConfig.vsignout:
    urlpatterns.append(url(
        r'^accounts/({})(.|/)?(?P<extension>({}))?/?$'.format(AuthentaConfig.get_regexarray('viewlogout_accepted'), extensions_regex),
        views.SignOut.as_view(),
        name='SignOut'))
if AuthentaConfig.vprofilelist:
    urlpatterns.append(url(
        r'^profile/?.?(?P<extension>({}))?$'.format(extensions_regex),
        views.ProfileList.as_view(),
        name='ProfileList'))
if AuthentaConfig.vprofile:
    urlpatterns.append(url(
        r'^profile/(?P<pk>\d+).?(?P<extension>({}))?/?$'.format(extensions_regex),
        views.Profile.as_view(),
        name='Profile'))

urlpatterns.append(url(r'^authenta/method/?.?(?P<extension>({}))?$'.format(extensions_regex), views.MethodList.as_view(), name='MethodList'))
urlpatterns.append(url(r'^authenta/task/details/(?P<pk>\d+).?(?P<extension>({}))?$'.format(extensions_regex), views.TaskDetail.as_view(), name='TaskDetail'))
urlpatterns.append(url(r'^authenta/task/create.?(?P<extension>({}))?/?$'.format(extensions_regex), views.TaskCreate.as_view(), name='TaskCreate'))
urlpatterns.append(url(r'^authenta/task/update/(?P<pk>\d+).?(?P<extension>({}))?/?$'.format(extensions_regex), views.TaskUpdate.as_view(), name='TaskUpdate'))
urlpatterns.append(url(r'^authenta/task/purge.?(?P<extension>({}))?/?$'.format(extensions_regex), views.TaskPurge.as_view(), name='TaskPurge'))