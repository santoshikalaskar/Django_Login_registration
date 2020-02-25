from django.urls import path, include
from .views import LabelCreateview,NoteCreateView,NoteUpdateView
from . import views


urlpatterns = [
    path('label/', views.LabelCreateview.as_view() ,name='create_label'),
    path('label/<int:id>/', views.LabelUpdateview.as_view() ,name='update_label'),
    path('note/', views.NoteCreateView.as_view() ,name='create_note'),
    path('note/<int:id>/', views.NoteUpdateView.as_view() ,name='Update_note'),
]