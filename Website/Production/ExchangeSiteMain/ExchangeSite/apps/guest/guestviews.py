from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.http import Http404
from django.shortcuts import render, get_object_or_404
import sys
import operator
import datetime

from ExchangeSite.models import exchangemodels, websitemodels



'''Serving Functions'''



def homepage(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    buy_order_list = get_buy_order_list(request, 15)
    sell_order_list = get_sell_order_list(request, 15)
    user_count = get_user_count(request)
    return render_to_response('GuestHomepage8.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'user_count': user_count, 'buy_order_list': buy_order_list, 'sell_order_list': sell_order_list}, context_instance=RequestContext(request))



def about(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    return render_to_response('GuestAbout1.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price})



'''Data Functions'''



def get_bid_price(request):
    import ExchangeSite.services as services
    bid_price = services.bid_price()
    return bid_price



def get_ask_price(request):
    import ExchangeSite.services as services
    ask_price = services.ask_price()
    return ask_price



def get_latest_price(request):
    latest_transaction = exchangemodels.Transactionlog.objects.using('exchange').latest('transactionnumber')
    return latest_transaction.transactionprice



def get_buy_order_list(request, truncate):
    """
    Returns the 15 most viable buy orders
    """
    base_buy_order_list = exchangemodels.Basicorderbook.objects.using('exchange').filter(
        action = 'Buy', 
        price__gt=600, 
        active = 1
        )
    volume_buy_order_list = base_buy_order_list.order_by('-volume')
    type_buy_order_list = []
    
    for order in volume_buy_order_list:
        if order.type == 'Liquid':
            type_buy_order_list.append(order)
    for order in volume_buy_order_list:
        if order.type == 'Limit':
            type_buy_order_list.append(order)
    for order in volume_buy_order_list:
        if order.type == 'Conditional':
            type_buy_order_list.append(order)
    type_buy_order_list.sort(key=operator.attrgetter('price'), reverse = True)
    if truncate == "all":
        buy_order_list = type_buy_order_list
    else:
        buy_order_list = type_buy_order_list[:truncate]
    return buy_order_list
    


def get_sell_order_list(request, truncate):
    """
    Returns the 15 most viable sell orders
    """
    base_sell_order_list = exchangemodels.Basicorderbook.objects.using('exchange').filter(
        action = 'Sell', 
        price__lt=800, 
        active = 1
        )
    volume_sell_order_list = base_sell_order_list.order_by('-volume')
    type_sell_order_list = []
    
    for order in volume_sell_order_list:
        if order.type == 'Liquid':
            type_sell_order_list.append(order)
    for order in volume_sell_order_list:
        if order.type == 'Limit':
            type_sell_order_list.append(order)
    for order in volume_sell_order_list:
        if order.type == 'Conditional':
            type_sell_order_list.append(order)
    type_sell_order_list.sort(key=operator.attrgetter('price'), reverse = False)
    if truncate == "all":
        sell_order_list = type_sell_order_list
    else:
        sell_order_list = type_sell_order_list[:truncate]
    return sell_order_list



def get_user_count(request):
    user_count = websitemodels.AuthUser.objects.all().count()
    return user_count



def get_transaction_list(request, truncate):
    current_date = datetime.datetime.now()
    month_ago_date = current_date - datetime.timedelta(days=31)
    transaction_list = exchangemodels.Transactionlog.objects.using('exchange').filter(transactiondate__gt = month_ago_date)
    if truncate == "all":
        return transaction_list
    else:
        return transaction_list[:10]


