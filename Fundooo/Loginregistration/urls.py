
from django.urls import path, include
from .views import RegistrationAPIview
from . import views

urlpatterns = [
    path('registration/', views.RegistrationAPIview.as_view(),name="registration" ),
    path('login/', views.LoginAPIview.as_view(),name="login" ),
    path('activate/<surl>', views.activate, name="activate"),
    # path('login/', views.Login.as_view(), name="login"),
]


