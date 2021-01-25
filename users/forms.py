from django import forms
from django.forms import Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, Account


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=40, required=True,
                               widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Username'}))
    email = forms.EmailField(max_length=60, required=True,
                             widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Email'}))
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'class': 'pr', 'title': 'First name'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Last name'}))
    type_account = forms.BooleanField(help_text='Zaznacz, jeśli chcesz założyć konto Pentestera',
                                   required=False)
    # załóżmy, że 1 to Pentester, a 0 to Klient
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'pr', 'title': 'Password'}))
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'class': 'pr', 'title': 'Confirm password'}))

    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'type_account']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.type_account = self.cleaned_data['type_account']

        if commit:
            user.save()

        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'pr', 'title': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'pr', 'title': 'Password'}))


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=40, required=True,
                               widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Username'}))
    email = forms.EmailField(max_length=60, required=True,
                             widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Email'}))
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'class': 'pr', 'title': 'First name'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Last name'}))

    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'Image': Textarea(attrs={'class': 'im'}),
        }
