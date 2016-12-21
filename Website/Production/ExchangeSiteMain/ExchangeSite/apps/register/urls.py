from django.conf.urls import patterns, url

from ExchangeSite.apps.register import registerviews

urlpatterns = patterns('',
    url(r'^success/', registerviews.registersuccess),
    url(r'^fail/', registerviews.registerfail),
    url(r'^', registerviews.register),
)