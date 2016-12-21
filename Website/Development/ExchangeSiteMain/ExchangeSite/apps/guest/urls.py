from django.conf.urls import patterns, url

from ExchangeSite.apps.guest import guestviews

urlpatterns = patterns('',
    url(r'^about/', guestviews.about),
    url(r'^', guestviews.homepage),
)