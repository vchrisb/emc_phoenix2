"""
Django settings for phoenix project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/


ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third pary apps
    'crispy_forms',
    'storages',
    'django_cleanup',
    'djcelery_email',
    'rest_framework',
    'rest_framework.authtoken',
    'captcha',
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.github',
    # my apps
    'content',
    'mytwitter',
    'agenda',
    'vault'
)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

# Authentication backends Setting
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

ROOT_URLCONF = 'phoenix.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'phoenix.wsgi.application'

DATABASES = {'default': dj_database_url.config()}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# Load VCAP_SERVICES
if "VCAP_SERVICES" in os.environ:
    VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
    for group in VCAP_SERVICES:
        for service in VCAP_SERVICES[group]:
            if "ecs" in service['name']:
                AWS_S3_HOST = service['credentials']['HOST']
                AWS_ACCESS_KEY_ID = service['credentials']['ACCESS_KEY_ID']
                AWS_SECRET_ACCESS_KEY = service['credentials']['SECRET_ACCESS_KEY']
                S3_PUBLIC_URL = service['credentials']['PUBLIC_URL']
                STATIC_BUCKET_NAME = service['credentials']['STATIC_BUCKET']
                MEDIA_BUCKET_NAME = service['credentials']['MEDIA_BUCKET']
                SECURE_BUCKET_NAME = service['credentials']['SECURE_BUCKET']

                # add S3 compatible storge
                STATICFILES_STORAGE = 'phoenix.custom_storages.StaticStorage'
                DEFAULT_FILE_STORAGE = 'phoenix.custom_storages.MediaStorage'
                SECURE_FILE_STORAGE = 'phoenix.custom_storages.SecureStorage'

                STATIC_CUSTOM_DOMAIN = '%s.%s' %(STATIC_BUCKET_NAME,S3_PUBLIC_URL)
                STATIC_URL = "http://%s/" % STATIC_CUSTOM_DOMAIN

                MEDIA_CUSTOM_DOMAIN = '%s.%s' %(MEDIA_BUCKET_NAME,S3_PUBLIC_URL)
                MEDIA_URL = "http://%s/" % MEDIA_CUSTOM_DOMAIN

                # django-storages settings
                AWS_AUTO_CREATE_BUCKET = True
                AWS_S3_SECURE_URLS = False
                AWS_QUERYSTRING_AUTH = False

            elif "mail" in service['name']:
                EMAIL_HOST = service['credentials']['HOST']
                EMAIL_HOST_USER = service['credentials']['USER']
                EMAIL_HOST_PASSWORD = service['credentials']['PASSWORD']
                EMAIL_PORT = int(service['credentials']['PORT'])
                if service['credentials']['TLS'] == 'True':
                    EMAIL_USE_TLS = True
                else:
                    EMAIL_USE_TLS = False
            # sendgrid does override "mail" and will use sendgrid web API
            elif "sendgrid" in service['name']:
                CELERY_EMAIL_BACKEND = "sgbackend.SendGridBackend"
                SENDGRID_USER = service['credentials']['username']
                SENDGRID_PASSWORD = service['credentials']['password']

            elif "rabbitmq" in service['name']:
                BROKER_URL = service['credentials']['uri']
                EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

                CELERY_EMAIL_TASK_CONFIG = {
                    'rate_limit': '100/m',  # * CELERY_EMAIL_CHUNK_SIZE (default: 10) limit to X per minute
                }

                if "cloudamqp" in VCAP_SERVICES[group]:
                    # https://www.cloudamqp.com/docs/celery.html
                    BROKER_POOL_LIMIT = 1 # Will decrease connection usage
                    BROKER_HEARTBEAT = 30 # Will detect stale connections faster
                    BROKER_CONNECTION_TIMEOUT = 30 # May require a long timeout due to Linux DNS timeouts etc
                    CELERY_RESULT_BACKEND = None
                    CELERY_SEND_EVENTS = False # Will not create celeryev.* queues
                    CELERY_EVENT_QUEUE_EXPIRES = 60 # Will delete all celeryev. queues without consumers after 1 minute.

            elif "twitter" in service['name']:
                TWITTER_CONSUMER_KEY = service['credentials']['CONSUMER_KEY']
                TWITTER_CONSUMER_SECRET = service['credentials']['CONSUMER_SECRET']
                TWITTER_ACCESS_TOKEN = service['credentials']['ACCESS_TOKEN']
                TWITTER_ACCESS_TOKEN_SECRET = service['credentials']['ACCESS_TOKEN_SECRET']

            elif "config" in service['name']:
                SECRET_KEY = service['credentials']['SECRET_KEY']
                if service['credentials']['DEBUG'] == 'True':
                    DEBUG = True
                else:
                    DEBUG = False
                DEFAULT_FROM_EMAIL = service['credentials']['DEFAULT_FROM_EMAIL']
                DEFAULT_TO_EMAIL = service['credentials']['DEFAULT_TO_EMAIL']
                SERVER_EMAIL = service['credentials']['SERVER_EMAIL']
                ADMINS = service['credentials']['ADMINS']
else:
    # for development, don't run migrations!
    DEBUG = True
    SECRET_KEY = "DEVELOPMENT"
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    SECURE_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    # custom_storages.py is referenced in migrations
    STATIC_BUCKET_NAME = None
    STATIC_CUSTOM_DOMAIN = None
    MEDIA_BUCKET_NAME = None
    MEDIA_CUSTOM_DOMAIN = None
    SECURE_BUCKET_NAME = None

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_custom'),
)

# crispy
CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = not DEBUG

# REST
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'PAGE_SIZE': 25
}

#captcha
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'

# allauth
ACCOUNT_ADAPTER = "phoenix.adapter.AccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_FORM_CLASS = 'phoenix.forms.SignupForm'
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
ACCOUNT_USERNAME_MIN_LENGTH = 6
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_AUTO_SIGNUP = False
#SOCIALACCOUNT_QUERY_EMAIL = False
SOCIALACCOUNT_PROVIDERS = \
    {
    'github':
        {   'SCOPE': ['user:email'],
            'VERIFIED_EMAIL': True,
        },
    'facebook':
        {#'METHOD': 'js_sdk',
            'SCOPE': ['email', 'public_profile'],
            'VERIFIED_EMAIL': True,
        },
    }
LOGIN_REDIRECT_URL = '/'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
#1h task limit
CELERYD_TASK_TIME_LIMIT = 3600

# django-resized
DJANGORESIZED_DEFAULT_SIZE = [1024, 1024]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True

# restrict access to certain domains
ALLOWED_DOMAINS = ['emc.com', 'vmware.com', 'vce.com', 'rsa.com', 'virtustream.com']
