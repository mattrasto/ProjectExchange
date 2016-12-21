from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
import django.middleware.csrf
import sys
import operator
import datetime

from ExchangeSite.models import exchangemodels, websitemodels
from ExchangeSite.apps.main.forms import BasicOrderForm
from ExchangeSite.services import add_basic_order, add_instant_order, get_basic_order_from_book, get_basic_order_from_log



'''Serving Functions'''



def homepage(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    btc_credit = get_btc_credit(request)
    total_net_worth = get_total_net_worth(request, latest_price)
    buy_order_list = get_buy_order_list(request, 15)
    sell_order_list = get_sell_order_list(request, 15)
    user_count = get_user_count(request)
    news_stories = get_news_stories(request)
    usd_balance = get_usd_credit(request)
    btc_balance = get_btc_credit(request)
    total_net_worth = get_total_net_worth(request, latest_price)
    print news_stories
    # for story in news_stories:
    #     print ""
    #     print story.type + " story number " + str(story.story_id) + ":"
    #     print ""
    #     print story.title
    #     print story.content
    #     print story.author
    #     print story.date_entered
    return render_to_response('Homepage8.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'usd_balance': usd_balance, 'btc_balance': btc_balance, 'total_net_worth': total_net_worth, 'user_count': user_count, 'buy_order_list': buy_order_list, 'sell_order_list': sell_order_list, 'news_stories': news_stories}, context_instance=RequestContext(request))



def tradingterminal(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    btc_credit = get_btc_credit(request)
    total_net_worth = get_total_net_worth(request, latest_price)
    buy_order_list = get_buy_order_list(request, 15)
    sell_order_list = get_sell_order_list(request, 15)
    usd_balance = get_usd_credit(request)
    btc_balance = get_btc_credit(request)
    total_net_worth = get_total_net_worth(request, latest_price)
    
    if request.method == 'POST':
        print request.POST
        # If hidden input field indicates a buy order
        if 'buy_form' in request.POST:
            form = BasicOrderForm(request.POST)
            order_action = "BUY"
            print "BUY ORDER: INITIALIZING REQUEST"
        # If hidden input field indicates a buy order
        elif 'sell_form' in request.POST:
            form = BasicOrderForm(request.POST)
            order_action = "SELL"
            print "SELL ORDER: INITIALIZING REQUEST"
        # If form was tampered with and hidden field indicates something else
        else:
            print "NEITHER BUY NOR SELL: CANCELING REQUEST"
            return Http
        if form.is_valid():
            user = request.user
            print "CREATING ORDER"
            # If order type is conditional, gather condition (trigger) and condition value (trigger value)
            if form.cleaned_data["order_type"] == "CONDITIONAL":
                condition_type = form.cleaned_data["condition"]
                condition_value = form.cleaned_data["condition_value"]
            else:
                condition_type = ""
                condition_value = ""
            # Values passed to function
            '''
            print user.username
            print form.cleaned_data["price"]
            print form.cleaned_data["volume"]
            print form.cleaned_data["order_type"]
            print order_action
            print condition_type
            print condition_value
            '''
            if form.cleaned_data["order_type"] == "INSTANT":
                if order_action == "BUY":
                    order_constraint = form.cleaned_data["buy_order_constraint"]
                elif order_action == "SELL":
                    order_constraint = form.cleaned_data["sell_order_constraint"]
                print "-----"
                print order_constraint
                order_number = add_instant_order(user.username, order_action, order_constraint, form.cleaned_data["price"], form.cleaned_data["volume"])
                if order_number == False:
                    print "ERROR: INSTANT ORDER NOT TRANSACTED"
                    #return order fail page
                    sys.exit()
                order = services_get_basic_order_from_log("ORDER NUMBER", order_number)
                order_total = order[5]*order[6]
                return render_to_response('InstantOrderSuccess1.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'usd_balance': usd_balance, 'btc_balance': btc_balance, 'total_net_worth': total_net_worth, 'order': order, 'order_total': order_total}, context_instance=RequestContext(request))
            elif form.cleaned_data["order_type"] == "LIQUID" or form.cleaned_data["order_type"] == "LIMIT" or form.cleaned_data["order_type"] == "CONDITIONAL":
                order_number = add_basic_order(user.username, form.cleaned_data["price"], form.cleaned_data["volume"], form.cleaned_data["order_type"], order_action, condition_type, condition_value)
                order = services_get_basic_order_from_book("ORDER NUMBER", order_number)
            return render_to_response('OrderSuccess2.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'usd_balance': usd_balance, 'btc_balance': btc_balance, 'total_net_worth': total_net_worth, 'order': order}, context_instance=RequestContext(request))
        else:
            print "FORM NOT VALID"
            print form.errors
    else:
        form = BasicOrderForm()
        
    return render_to_response('TradingTerminal2.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'usd_balance': usd_balance, 'btc_balance': btc_balance, 'total_net_worth': total_net_worth, 'buy_order_list': buy_order_list, 'sell_order_list': sell_order_list, 'form': form}, context_instance=RequestContext(request))



def orderbook(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    buy_order_list = get_buy_order_list(request, "all")
    sell_order_list = get_sell_order_list(request, "all")
    transaction_list = get_transaction_list(request, "all")
    usd_balance = get_usd_credit(request)
    btc_balance = get_btc_credit(request)
    total_net_worth = get_total_net_worth(request, latest_price)
    return render_to_response('OrderBook3.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'usd_balance': usd_balance, 'btc_balance': btc_balance, 'total_net_worth': total_net_worth, 'buy_order_list': buy_order_list, 'sell_order_list': sell_order_list, 'transaction_list': transaction_list}, context_instance=RequestContext(request))



def about(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    usd_balance = get_usd_credit(request)
    btc_balance = get_btc_credit(request)
    total_net_worth = get_total_net_worth(request, latest_price)
    return render_to_response('About2.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'usd_balance': usd_balance, 'btc_balance': btc_balance, 'total_net_worth': total_net_worth}, context_instance=RequestContext(request))



def account(request):
    bid_price = get_bid_price(request)
    ask_price = get_ask_price(request)
    latest_price = get_latest_price(request)
    user = request.user
    order_list = services_get_basic_order_from_book("USERNAME", user.username)
    usd_balance = get_usd_credit(request)
    btc_balance = get_btc_credit(request)
    total_net_worth = get_total_net_worth(request, latest_price)
    return render_to_response('Account2.html', {'bid_price': bid_price, 'ask_price': ask_price, 'latest_price': latest_price, 'order_list': order_list, 'usd_balance': usd_balance, 'btc_balance': btc_balance, 'total_net_worth': total_net_worth}, context_instance=RequestContext(request))



def logout_user(request):
    logout(request)
    # Create separate logout success page
    return HttpResponseRedirect("/homepage/")



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



def services_get_basic_order_from_book(search_parameter, search_value):
    order = get_basic_order_from_book(search_parameter, search_value)
    return order

def services_get_basic_order_from_log(search_parameter, search_value):
    order = get_basic_order_from_log(search_parameter, search_value)
    return order



def get_news_stories(request):
    news_stories = websitemodels.NewsStories.objects.all().filter()
    return news_stories





