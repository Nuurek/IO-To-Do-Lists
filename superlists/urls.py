from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexMixin.as_view(), name='index'),
    url(r'^create/$', views.ToDoListCreateView.as_view(), name='create_list'),
    url(r'^(?P<todo_list_id>[0-9]+)/$', views.ToDoListDetailView.as_view(), name='list'),
    url(r'^(?P<todo_list_id>[0-9]+)/create_item/$',
        views.ToDoListItemCreateView.as_view(), name='create_item'),
]
