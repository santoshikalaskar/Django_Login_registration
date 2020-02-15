"""
 ******************************************************************************
 *  Purpose: Login Registration functionality using Django-REST framework.
 *  File  :view.py
 *  Author :Santoshi kalaskar
 ******************************************************************************
"""

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Registration
from .serializers import RegistrationSerializer, LoginSerializer,EmailSerializer,ResetPassSerializer
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
from django.core.mail import send_mail
import os, smtplib, jwt, pdb, logging, json
from Fundooo.settings import EMAIL_HOST_USER, SECRET_KEY, file_handler

#seting log
logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

def activate(request, surl): 
    try:
        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)

        # if user is not none then user account will be activated
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


class RegistrationAPIview(GenericAPIView):

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
         # if Entered email_id not valied  show error
        try:
            validate_email(email)
        except Exception as e:
            sms['message'] = "please enter vaild email address"
            logger.error("error: %s while as email entered was not a vaild email address", str(e))
            return HttpResponse(json.dumps(sms), status=400)

         # if user input is black show error
        if username == "" or email == "" or password1 == "" or password2 == "":
            sms['message'] = "one of the details missing, please enter carefully."
            logger.error("one of the details missing while registration process.")
            return HttpResponse(json.dumps(sms), status=400)

        # if email already exists it will show error message
        elif User.objects.filter(email=email).exists():
            sms['message'] = "email address is already registered, please enter other Email_Id!"
            logger.error("email address is already registered registration process")
            return HttpResponse(json.dumps(sms), status=400)
        
        # if both passwords not matches then show error message
        elif not password1 == password2:
            sms['message'] = "Both password is not matched, please password enter carefully !"
            logger.error("email address is already registered registration process")
            return HttpResponse(json.dumps(sms), status=400)

        # else valied details then create New user after Registration processes   
        else:
            try:
                user_created = User.objects.create_user(username=username, email=email, password=password1,
                                                        is_active=False)
                user_created.save()
                if user_created is not None:
                    # call create token and short it and send to email id.
                    token = str(token_activation(username,password1))
                    short_url = get_surl(token)
                    short_token = short_url.split("/")[2]
                    mail_subject = "Activate your account by clicking below link..!"
                    mail_message = render_to_string('Loginregistration/email_validation.html', {
                        'user': user_created.username,
                        'domain': get_current_site(request).domain,
                        'short_token': short_token,
                    })
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
            # if above conditions are failed then return error
            except Exception as e:
                sms["success"] = False
                sms["message"] = "username already taken"
                logger.error("error: %s while registration ", str(e))
                return HttpResponse(json.dumps(sms), status=400)

# for login user
class LoginAPIview(GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request):
        return render(request, 'Loginregistration/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticate entered details while login
        user = authenticate(username=username, password=password)
        # if valied user and check its status is active or not, if yes then allowed to login
        if user:
            if user.is_active:
                login(request,user)
                logger.info("user logged in successfully..user-> {}!".format(username))
                return HttpResponse("<h1>Your account is successfully Logged in...!</h1>")
            else:
                logger.error("Failed, to login,account was inactive")
                return HttpResponse("<h1>Your account was inactive.</h1>")
        else:
            logger.error("Failed, Not the Registered username or password")
            logger.error("They used username: {} and password: {}".format(username,password))
            return HttpResponse("<h1>Invalid login details given</h1>")  

# forgotpassword call 
class ForgotPasswordAPIview(GenericAPIView):
    serializer_class = EmailSerializer

    def get(self, request):
        return render(request, 'Loginregistration/forgotpassword.html')

    def post(self, request):
        email = request.POST.get('email')
        sms = {
            'success': False,
            'message': "password not set yet ",
            'data': []
        }
        # if email value is empty while forgot password return error 
        if email == "":
            sms['message'] = 'email field is empty please provide vaild input'
            logger.error('email field is empty please provide vaild input')
            return HttpResponse(json.dumps(sms), status=400)
        # else validate entered mail & filter mail is exists or not
        else:
            try:
                validate_email(email)
            except Exception:
                sms['message'] = 'email field value is not vaild input, please provide valid email id.'
                logger.error('email field value is not vaild input')
                return HttpResponse(json.dumps(sms) ,status=400)
            try:
                query_user = User.objects.filter(email=email)
                useremail = query_user.values()[0]["email"]
                username = query_user.values()[0]["username"]
                id = query_user.values()[0]["id"]

                # generate token while forgot password reset process
                if useremail is not None:
                    token = str(token_activation(username, id))
                    surl = get_surl(token)
                    short_token = surl.split("/")[2]

                    # email send to user for reset their password.
                    mail_subject = "Reset your account Password by clicking below link..!"
                    mail_message = render_to_string('Loginregistration/reset_pass_token.html', {
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
                sms['message'] = "something went wrong, please try again."
                logger.error("something went wrong")
                return HttpResponse(json.dumps(sms), status=400)             

# after clicking rest_password link of email by user
def reset_password(request, surl):
    try:
        # decode token & fetch username from it
        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)

        # if username is not none then we will fetch the data and redirect to the reset password page
        if user is not None:
            logger.info(request, 'user is valid email')
            return redirect('/api/resetpassword/' + str(user))
        else:
            logger.error(request, 'User is not found with this mail id')
            return redirect('/api/forgotpass')
    except KeyError:
        logger.error(request, 'was not able to sent the email, try again.')
        return redirect('/api/forgotpass')
    except Exception as e:
        logger.error(request, 'activation link expired')
        return redirect('/api/forgotpass')

# reset password page
class ResetPasswordAPIview(GenericAPIView):
    serializer_class = ResetPassSerializer
    
    # enter new password
    def post(self, request, user_name):
        password = request.data['password']
        sms = {
            'success': False,
            'message': 'password reset not done',
        }
        # username is null throw error
        if user_name is None:
            sms['message'] = 'not a vaild user'
            logger.error('not a vaild user')
            return Response(sms, status=404)

        # if new entered password is null throw error. 
        elif password == "":
            sms['message'] = 'New password not entered'
            logger.error('New password not entered')
            return Response(sms, status=400)

        # if entered password has charactor less than 7 throw error
        elif len(password) <= 7:
            sms['message'] = 'password should be grater than 7 dicharacters.'
            logger.error('New password less than 7 characters')
            return Response(sms, status=400)
        
        # else match this username & set password to that user
        else:
            try:
                user = User.objects.get(username=user_name)
                user.set_password(password)
                user.save()
                sms = {
                    'success': True,
                    'message': 'password reset done successfully.'
                }
                logger.info('New password set successfully..!')
                return Response(sms, status=201)
            except User.DoesNotExist:
                smd['message'] = 'not a vaild user '
                logger.error('User does not exits.')
                return HttpResponse(sms, status=400)

