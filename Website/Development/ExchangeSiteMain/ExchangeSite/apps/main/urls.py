from django.conf.urls import patterns, url

from ExchangeSite.apps.main import mainviews

urlpatterns = patterns('',
    url(r'^orderbook/', mainviews.orderbook),
    #url(r'^trading/basicordersuccess/', mainviews.basic_order_success),
    url(r'^trading/', mainviews.tradingterminal),
    url(r'^about/', mainviews.about),
    url(r'^account/', mainviews.account),
    url(r'^logout/', mainviews.logout_user),
    url(r'^', mainviews.homepage),
)