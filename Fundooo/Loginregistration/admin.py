"""
 ******************************************************************************
 *  Purpose: Login Registration functionality using Django-REST framework.
 *  File  : admin.py
 *  Author :Santoshi kalaskar
 ******************************************************************************
"""


from django.contrib import admin
from .models import Registration, Profile
from .forms import RegistrationForm

class RegisterAdmin(admin.ModelAdmin):
    list_display = '__all__'
    form = RegistrationForm

admin.site.register(Registration)
admin.site.register(Profile)