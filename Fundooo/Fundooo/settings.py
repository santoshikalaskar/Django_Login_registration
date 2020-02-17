"""
Django settings for Fundooo project.

Generated by 'django-admin startproject' using Django 3.0.3.
"""

import os, logging
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# #Logging 
log_filename = "logs/output.log"
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
formatter = logging.Formatter('%(levelname)s :%(asctime)s :%(pathname)s :%(lineno)s :%(message)s')
file_handler = logging.FileHandler(filename=log_filename)
file_handler.setFormatter(formatter)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-(=-50iklh+r^mtl_lmwe%k&(w!&%-$ak=1*a$-c)rcj!vnq)9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # thired-party apps
    'rest_framework',
    'django_short_url',
    'social_django',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    #Local-apps
    'Loginregistration',



]

AUTHENTICATION_BACKENDS=[
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    # 'django.account.auth_backends.AuthenticationBackend',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'Fundooo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'Fundooo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'loginapp',
        'USER': 'santoshi',
        'PASSWORD': 'testing321',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
  ),
}
#AUTH_USER_MODEL = 'user.User'
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [ 
#         'rest_framework.permissions.IsAuthenticated',
#     ],
#     "DEFAULT_PARSER_CLASSES": [
#         "rest_framework.parsers.JSONParser", 
#     ],
#     "DEFAULT_AUTHENTICATION_CLASSES": 
#     [                              # new
#         "rest_framework.authentication.SessionAuthentication",        # new
#         "rest_framework_simplejwt.authentication.JWTAuthentication"  # new 
#     ],
# }

# JWT_AUTH = {
#   'JWT_ENCODE_HANDLER':
#   'rest_framework_jwt.utils.jwt_encode_handler',
#   'JWT_DECODE_HANDLER':
#   'rest_framework_jwt.utils.jwt_decode_handler',
#   'JWT_PAYLOAD_HANDLER':
#   'rest_framework_jwt.utils.jwt_payload_handler',
#   'JWT_PAYLOAD_GET_USER_ID_HANDLER':
#   'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
#   'JWT_RESPONSE_PAYLOAD_HANDLER':
#   'rest_framework_jwt.utils.jwt_response_payload_handler',
 
#   'JWT_SECRET_KEY': 'SECRET_KEY',
#   'JWT_GET_USER_SECRET_KEY': None,
#   'JWT_PUBLIC_KEY': None,
#   'JWT_PRIVATE_KEY': None,
#   'JWT_ALGORITHM': 'HS256',
#   'JWT_VERIFY': True,
#   'JWT_VERIFY_EXPIRATION': True,
#   'JWT_LEEWAY': 0,
#   'JWT_EXPIRATION_DELTA': timedelta(days=3),
#   'JWT_AUDIENCE': None,
#   'JWT_ISSUER': None,
#   'JWT_ALLOW_REFRESH': False,
#   'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=3),
#   'JWT_AUTH_HEADER_PREFIX': 'Bearer',
#   'JWT_AUTH_COOKIE': None,
# }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# email settings
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD=os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER=os.environ.get('EMAIL_HOST_USER')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


LOGIN_REDIRECT_URL = 'home'
# LOGOUT_REDIRECT_URL = 'home'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '17490015860-6ncn7fpig453to983k6acvr68893qmp1.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET ='DAx-i3AsOCu4RSBnLFk8Ot8p'

SOCIAL_AUTH_GITHUB_KEY = '686f469f289e33c55149'
SOCIAL_AUTH_GITHUB_SECRET = '7b1e72f40834f5084607181e162f626f7c88568e'

SOCIAL_AUTH_FACEBOOK_KEY = '195122904882696'
SOCIAL_AUTH_FACEBOOK_SECRET = '91f71cfb401a07f2001f474efc0f0f73'

SITE_ID =1 