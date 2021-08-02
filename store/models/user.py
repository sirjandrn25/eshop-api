from django.db import models
from django.contrib.auth.models import AbstractUser,User
from .abstract import *
from store.managers import *


class User(AbstractUser,DateTimeTracker):
    username = None
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=150,unique=True)
    is_customer = models.BooleanField(default=True)
    contact_no = models.CharField(max_length=15)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Profile(models.Model):
    global gender_choices
    address = models.CharField(max_length=200,blank=True)
    avatar = models.ImageField(upload_to="avatar/",null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    gender = models.CharField(max_length=10,choices=gender_choices,default=gender_choices[0][0])
    def __str__(self):
        return self.user.full_name


