from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


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

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'This email address is already in use.')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_place', 'airdrop_wallet_address']
        
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_place', 'airdrop_wallet_address']