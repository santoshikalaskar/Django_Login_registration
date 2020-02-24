from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Label

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['labelname']
