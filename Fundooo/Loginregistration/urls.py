"""
 ******************************************************************************
 *  Purpose: Login Registration functionality using Django-REST framework.
 *  File  : urls.py
 *  Author :Santoshi kalaskar
 ******************************************************************************
"""

from django.urls import path, include
from .views import RegistrationAPIview,ForgotPasswordAPIview,ResetPasswordAPIview,ProfileUpdateAPIview
from . import views

urlpatterns = [
	path('',views.home, name="home"),
    path('registration/', views.RegistrationAPIview.as_view(),name="registration" ),
    path('login/', views.LoginAPIview.as_view(),name="login" ),
    path('profile/', views.profileView, name="profile"),
    path('forgotpassword/', views.ForgotPasswordAPIview.as_view(), name="forgotpass"),
    path('activate/<surl>',views.activate, name="activate"),
    path('reset_password/<surl>/', views.reset_password, name="reset_password"),
    path('resetpassword/<user_name>/', views.ResetPasswordAPIview.as_view(), name="resetpassword"),
    path('updateprofile/', views.ProfileUpdateAPIview.as_view(), name="updateprofile"),
    path('logout/', views.LogoutAPIview ,name="logout"),
    #path('api-auth/', include('rest_framework.urls')),
]

