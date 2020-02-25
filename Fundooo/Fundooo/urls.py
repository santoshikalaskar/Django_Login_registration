"""Fundooo URL Configuration
"""

# from Fundooo.rest_conf.main import *
from django.contrib import admin
from django.urls import path, include
from Loginregistration import views as user_views
from Note import views as note_view
from django.conf import settings
# import rest_framework 
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Loginregistration.urls')),
    path('api/label/', include('Note.urls')),
    path('oauth/',include('social_django.urls'), name='social'),
    path('api/token/',jwt_views.TokenObtainPairView.as_view(), name='obtain_token_pair'),
    # path('api-auth',include('rest_frameworks.urls')),
    #path('activate/<slug:surl>/', user_views.activate, name='activate'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

