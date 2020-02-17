"""
 ******************************************************************************
 *  Purpose: Login Registration functionality using Django-REST framework.
 *  File  : urls.py
 *  Author :Santoshi kalaskar
 ******************************************************************************
"""

from django.urls import path, include
from .views import RegistrationAPIview,ForgotPasswordAPIview,ResetPasswordAPIview
from . import views

urlpatterns = [
	path('',views.home, name="home"),
    path('registration/', views.RegistrationAPIview.as_view(),name="registration" ),
    path('login/', views.LoginAPIview.as_view(),name="login" ),
    path('forgotpassword/', views.ForgotPasswordAPIview.as_view(), name="forgotpass"),
    path('activate/<surl>',views.activate, name="activate"),
    path('reset_password/<surl>/', views.reset_password, name="reset_password"),
    path('resetpassword/<user_name>', views.ResetPasswordAPIview.as_view(), name="resetpassword")
]


