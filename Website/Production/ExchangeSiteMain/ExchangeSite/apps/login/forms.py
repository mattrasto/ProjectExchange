from django import forms
from ExchangeSite.models.websitemodels import AuthUser



class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = AuthUser
        fields = ('username', 'password')
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'logintext', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class' : 'logintext', 'placeholder': 'Password'})
        # Figure out how to update all fields at once
        #self.fields['username', 'password'].widget.attrs.update({'class': 'logintext'})