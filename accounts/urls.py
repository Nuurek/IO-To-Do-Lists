from django.conf.urls import url, include

from . import views


register_urls = [
    url(r'^$', views.RegisterView.as_view(), name='register'),
    url(r'^success/$', views.RegisterSuccessView.as_view(),
        name='register_success'),
    url(r'^confirm/(?P<user_profile_id>[0-9]+)/(?P<code>.{32})/$',
        views.RegisterConfirmView.as_view(), name='register_confirm')
]

urlpatterns = [
    url(r'^register/', include(register_urls)),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^user/$', views.UserProfileView.as_view(), name='user'),
]