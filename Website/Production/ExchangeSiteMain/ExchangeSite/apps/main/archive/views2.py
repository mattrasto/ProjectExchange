from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
import sys
import operator

from ExchangeSite.apps.orderbook import models



#Hook to services.py, then have it call ExchangeEngineCollaborative's AskPriceChecker function to store in variable
#and use to filter, then order list by types
class OrdersView(generic.ListView):
    model = models.Basicorderbook
    template_name = 'Blank.html'
    context_object_name = 'buy_order_list'
    
    
    def get_queryset(self):
        """
        Returns the 15 most viable buy orders
        """
        base_buy_order_list = models.Basicorderbook.objects.filter(
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
        buy_order_list = type_buy_order_list[:15]
        return buy_order_list
    
    '''
    
    
    #NOTE: DOES NOT WORK IN COINCIDENCE WITH get_sell_order_list()
    
    
    def get_sell_order_list(request):
        """
        Returns the 15 most viable sell orders
        """
        base_sell_order_list = models.Basicorderbook.objects.filter(
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
        sell_order_list = type_sell_order_list[:15]
        return sell_order_list
        '''







'''
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html', {'poll': poll})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
'''