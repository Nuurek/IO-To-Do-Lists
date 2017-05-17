from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('superlists.urls')),
    url(r'^accounts/', include('accounts.urls')),
    # Django urls
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
]
