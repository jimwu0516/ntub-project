from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
import re

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    user_place = forms.ChoiceField(choices=Profile.USER_PLACE_CHOICES)
    airdrop_wallet_address = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password1',
                  'password2', 'email', 'user_place', 'airdrop_wallet_address']
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['user_place'].choices = [('', '')] + list(self.fields['user_place'].choices)
        self.fields['user_place'].required = True

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        airdrop_wallet_address = cleaned_data.get('airdrop_wallet_address')

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'This email address is already in use.')
        
        if airdrop_wallet_address:
            if not re.match(r'^0x[a-fA-F0-9]{40}$', airdrop_wallet_address):
                self.add_error('airdrop_wallet_address', 'Invalid Ethereum wallet address format.')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_place', 'airdrop_wallet_address']
        
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_place', 'airdrop_wallet_address']

    def clean_airdrop_wallet_address(self):
        airdrop_wallet_address = self.cleaned_data.get('airdrop_wallet_address')
        
        if airdrop_wallet_address:
            if not re.match(r'^0x[a-fA-F0-9]{40}$', airdrop_wallet_address):
                raise forms.ValidationError('Invalid Ethereum wallet address format.')

        return airdrop_wallet_address