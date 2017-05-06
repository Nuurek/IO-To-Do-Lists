from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.IndexMixin.as_view(), name='index'),
    url(r'^create/$', views.ToDoListCreateView.as_view(), name='create_list'),
    url(r'^(?P<todo_list_id>[0-9]+)/$',
        views.ToDoListDetailView.as_view(), name='list'),
    url(r'^(?P<todo_list_id>[0-9]+)/create_item/$',
        views.ToDoListItemCreateView.as_view(), name='create_item'),
    url(r'^register/', include([
        url(r'^$', views.RegisterView.as_view(), name='register'),
        url(r'^success/$', views.RegisterSuccessView.as_view(),
            name='register_success'),
        url(r'^confirm/(?P<user_profile_id>[0-9]+)/(?P<code>.{32})/$',
            views.RegisterConfirmView.as_view(), name='register_confirm')
    ])),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
