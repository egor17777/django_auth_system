from django.shortcuts import render
from .forms import SingupForm, LoginForm
from django.http import HttpResponseRedirect
from .models import User
from django import forms
# Create your views here.


def index(request):
    return render(request,"Authentication/index.html")

def singup(request):
    if request.method == 'POST':
        form = SingupForm(request.POST)
        if form.is_valid() and clean(form) and check_bd_nick(form) and check_bd_email(form):
            print(form.cleaned_data)
            feed = User(
                name = form.cleaned_data['name'],
                surname = form.cleaned_data['surname'],
                nickname = form.cleaned_data['nickname'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
            )
            feed.save()
            return HttpResponseRedirect('/account')
    else:
        form = SingupForm()
    return render(request, "Authentication/singup.html", context={'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        nik = form.data['nickname']
        passw = form.data['password']
        try:
            user = User.objects.get(nickname= nik)
        except Exception:
            form = LoginForm()
            return render(request,"Authentication/login.html", context={'form': form})
        if user.nickname == nik and user.password == passw:
            return HttpResponseRedirect('/account')
    else:
        form = LoginForm()
    return render(request,"Authentication/login.html", context={'form': form})

def account(request):
    return render(request,"Authentication/account.html")

def clean(self):

    password = self.cleaned_data['password']
    password_repeat = self.cleaned_data['confirm_password']
    if password != password_repeat:
        self._errors['confirm_password'] = self.error_class(["↕↕ The passwords don't match! ↕↕"])
        return False

    return self.cleaned_data

def check_bd_nick(self):
    nickname = self.cleaned_data['nickname']
    try:
        user = User.objects.get(nickname= nickname)
    except Exception:
        return True
    self._errors['nickname'] = self.error_class(["↓ A user with this nickname is already registered ↓"])
    return False

def check_bd_email(self):
    email = self.cleaned_data['email']
    try:
        user = User.objects.get(email= email)
    except Exception:
        return True
    self._errors['email'] = self.error_class(["↓ A user with this email is already registered ↓"])
    return False