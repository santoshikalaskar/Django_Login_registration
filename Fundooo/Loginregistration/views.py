from django.shortcuts import render
import logging, json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from .models import Registration
from .serializers import RegistrationSerializer, LoginSerializer
from django.contrib.auth.forms import UserChangeForm 
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.validators import validate_email
from django.urls import reverse
from .token import token_activation
from .sendmail import send_mail_to_recipients
from django.core.mail import EmailMessage
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import pdb
from django.core.mail import send_mail
import os
import smtplib

print(os.environ.get('EMAIL_HOST_USER'))
print(os.environ.get('EMAIL_HOST_PASSWORD'))
# Create your views here.

class RegistrationAPIview(GenericAPIView):

    #serializer_class = UserSerializer
    serializer_class = RegistrationSerializer
    def get(self, request):
        return render(request, 'Loginregistration/registration.html')

    def post(self, request):
        username = request.data['username']
        email = request.data['email']
        password1 = request.data['password1']
        password2 = request.data['password2']
        sms = {
            'success': False,
            'message': "not registered yet",
            'data': [],
        }
        try:
            validate_email(email)
        except Exception as e:
            sms['message'] = "please enter vaild email address"
            logging.error("error: %s while as email entered was not a vaild email address", str(e))
            return HttpResponse(json.dumps(sms), status=400)

         # user input is checked
        if username == "" or email == "" or password1 == "" or password2 == "":
            sms['message'] = "one of the details missing, please enter carefully."
            logging.error("one of the details missing while registration process.")
            return HttpResponse(json.dumps(sms), status=400)

        # if email exists it will show error message
        elif User.objects.filter(email=email).exists():
            sms['message'] = "email address is already registered, please enter other Email_Id!"
            logging.error("email address is already registered registration process")
            return HttpResponse(json.dumps(sms), status=400)
        
        # if both password not matches then show error message
        elif not password1 == password2:
            sms['message'] = "Both password is not matched, please password enter carefully !"
            logging.error("email address is already registered registration process")
            return HttpResponse(json.dumps(sms), status=400)

        # create New user    
        else:
            try:
                user_created = User.objects.create_user(username=username, email=email, password=password1,
                                                        is_active=True)
                user_created.save()
                # print("1111111", user_created)
                # user is unique then we will send token to his/her email for validation
                if user_created is not None:
                    token = str(token_activation(username, password1))
                    # print("22222222222",token)
                    short_url = get_surl(token)
                    # print("4444444",short_url)
                    short_token = short_url.split("/")[2]
                    # print(short_token)

                    # sending email for activation
                    # pdb.set_trace()
                    mail_subject = "Activate your account by clicking below link..!"
                    mail_message = render_to_string('Loginregistration/email_validation.html', {
                        'user': user_created.username,
                        'domain': get_current_site(request).domain,
                        'short_token': short_token
                    })
                    # print(mail_message)
                    recipient_email = user_created.email
                  
                    # email = EmailMessage(mail_subject, mail_message, to=[recipient_email])
                    send_mail_to_recipients(mail_subject, mail_message,recipient_email)
                    email.send()
                    return Response("Please check your mail.")
            except Exception as e:
                sms["success"] = False
                sms["message"] = "username already taken, Please choose other unique username."
                logging.error("error: %s while Registration ", str(e))
                return HttpResponse(json.dumps(sms), status=400)


        print(username,email,password1,password2,sms)
        return HttpResponse("till .. done..")

    
#  mail_subject = "Activate your account by clicking below link"
#                     mail_message = render_to_string('user/email_validation.html', {
#                         'user': user_created.username,
#                         'domain': get_current_site(request).domain,
#                         'surl': z[2]
#                     })
#                     recipient_email = user_created.email
#                     email = EmailMessage(mail_subject, mail_message, to=[recipient_email])
#                     email.send()
#                     smd = {
#                         'success': True,
#                         'message': 'please check the mail and click on the link  for validation',
#                         'data': [token],
#                     }
#                     logger.info("email was sent to %s email address ", username)
#                     return HttpResponse(json.dumps(smd), status=201)
#             except Exception as e:
#                 smd["success"] = False
#                 smd["message"] = "username already taken"
#                 logger.error("error: %s while loging in ", str(e))
#                 return HttpResponse(json.dumps(smd), status=400)