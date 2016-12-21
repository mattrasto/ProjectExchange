from django import forms



class BasicOrderForm(forms.Form):
    CONDITION_CHOICES = [("Bid Price", "Bid Price"),
                         ("Ask Price", "Ask Price"),
                         ("Latest Price", "Latest Price")]
    price = forms.FloatField(required=False)
    volume = forms.FloatField(required=False)
    order_type = forms.CharField(widget=forms.HiddenInput(), initial="INSTANT")
    buy_order_constraint = forms.CharField(required=False, widget=forms.HiddenInput(), initial="PRICE")
    sell_order_constraint = forms.CharField(required=False, widget=forms.HiddenInput(), initial="PRICE")
    condition = forms.ChoiceField(required=False, choices=CONDITION_CHOICES)
    condition_value = forms.FloatField(required=False)

    class Meta:
        fields = ('price', 'volume', 'order_type', 'buy_order_constraint', 'sell_order_constraint', 'condition', 'condition_value')
    
    def __init__(self, *args, **kwargs):
        super(BasicOrderForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs.update({'class' : 'createordertext', 'placeholder': 'Price'})
        self.fields['volume'].widget.attrs.update({'class' : 'createordertext', 'placeholder': 'Volume'})
        self.fields['order_type'].widget.attrs.update({'class' : 'order_type', 'default': 'INSTANT'})
        self.fields['buy_order_constraint'].widget.attrs.update({'id' : 'buy_order_constraint', 'default': 'PRICE'})
        self.fields['sell_order_constraint'].widget.attrs.update({'id' : 'sell_order_constraint', 'default': 'PRICE'})
        self.fields['condition'].widget.attrs.update({'class' : 'createorderselect', 'placeholder': 'Condition'})
        self.fields['condition_value'].widget.attrs.update({'class' : 'createordertext', 'placeholder': 'Value'})



