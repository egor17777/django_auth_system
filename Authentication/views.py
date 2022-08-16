import base64, hmac, hashlib
from urllib import response
from django.shortcuts import render
from .forms import SingupForm, LoginForm
from django.http import HttpResponseRedirect
from .models import User
from .valid import *
# Create your views here.




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
                username = form.cleaned_data['nickname']
                username_signed = base64.b64encode(username.encode()).decode() + "." + sign_data(username)
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
                username = nik
                username_signed = base64.b64encode(username.encode()).decode() + "." + sign_data(username)
                response.set_cookie(key="username", value=username_signed)

                return response
        else:
            form = LoginForm()
        return render(request, "Authentication/login.html", context={'form': form})


def account(request):
    try:
        value = request.COOKIES['username']
        valid_username = get_username_from_signed_string(value)
        info = User.objects.get(nickname=valid_username)
        return render(request, "Authentication/account.html",context={'info': info})
    except Exception:
        response = HttpResponseRedirect('/')
        response.delete_cookie(key="username")
        return response
    
def singout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie(key="username")
    return response




