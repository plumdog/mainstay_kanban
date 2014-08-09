from django.conf.urls import patterns, url
from . import views

PREFIX = 'kanban'

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^/add/$', views.add_task, name='add_task'),
    url(r'^/edit/(?P<task_id>[0-9]+)/$', views.edit_task, name='edit_task'),
    url(r'^/start/(?P<task_id>[0-9]+)/$', views.start_task, name='start_task'),
    url(r'^/complete/(?P<task_id>[0-9]+)/$', views.complete_task, name='complete_task'))
