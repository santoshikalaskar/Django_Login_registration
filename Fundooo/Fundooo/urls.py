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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # new
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]


#     path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
