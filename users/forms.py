from django import forms
from django.forms import Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, Account


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=40, required=True,
                               widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Nazwa użytkownika'}))
    email = forms.EmailField(max_length=60, required=True,
                             widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Email'}))
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Imię'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Nazwisko'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'pr', 'title': 'Hasło powinno: zawierać minimum 8 znaków, nie może składać się z samych cyfr,'
                                       'nie może być powszechnie znane, nie może zawirerać informacji personalnych'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'pr', 'title': 'Potwierdź hasło'}))

    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.type_account = 0

        if commit:
            user.save()

        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'pr', 'title': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'pr', 'title': 'Hasło'}))


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=40, required=True,
                               widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Nazwa użytkownika'}))
    email = forms.EmailField(max_length=60, required=True,
                             widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Email'}))
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Imię'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Nazwisko'}))

    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
