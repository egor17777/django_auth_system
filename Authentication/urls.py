from django.urls import path, include
from . import views 
urlpatterns = [
    path('', views.index),
    path('singup', views.singup),
    path('login', views.login),
    path('account', views.account),
    path('singout', views.singout),
    path('captcha/', include('captcha.urls')),
]
