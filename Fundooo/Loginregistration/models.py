"""
 ******************************************************************************
 *  Purpose: Login Registration functionality using Django-REST framework.
 *  File  : models.py
 *  Author : Santoshi kalaskar
 ******************************************************************************
"""


from django.db import models
from django import forms

class Registration(models.Model):
    
    name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    email = models.EmailField()
    password = models.CharField(max_length = 100)

    def __str__(self):
        return self.name
