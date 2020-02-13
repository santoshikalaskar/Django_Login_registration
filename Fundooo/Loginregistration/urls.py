
from django.urls import path, include
from .views import RegistrationAPIview
# from rest_framework_simplejwt import views as jwt_views
# from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('registration/', views.RegistrationAPIview.as_view(),name="registration" ),
    # path('login/', views.Login.as_view(), name="login"),


]


# urlpatterns = [


#     # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
#     path('forgotpassword', views.ForgotPassword.as_view(),name="forgotPassword"),
#     path('activate/<surl>/', views.activate, name="activate"),
#     path('reset_password/<surl>/', views.reset_password, name="reset_password"),
#     path('resetpassword/<user_reset>', views.ResetPassword.as_view(), name="resetpassword"),
#     path('logout/', views.Logout.as_view() ,name="logout"),
