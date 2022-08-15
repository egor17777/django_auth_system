import hashlib
from multiprocessing import context
from django.shortcuts import render
from .forms import SingupForm, LoginForm
from django.http import HttpResponseRedirect
from .models import User
from django import forms
from .valid import password_valid
# Create your views here.

PASSWORD_SALT = '768d6ff9470a6befffaade6d0419f4aed7ee0fc008ba7515be7f2bc76cba1b40'

def verify_password(password: str, user: User) -> bool:

    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    stored_password_hash=user.password.lower()
    return password_hash == stored_password_hash

def index(request):
    try:
        value = request.COOKIES['username']
        return HttpResponseRedirect('/account')
    except KeyError:
        return render(request, "Authentication/index.html")


def singup(request):
    try:
        value = request.COOKIES['username']
        return HttpResponseRedirect('/account')
    except KeyError:
        
        if request.method == 'POST':
            form = SingupForm(request.POST)
            if form.is_valid() and check_bd_nick(form) and check_bd_email(form) and password_valid(form):
                password = hashlib.sha256((form.cleaned_data['password'] + PASSWORD_SALT).encode()).hexdigest().lower()
                feed = User(
                    name=form.cleaned_data['name'],
                    surname=form.cleaned_data['surname'],
                    nickname=form.cleaned_data['nickname'],
                    email=form.cleaned_data['email'],
                    password=password,
                )
                feed.save()
                response = HttpResponseRedirect('/account')
                username_signed = form.cleaned_data['nickname']
                response.set_cookie(key="username", value=username_signed)
                return response
        else:
            form = SingupForm()
        return render(request, "Authentication/singup.html", context={'form': form})


def login(request):
    try:
        value = request.COOKIES['username']
        return HttpResponseRedirect('/account')
    except KeyError:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            nik = form.data['nickname']
            passw = form.data['password']
            try:
                user = User.objects.get(nickname=nik)
            except Exception:
                form = LoginForm()
                return render(request, "Authentication/login.html", context={'form': form})
            if verify_password(passw, user):
                response = HttpResponseRedirect('/account')
                username_signed = nik
                response.set_cookie(key="username", value=username_signed)
                return response
        else:
            form = LoginForm()
        return render(request, "Authentication/login.html", context={'form': form})


def account(request):
    try:
        value = request.COOKIES['username']
        info = User.objects.get(nickname=value)
        return render(request, "Authentication/account.html",context={'info': info})
    except KeyError:
        return HttpResponseRedirect('/')
    
def singout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie(key="username")
    return response

def check_bd_nick(self):
    nickname = self.cleaned_data['nickname']
    try:
        user = User.objects.get(nickname=nickname)
    except Exception:
        return True
    self._errors['nickname'] = self.error_class(
        ["↓ A user with this nickname is already registered ↓"])
    return False


def check_bd_email(self):
    email = self.cleaned_data['email']
    try:
        user = User.objects.get(email=email)
    except Exception:
        return True
    self._errors['email'] = self.error_class(
        ["↓ A user with this email is already registered ↓"])
    return False


