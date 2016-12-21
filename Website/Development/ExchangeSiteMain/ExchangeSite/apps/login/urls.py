from django.conf.urls import patterns, url

from ExchangeSite.apps.login import loginviews

urlpatterns = patterns('',
    url(r'^success/', loginviews.loginsuccess),
    url(r'^fail/', loginviews.loginfail),
    url(r'^disabled/', loginviews.accountdisabled),
    url(r'^', loginviews.loginuser),
)