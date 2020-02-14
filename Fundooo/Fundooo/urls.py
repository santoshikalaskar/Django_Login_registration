"""Fundooo URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from Loginregistration import views as user_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework_simplejwt import views as jwt_views
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Loginregistration.urls')),
    #path('activate/<slug:surl>/', user_views.activate, name='activate'),
]

