from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Label, MyNotes
from drf_extra_fields.fields import Base64ImageField

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['labelname']

class NoteSerializer(serializers.ModelSerializer):
    # image=Base64ImageField()
    class Meta:
        model = MyNotes
        fields = ['title','note','image','is_archieved','is_trashed','is_pinned','remender','color','label','collabrator']