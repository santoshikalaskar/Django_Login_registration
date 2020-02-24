from django.urls import path, include
from .views import LabelCreateview
from . import views


urlpatterns = [
    path('', views.LabelCreateview.as_view() ,name='create_label'),
    path('<int:id>/', views.LabelUpdateview.as_view() ,name='update_label'),
]