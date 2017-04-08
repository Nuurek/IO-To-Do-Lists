from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<todo_list_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create_todo_list/$', views.create_todo_list, name='create_todo_list'),
    url(r'^(?P<todo_list_id>[0-9]+)/add_todo_list_item/$',
        views.add_todo_list_item, name='add_todo_list_item'),
]
