from django import forms

class SingupForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    surname = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    nickname = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Nickname'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

class LoginForm(forms.Form):
    nickname = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Nickname'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))