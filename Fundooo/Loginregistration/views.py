"""
 ******************************************************************************
 *  Purpose: Login Registration functionality using Django-REST framework.
 *  File  :view.py
 *  Author :Santoshi kalaskar
 ******************************************************************************
"""


from django.shortcuts import render, redirect
import logging, json
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from .models import Registration
from .serializers import RegistrationSerializer, LoginSerializer,EmailSerializer
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.validators import validate_email
from django.urls import reverse
from .token import token_activation
from .sendmail import send_mail_to_recipients
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import pdb
from django.core.mail import send_mail
import os
import smtplib
import jwt
#from jwt import ExpiredSignatureError
from django.contrib import messages
from Fundooo.settings import EMAIL_HOST_USER, SECRET_KEY, file_handler

logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

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
            logger.error("error: %s while as email entered was not a vaild email address", str(e))
            return HttpResponse(json.dumps(sms), status=400)

         # user input is checked
        if username == "" or email == "" or password1 == "" or password2 == "":
            sms['message'] = "one of the details missing, please enter carefully."
            logger.error("one of the details missing while registration process.")
            return HttpResponse(json.dumps(sms), status=400)

        # if email exists it will show error message
        elif User.objects.filter(email=email).exists():
            sms['message'] = "email address is already registered, please enter other Email_Id!"
            logger.error("email address is already registered registration process")
            return HttpResponse(json.dumps(sms), status=400)
        
        # if both password not matches then show error message
        elif not password1 == password2:
            sms['message'] = "Both password is not matched, please password enter carefully !"
            logger.error("email address is already registered registration process")
            return HttpResponse(json.dumps(sms), status=400)

        # create New user    
        else:
            try:
                user_created = User.objects.create_user(username=username, email=email, password=password1,
                                                        is_active=False)
                user_created.save()
                if user_created is not None:
                    token = str(token_activation(username,password1))
                    short_url = get_surl(token)
                    short_token = short_url.split("/")[2]
                    mail_subject = "Activate your account by clicking below link..!"
                    mail_message = render_to_string('Loginregistration/email_validation.html', {
                        'user': user_created.username,
                        'domain': get_current_site(request).domain,
                        'short_token': short_token,
                        # 'token':token
                    })
                    # print(mail_message)
                    recipient_email = user_created.email
                    subject, from_email, to = mail_subject, EMAIL_HOST_USER, recipient_email
                    #email = EmailMessage(mail_subject, mail_message, to=[recipient_email])
                    text_content = 'This is an important message.'
                    html_content = mail_message
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    sms = {
                        'success': True,
                        'message': 'please check the mail and click on the link  for validation',
                        'data': [token],
                    }
                    logger.info("email was sent to %s email address ", username)
                    return HttpResponse('<h1>please check the mail and click on the link  for validation</h1>', status=201)
            except Exception as e:
                sms["success"] = False
                sms["message"] = "username already taken"
                logger.error("error: %s while registration ", str(e))
                return HttpResponse(json.dumps(sms), status=400)


class LoginAPIview(GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request):
        return render(request, 'Loginregistration/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponse("<h1>Your account is successfully Logged in...!</h1>")
            else:
                return HttpResponse("<h1>Your account was inactive.</h1>")
        else:
            logger.error("Failed, Not the Registered username or password")
            logger.error("They used username: {} and password: {}".format(username,password))
            return HttpResponse("<h1>Invalid login details given</h1>")  

class ForgotPasswordView(GenericAPIView):

    serializer_class = EmailSerializer

    def get(self, request):
        return render(request, 'Loginregistration/forgotpassword.html')
    # pdb.set_trace()
    def post(self, request):
        email = request.POST.get('email')
        response = {
            'success': False,
            'message': "not a vaild email ",
            'data': []
        }

        if email == "":
            response['message'] = 'email field is empty please provide vaild input'
            logger.error('email field is empty please provide vaild input')
            return HttpResponse(json.dumps(response), status=400)
        else:
            try:
                validate_email(email)
            except Exception:
                response['message'] = 'email field value is not vaild input, please provide valid email id.'
                logger.error('email field value is not vaild input')
                return HttpResponse(json.dumps(response) ,status=400)
            try:
                query_user = User.objects.filter(email=email)
                useremail = query_user.values()[0]["email"]
                username = query_user.values()[0]["username"]
                id = query_user.values()[0]["id"]

                if useremail is not None:
                    token = token_activation(username, id)
                    url = str(token)
                    surl = get_surl(url)
                    short_token = surl.split("/")[2]

                    # email is generated  where it is sent the email address entered in the form
                    mail_subject = "Reset your account Password by clicking below link"
                    mail_message = render_to_string('Loginregistration/email_validation.html', {
                        'user': username,
                        'domain': get_current_site(request).domain,
                        'short_token': short_token
                    })

                    recipient_email = email

                    subject, from_email, to = mail_subject, EMAIL_HOST_USER, recipient_email
                    #email = EmailMessage(mail_subject, mail_message, to=[recipient_email])
                    text_content = 'This is an important message.'
                    html_content = mail_message
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    sms = {
                        'success': True,
                        'message': 'please check the mail and click on the link  for Reset password',
                        'data': [token],
                    }
                    logger.info("email was sent to %s email address ", username)
                    return HttpResponse('<h1>please check the mail and click on the link  for Reseting your password</h1>', status=201)

            except Exception as e:
                print(e)
                response['message'] = "something went wrong, please try again."
                logger.error("something went wrong")
                return HttpResponse(json.dumps(response), status=400)             

def activate(request, surl): 
    try:
        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)

        # if user is not none then user account willed be activated
        if user is not None:
            user.is_active = True
            user.save()
            logger.info(request, "your account is active now")
            return redirect('/api/login')
        else:
            logger.info(request, 'not able to sent the email')
            return redirect('/api/registration')
    except KeyError:
        logger.info(request, 'was not able to sent the email')
        return redirect('/api/registration')

