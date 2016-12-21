from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate, login
import sys
import operator
import datetime

from ExchangeSite.models import websitemodels, exchangemodels
from ExchangeSite.apps.login.forms import LoginForm



'''Serving Functions'''



def loginuser(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("success/")
            else:
                # Return a 'disabled account' error message
                return HttpResponseRedirect("disabled/")
        else:
            # Return an 'invalid login' error message.
            return HttpResponseRedirect("fail/")
    else:
        form = LoginForm()
    
    return render_to_response('Login4.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'form': form}, context_instance=RequestContext(request))



def loginsuccess(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    usd_balance = get_usd_credit(request)
    btc_balance = get_btc_credit(request)
    total_net_worth = get_total_net_worth(request, latest_price)
    return render_to_response('LoginSuccess2.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'usd_balance': usd_balance, 'btc_balance': btc_balance, 'total_net_worth': total_net_worth}, context_instance=RequestContext(request))



def accountdisabled(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    return render_to_response('LoginDisabled2.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price}, context_instance=RequestContext(request))



def loginfail(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    return render_to_response('LoginFail2.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price}, context_instance=RequestContext(request))



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



def get_usd_credit(request):
    user = request.user
    userdetails = exchangemodels.Userbook.objects.using('exchange').get(username=user.username)
    return userdetails.usdcredit



def get_btc_credit(request):
    user = request.user
    userdetails = exchangemodels.Userbook.objects.using('exchange').get(username=user.username)
    return userdetails.btccredit



def get_total_net_worth(request, latest_price):
    user = request.user
    userdetails = exchangemodels.Userbook.objects.using('exchange').get(username=user.username)
    total_net_worth = (userdetails.btccredit)*(latest_price) + (userdetails.usdcredit)
    return total_net_worth




