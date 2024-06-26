from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
# from pxomymart.products.models import User
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'agree_terms')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agree_terms'].label = 'I agree to the Terms of Service'

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'your_name', 'placeholder': 'Username'}),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'your_pass', 'placeholder': 'Password'}),
        label='Password'
    )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'state', 'city', 'lga', 'town', 'zipcode', 'street', 'house_address', 'mobile_number', 'additional_info']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                # 'placeholder': 'Enter your state'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                # 'placeholder': 'Enter your city'
            }),
            'lga': forms.TextInput(attrs={
                'class': 'form-control',
                # 'placeholder': 'Enter your local government area'
            }),
            'town': forms.TextInput(attrs={
                'class': 'form-control',
                # 'placeholder': 'Enter your town'
            }),
            'zipcode': forms.TextInput(attrs={
                'class': 'form-control',
                # 'placeholder': 'Enter your zipcode'
            }),
            'street': forms.TextInput(attrs={
                'class': 'form-control',
                # 'placeholder': 'Enter your street'
            }),
            'house_address': forms.TextInput(attrs={
                'class': 'form-control',
                # 'placeholder': 'Enter your house address'
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                # 'placeholder': 'Enter your mobile number'
            }),
            'additional_info': forms.Textarea(attrs={
                'class': 'form-control',
                # 'placeholder': 'Enter any additional information'
            }),
        }

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }