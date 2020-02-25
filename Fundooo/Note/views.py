from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Label, MyNotes
from .serializers import LabelSerializer, NoteSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
import os, smtplib, jwt, pdb, logging, json
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from rest_framework import mixins

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

@method_decorator(login_required(login_url='login'),name='dispatch')
class LabelUpdateview(LoginRequiredMixin,APIView):
    serializer_class = LabelSerializer
    lookup_field = 'id'
    sms = {
            'success': False,
            'message': "Updating Lables",
            'data': [],
        }
    def get_object(self, id):
        try:
            queryset = Label.objects.all()
            return get_object_or_404(queryset,id=id)
        except Label.DoesNotExist:
            sms['message']= "id not present"
            return Response(sms, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id=id)
        serializer = LabelSerializer(instance)
        return Response(serializer.data)

    def put(self, request, id):
        sms = {
            'success': False,
            'message': "Updating Lables",
            'data': [],
        }
        user = request.user
        try:
            data= request.data
            instance = self.get_object(id)
            serializer = LabelSerializer(instance, data=data)
            if serializer.is_valid():
                serializer.save()
                sms["success"] = True
                sms['message']= "Label Updated successfully"
                sms['data'] = request.data
                return Response(sms, status=200)
            sms["success"] = False
            sms['message']= "Label Not Updated successfully"
            sms['data'] = request.data
            return Response(sms, status=400)
        except:
            sms["success"] = False
            sms['message']= "Label id not present or may be deleted"
            return Response(sms, status=400)
    
    def delete(self, request, id):
        sms = {
            'success': False,
            'message': "Updating Lables",
            'data': [],
        }
        try:
            data= request.data
            instance = self.get_object(id)
            instance.delete()
            sms["success"] = True
            sms['message']= "Label Deleted successfully"
            sms['data'] = request.data
            return Response(sms, status=204)
        except e:
            sms["success"] = False
            sms['message']= "Label not deleted"
            sms['data'] = request.data
            return Response(sms, status=400)
        

@method_decorator(login_required(login_url='login'),name='dispatch')
class NoteCreateView(generics.GenericAPIView, 
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin):
    serializer_class = NoteSerializer
    queryset = MyNotes.objects.all()
    lookup_field = 'id'

    sms = {
            'success': False,
            'message': "listing Notes",
            'data': [],
    }
    def get(self, request):
        try:
            user = request.user
            mynote = MyNotes.objects.filter(user_id = user.id)
            serializer = NoteSerializer(mynote, many=True)
            return Response(serializer.data, status=200)
        except Exception:
            return Response(serializer.data, status=400)

    def post(self,request):
        data = request.data
        user = request.user
        serializer = NoteSerializer(data=data,partial=True)
        if serializer.is_valid():
            serializer.save(user_id=user.id)
            return Response(serializer.data,status=201)
        return Response(serializer.data, status=400)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

@method_decorator(login_required(login_url='login'),name='dispatch')
class NoteUpdateView(generics.GenericAPIView, 
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin):
    serializer_class = NoteSerializer
    queryset = MyNotes.objects.all()
    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request,id)
    
    def put(self,request, id):
        return self.update(request, id)
    
    def delete(self,request,id):
        return self.destroy(request,id)

    # def perform_update(self, serializer):
    #     serializer.save(user = self.request.user)

    # def perform_destroy(self, instance):
    #     return super().perform_destroy(instance)

    
    