from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Label, MyNotes
from .serializers import LabelSerializer, NoteSerializer, NoteUnArchieveSerializer, NoteUnTrashSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
import os, smtplib, jwt, pdb, logging, json
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from rest_framework import mixins
from Fundooo.settings import SECRET_KEY, file_handler
from Loginregistration.redis_instance import redis_instances
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from .pagination import CustomPagination
import datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.ERROR)
logger.addHandler(file_handler)

old_format = '%Y-%m-%dT%H:%M:%S.%f'
new_format = '%d-%m-%Y %H:%M:%S'

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
            sms['message']="unable to list Lables"
            logger.error("unable to list Lables, from get() ")
            return Response(sms, status=400)

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
                sms['message']= "black input label_name"
                logger.error("black input label_name given, from post() ")
                return Response(sms,status=400)
            if Label.objects.filter(user_id = user.id, labelname=label).exists():
                sms['message']= "label already exist"
                logger.error("label already exist ")
                return Response(sms,status=400)
            create_label = Label.objects.create(labelname=label,user_id=user.id)
            sms["success"] = True
            sms['message']= "new label created"
            sms['data'] = request.data
            logger.info(" new label created, successfully...!")
            redis_instances.hmset(str(user.id)+"label",{create_label.id:label})
            print(redis_instances.hgetall(str(user.id)+ "label"))
            return Response(sms, status=201)
        except Exception as e:
            sms["message"] = "something went wrong, while creating label in post()"
            logger.error("something went wrong, while creating label in post() ")
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
    def get_object(self,request, id):
        try:
            user = request.user
            queryset = Label.objects.filter(user_id = user.id)
            return get_object_or_404(queryset,id=id)
        except Label.DoesNotExist:
            sms['message']= "id not present"
            logger.error("Entered Id not present, from get_object() ")
            return Response(sms, status=404)

    def get(self, request, id):
        instance = self.get_object(request,id)
        serializer = LabelSerializer(instance)
        logger.info("List all Labels successfully, from get() ")
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
            label = request.data['labelname']
            instance = self.get_object(request,id)
            serializer = LabelSerializer(instance, data=data)
            if serializer.is_valid():
                update_label = serializer.save()
                sms["success"] = True
                sms['message']= "Label Updated successfully"
                sms['data'] = request.data
                logger.info("Label Updated successfully, from put() ")
                redis_instances.hmset(str(user.id)+"label",{update_label.id:label})
                print(redis_instances.hgetall(str(user.id)+ "label"))
                return Response(sms, status=200)
            sms["success"] = False
            sms['message']= "Label Not Updated, entered data not valied."
            sms['data'] = request.data
            logger.error("Label Not Updated, entered data not valied, from put() ")
            return Response(sms, status=400)
        except:
            sms["success"] = False
            sms['message']= "Label id not present or may be deleted"
            logger.error("Label id not present or may be deleted, from put() ")
            return Response(sms, status=400)
    
    def delete(self, request, id):
        sms = {
            'success': False,
            'message': "Updating Lables",
            'data': [],
        }
        try:
            data= request.data
            user = request.user
            instance = self.get_object(id)
            instance.delete()
            sms["success"] = True
            sms['message']= "Label Deleted successfully"
            sms['data'] = request.data
            logger.info("Label Deleted successfully, from delete() ")
            redis_instances.hdel(str(user.id)+"label",id)
            print(redis_instances.hgetall(str(user.id)+ "label"))
            return Response(sms, status=204)
        except:
            sms["success"] = False
            sms['message']= "Label not deleted"
            sms['data'] = request.data
            logger.error("Label not deleted, from delete() ")
            return Response(sms, status=400)


@method_decorator(login_required(login_url='login'),name='dispatch')
class NoteCreateView(generics.GenericAPIView, 
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin):
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
            notes = MyNotes.objects.filter(user_id = user.id,is_trashed =False, is_archieved=False)
            page = request.GET.get('page', 1)
            paginator = Paginator(notes, 4)
            try:
                notes = paginator.page(page)
            except PageNotAnInteger:
                notes = paginator.page(1)
            except EmptyPage:
                notes = paginator.page(paginator.num_pages)
            serializer = NoteSerializer(notes, many=True)
            logger.info("Notes listed successfully, from get() ")
            return Response(serializer.data, status=200)
        except Exception:
            logger.error("Notes not listed something went wrong, from get() ")
            return Response(serializer.data, status=400)

    def post(self,request):
        data = request.data
        user = request.user
        serializer = NoteSerializer(data=data,partial=True)
        if serializer.is_valid():
            note_create = serializer.save(user_id=user.id)
            logger.info("new note is created, from post() ")
            # setting new Note in redis
            redis_instances.hmset(str(user.id)+ "note", {note_create.id: str(json.dumps(serializer.data))})
            print(redis_instances.hgetall(str(user.id)+ "note"))
            return Response(serializer.data,status=201)
        logger.error("something went wrong while creating new note, from post() ")
        return Response(serializer.data, status=400)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

@method_decorator(login_required(login_url='login'),name='dispatch')
class NoteUpdateView(APIView):
    serializer_class = NoteSerializer
    queryset = MyNotes.objects.all()
    lookup_field = 'id'
    sms = {
            'success': False,
            'message': "Update operations on Note",
            'data': [],
        }
    def get_object(self,request, id):
        try:
            user = request.user
            queryset = MyNotes.objects.filter(user_id = user.id)
            return get_object_or_404(queryset,id=id)
        except MyNotes.DoesNotExist:
            sms['message']= "id not present"
            logger.error("id not present, from get_object() ")
            return Response(sms, status=404)

    def get(self, request, id):
        try:
            user = request.user
            mynote = self.get_object(request, id)
            serializer = NoteSerializer(mynote)
            logger.info("retrieved specific id, from get() ")
            return Response(serializer.data, status=200)
        except Exception:
            logger.error("can't get this id data, from get() ")
            return Response("can't get this id data.", status=400)

    def put(self, request, id):
        sms = {
            'success': False,
            'message': "Updating Note",
            'data': [],
        }
        user = request.user
        try:
            data= request.data
            instance = self.get_object(request, id)
            serializer = NoteSerializer(instance, data=data)
            if serializer.is_valid():
                note_update = serializer.save(user_id=user.id)
                sms["success"] = True
                sms['message']= "Note Updated successfully"
                sms['data'] = request.data
                logger.info("Note Updated successfully, from put() ")
                redis_instances.hmset(str(user.id)+"note",{note_update.id:str(json.dumps(serializer.data))})
                print(redis_instances.hgetall(str(user.id)+ "note"))
                return Response(sms, status=200)
            logger.error("Note Updatedtion failed, from put() ")
            sms['message']= "Note Updatedtion failed"
            return Response(sms, status=400)
        except:
            sms["message"] = "Failed to update Note"
            logger.error("Failed to update Note, from put() ")
            return Response(sms, status=400)

    def delete(self, request, id):
        sms = {
            'success': False,
            'message': "Deleting Note",
            'data': [],
        }
        try:
            data= request.data
            user = request.user
            instance = self.get_object(request,id)
            instance.delete()
            redis_instances.hdel(str(user.id)+"note",id)
            try:
                print(redis_instances.hgetall(str(user.id)+ "note"))
            except:
                print("All note Deleted of %s user",user)
            sms["success"] = True
            sms['message']= "Note Deleted successfully"
            sms['data'] = request.data
            logger.info("Note Deleted successfully, from delete() ")
            return Response(sms, status=204)
        except:
            sms["success"] = False
            sms['message']= "Note not deleted"
            sms['data'] = request.data
            logger.error("Note can't delete, from delete() ")
            return Response(sms, status=400)

@method_decorator(login_required(login_url='login'),name='dispatch')   
class ArchievedNoteView(GenericAPIView):
    serializer_class = NoteSerializer
    queryset = MyNotes.objects.all()
    lookup_field = 'id'

    def get(self, request):
        user = request.user
        try:
            arch_redis_data = redis_instances.hvals(str(user.id)+"is_archieved")
            if len(arch_redis_data) > 0:
                serializer = NoteSerializer(arch_redis_data, many=True)
                return Response(serializer.data, status = 200)
            else:
                arch_db_data = MyNotes.objects.filter(user_id = user.id , is_archieved=True)
                if len(arch_db_data) > 0:
                    serializer = NoteSerializer(arch_db_data, many=True)
                    return Response(serializer.data, status = 200)
                else:
                    return Response(" Archieved data not available ", status = 400)
        except:
            return Response("something bad happend", status = 400)     

@method_decorator(login_required(login_url='login'),name='dispatch')
class TrashedNoteView(GenericAPIView):
    serializer_class = NoteSerializer
    queryset = MyNotes.objects.all()
    lookup_field = 'id'

    def get(self, request):
        user = request.user
        data = request.data
        try:
            arch_redis_data = redis_instances.hvals(str(user.id)+"is_trashed")
            if len(arch_redis_data) > 0:
                serializer = NoteSerializer(arch_redis_data, many=True)
                return Response(serializer.data, status = 200)
            else:
                arch_db_data = MyNotes.objects.filter(user_id = user.id , is_trashed=True)
                if len(arch_db_data) > 0:
                    serializer = NoteSerializer(arch_db_data, many=True)
                    return Response(serializer.data, status = 200)
                else:
                    return Response(" Trashed Note not available ", status = 400)
        except:
            return Response("something bad happend", status = 400)

class UnArchieveNoteView(GenericAPIView):
    serializer_class = NoteUnArchieveSerializer
    queryset = MyNotes.objects.all()
    lookup_field = 'id'
    sms = {
            'success': False,
            'message': "Un archieved Note",
            'data': [],
        }
    def get_object(self,request, id):
        try:
            user = request.user
            queryset = MyNotes.objects.filter(user_id = user.id)
            return get_object_or_404(queryset,id=id)
        except MyNotes.DoesNotExist:
            sms['message']= "id not present"
            logger.error("id not present, from get_object() ")
            return Response(sms, status=404)

    def get(self, request, id):
        try:
            user = request.user
            mynote = self.get_object(request, id)
            serializer = NoteUnArchieveSerializer(mynote)
            logger.info("retrieved specific id, from get() ")
            return Response(serializer.data, status=200)
        except Exception:
            logger.error("can't get this id data, from get() ")
            return Response("can't get this id data.", status=400)

    def put(self, request, id):
        sms = {
            'success': False,
            'message': "Updating Note",
            'data': [],
        }
        user = request.user
        try:
            data= request.data
            instance = self.get_object(request, id)
            serializer = NoteUnArchieveSerializer(instance, data=data)
            if serializer.is_valid():
                note_update = serializer.save(user_id=user.id)
                sms["success"] = True
                sms['message']= "Note UnAnarchieved successfully"
                sms['data'] = request.data
                logger.info("Note UnAnarchieved successfully, from put() ")
                redis_instances.hmset(str(user.id)+"note",{note_update.id:str(json.dumps(serializer.data))})
                print(redis_instances.hgetall(str(user.id)+ "note"))
                return Response(sms, status=200)
            logger.error("Note UnArchieve failed, from put() ")
            sms['message']= "Note Updatedtion failed"
            return Response(sms, status=400)
        except:
            sms["message"] = "Failed to UnArchieve Note"
            logger.error("Failed to UnArchieve Note, from put() ")
            return Response(sms, status=400)

