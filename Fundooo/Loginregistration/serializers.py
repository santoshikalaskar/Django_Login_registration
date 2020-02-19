"""
 ******************************************************************************
 *  Purpose: Login Registration functionality using Django-REST framework.
 *  File  : serializers.py
 *  Author :Santoshi kalaskar
 ******************************************************************************
"""


from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Registration, Profile
#from validate_email import validate_email


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        
class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class ResetPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']


    




