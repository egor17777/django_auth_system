from django.db import models

# Create your models here.



class User(models.Model):
    name = models.CharField(max_length=40, null=True, blank= True)
    surname = models.CharField(max_length=40)
    nickname = models.CharField(max_length=40, null=True, blank= True)
    email = models.EmailField(null=True, blank= True)
    password = models.CharField(max_length=50)


