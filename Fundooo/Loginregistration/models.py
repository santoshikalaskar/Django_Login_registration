"""
 ******************************************************************************
 *  Purpose: Login Registration functionality using Django-REST framework.
 *  File  : models.py
 *  Author : Santoshi kalaskar
 ******************************************************************************
"""


from django.db import models
from django import forms
from django.contrib.auth.models import User
 
class Registration(models.Model):
    
    name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    email = models.EmailField()
    password = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'