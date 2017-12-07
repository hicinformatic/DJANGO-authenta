from django.conf.urls import url

from .apps import AuthentaConfig as conf
from . import views

formatter = conf.formatter(conf)
urlpatterns = []

#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
urlpatterns.append(url(r'^{name}/method/function/(?P<pk>\d+)(\.|/)?(?P<extension>({regex_extension}))?/?$'.format(**formatter), views.MethodFunction.as_view(), name='MethodFunction'))
urlpatterns.append(url(r'^{name}/method/detail/(?P<pk>\d+)(\.|/)?(?P<extension>({regex_extension}))?/?$'.format(**formatter), views.MethodDetail.as_view(), name='MethodDetail'))
urlpatterns.append(url(r'^{name}/methods(\.|/)?(?P<extension>({regex_extension}))?/?$'.format(**formatter), views.MethodList.as_view(), name='MethodList'))

#████████╗ █████╗ ███████╗██╗  ██╗
#╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
#   ██║   ███████║███████╗█████╔╝ 
#   ██║   ██╔══██║╚════██║██╔═██╗ 
#   ██║   ██║  ██║███████║██║  ██╗
#   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
urlpatterns.append(url(r'^{name}/task/create(\.|/)?(?P<extension>({regex_extension}))?/?$'.format(**formatter), views.TaskCreate.as_view(), name='TaskCreate'))
urlpatterns.append(url(r'^{name}/task/update/(?P<pk>\d+)(\.|/)?(?P<extension>({regex_extension}))/?$'.format(**formatter), views.TaskUpdate.as_view(), name='TaskUpdate'))
urlpatterns.append(url(r'^{name}/task/detail/(?P<pk>\d+)(\.|/)?(?P<extension>({regex_extension}))/?$'.format(**formatter), views.TaskDetail.as_view(), name='TaskDetail'))
urlpatterns.append(url(r'^{name}/task/purge(\.|/)?(?P<extension>({regex_extension}))/?$'.format(**formatter), views.TaskPurge.as_view(), name='TaskPurge'))