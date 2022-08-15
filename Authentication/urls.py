from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index),
    path('singup', views.singup),
    path('login', views.login),
    path('account', views.account),
    path('singout', views.singout),
]
