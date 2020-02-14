"""
 ******************************************************************************
 *  Purpose: Login Registration functionality using Django-REST framework.
 *  File  : urls.py
 *  Author :Santoshi kalaskar
 ******************************************************************************
"""



from django.urls import path, include
from .views import RegistrationAPIview,ForgotPasswordView
from . import views

urlpatterns = [
    path('registration/', views.RegistrationAPIview.as_view(),name="registration" ),
    path('login/', views.LoginAPIview.as_view(),name="login" ),
    path('forgotpassword/', views.ForgotPasswordView.as_view(), name="forgotpass"),
    path('activate/<surl>',views.activate, name="activate")
    # path('login/', views.Login.as_view(), name="login"),
]


