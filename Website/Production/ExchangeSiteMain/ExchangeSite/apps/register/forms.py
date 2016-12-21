from django import forms
from ExchangeSite.models import websitemodels



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    firstname = forms.CharField(required=False)
    lastname = forms.CharField(required=False)

    class Meta:
        model = websitemodels.AuthUser
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'registertext', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class' : 'registertext', 'placeholder': 'Password'})
        self.fields['email'].widget.attrs.update({'class' : 'registertext', 'placeholder': 'Email'})
        self.fields['firstname'].widget.attrs.update({'class' : 'registertext', 'placeholder': 'First Name'})
        self.fields['lastname'].widget.attrs.update({'class' : 'registertext', 'placeholder': 'Last Name'})
        # Figure out how to update all fields at once
        #self.fields['username', 'password', 'email', 'firstname', 'lastname'].widget.attrs.update({'class': 'registertext'})