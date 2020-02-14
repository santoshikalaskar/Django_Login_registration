"""
 ******************************************************************************
 *  Purpose: Login Registration functionality using Django-REST framework.
 *  File  : serializers.py
 *  Author :Santoshi kalaskar
 ******************************************************************************
"""


from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Registration
#from validate_email import validate_email


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


    




