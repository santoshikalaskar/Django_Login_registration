from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Label
from .serializers import LabelSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
import os, smtplib, jwt, pdb, logging, json
from django.contrib.auth.mixins import LoginRequiredMixin

@method_decorator(login_required(login_url='login'),name='dispatch')
class LabelCreateview(LoginRequiredMixin,APIView):
    # login_url = 'login'
    #redirect_field_name = '/n'

    serializer_class = LabelSerializer

    def get(self, request):
        sms = {
            'success': False,
            'message': "listing Lables",
            'data': [],
        }
        try:
            user = request.user
            labels = Label.objects.filter(user_id = user.id)
            serializer = LabelSerializer(labels, many=True)
            return Response(serializer.data, status=200)
        except Exception:
            return Response(serializer.data, status=400)

    def post(self, request):
        user = request.user

        sms = {
            'success': False,
            'message': "creating Lables",
            'data': [],
        }
        try:
            label = request.data['labelname']
            if label == "":
                sms['message']= "black input"
                return Response(sms,status=400)
            if Label.objects.filter(user_id = user.id, labelname=label).exists():
                sms['message']= "label already exist"
                return Response(sms,status=400)
            create_label = Label.objects.create(labelname=label,user_id=user.id)
            sms["success"] = True
            sms['message']= "new label created"
            sms['data'] = request.data
            return Response(sms, status=201)
        except Exception as e:
            sms["message"] = "something went wrong"
            return HttpResponse(sms, status=400)




