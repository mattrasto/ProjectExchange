from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', include('ExchangeSite.apps.register.urls')),
    url(r'^login/', include('ExchangeSite.apps.login.urls')),
    #url(r'^accounts/', include('allauth.urls')),
    url(r'^active/',  include('ExchangeSite.apps.main.urls')),
    url(r'^', include('ExchangeSite.apps.guest.urls'))
)

urlpatterns += staticfiles_urlpatterns()