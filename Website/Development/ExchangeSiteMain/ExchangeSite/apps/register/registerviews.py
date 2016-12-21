from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core import exceptions
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
import sys
import operator
import datetime

from ExchangeSite.models import exchangemodels, websitemodels
from ExchangeSite.apps.register.forms import RegisterForm
import ExchangeSite.services as services



'''Serving Functions'''



def register(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            hashedpassword = make_password(password)
            user.password = hashedpassword
            form.save(commit=True)
            services.add_user(form.cleaned_data['username'], hashedpassword, form.cleaned_data['email'], form.cleaned_data['first_name'], form.cleaned_data['last_name'],)
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect("success/")
        else:
            #raise exceptions.ValidationError("Form is not valid. Check for duplicate data.")
            print form.errors
    else:
        form = RegisterForm()
    
    return render_to_response('Register4.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'register_form': form}, context_instance=RequestContext(request))
    #return render(request, 'Register3.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'register_form': form}, content_type="html")



def registersuccess(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    usd_balance = get_usd_credit(request)
    btc_balance = get_btc_credit(request)
    total_net_worth = get_total_net_worth(request, latest_price)
    return render_to_response('RegisterSuccess2.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'usd_balance': usd_balance, 'btc_balance': btc_balance, 'total_net_worth': total_net_worth}, context_instance=RequestContext(request))



def registerfail(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    return render_to_response('RegisterFail2.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price}, context_instance=RequestContext(request))



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
    try:
        latest_transaction = exchangemodels.Transactionlog.objects.using('exchange').latest('transactionnumber')
        return latest_transaction.transactionprice
    except:
        return 0



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



def clean_username(self):
    username = self.cleaned_data['username']
    if websitemodels.AuthUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
        #raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        #return render_to_response('TradingTerminal1.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price})
        #return HttpResponse("parent.Response_OK()", mimetype="ExchangeSite/apps/business/static/scripts/error")
        return False
    return True
