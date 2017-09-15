"""
Django settings for quizwhiz project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'asupersecretquizwhizsecretwith&%!characters'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'easy_thumbnails',
    'mptt',
    'filer',
    'ckeditor',
    'ckeditor_filebrowser_filer',
    'gfklookupwidget',
    'widget_tweaks',
    'django_s3_storage',

    'quizard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'quizwhiz.urls'

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
                'quizard.context_processors.quizard_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'quizwhiz.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
# EMAIL_HOST_USER = 'Define me in local_settings.py.'
# EMAIL_HOST_PASSWORD = 'Define me in local_settings.py.'
EMAIL_PORT = 25

# +------------------------------------------------------------------------------------------------+
# |                                                                                                |
# |                                    django.contrib.messages                                     |
# |                                                                                                |
# +------------------------------------------------------------------------------------------------+
# Change default message tags to things that bootstrap recognizes.
# https://docs.djangoproject.com/en/1.11/ref/contrib/messages/#message-tags
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


# +------------------------------------------------------------------------------------------------+
# |                                                                                                |
# |                                     logging configuration                                      |
# |                                                                                                |
# +------------------------------------------------------------------------------------------------+

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/../logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# +------------------------------------------------------------------------------------------------+
# |                                                                                                |
# |                                    ckeditor configuration                                      |
# |                                                                                                |
# +------------------------------------------------------------------------------------------------+

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_Full': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo',
             'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['FilerImage', 'Iframe', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], ['Source'],
        ],
        'toolbar': 'Full',
        'height': 200,
        'extraPlugins': 'filerimage',
    }
}

# +------------------------------------------------------------------------------------------------+
# |                                                                                                |
# |                                        django-filer                                            |
# |                                                                                                |
# +------------------------------------------------------------------------------------------------+

FILER_ENABLE_PERMISSIONS = True
FILER_PAGINATE_BY = 50

# +------------------------------------------------------------------------------------------------+
# |                                                                                                |
# |                                           boto                                                 |
# |                                                                                                |
# +------------------------------------------------------------------------------------------------+

AWS_REGION = 'us-west-2'
# AWS_ACCESS_KEY_ID = 'Define me in local_settings.py.'
# AWS_SECRET_ACCESS_KEY = 'Define me in local_settings.py.'
AWS_S3_ADDRESSING_STYLE = 'auto'
AWS_S3_BUCKET_AUTH = False
AWS_S3_BUCKET_NAME = 'quizwhiz.io'
AWS_S3_CUSTOM_DOMAIN = "{bucket}.s3.amazonaws.com".format(bucket=AWS_S3_BUCKET_NAME)
AWS_S3_GZIP = True

# +------------------------------------------------------------------------------------------------+
# |                                                                                                |
# |                              django media storage settings                                     |
# |                                                                                                |
# +------------------------------------------------------------------------------------------------+

# This comes after 'boto' because it depends on AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
MEDIA_URL = "//{media_domain}/".format(media_domain=AWS_S3_CUSTOM_DOMAIN)

# +------------------------------------------------------------------------------------------------+
# |                                                                                                |
# |                                          quizard                                               |
# |                                                                                                |
# +------------------------------------------------------------------------------------------------+

BRAND_NAME = 'QuizWhiz'  # The brand this instance of quizard should present itself as.
DOMAIN_NAME = 'quizwhiz.io'  # The canonical domain name on which this quizard instance is deployed.

# This is actually a Django setting, but we're making it depend on the
# quizard-specific DOMAIN_NAME setting above.
DEFAULT_FROM_EMAIL = "webmaster@{domain}".format(domain=DOMAIN_NAME)

# +------------------------------------------------------------------------------------------------+
# |                                                                                                |
# |                Local settings. Don't declare any settings beyond this point.                   |
# |                                                                                                |
# +------------------------------------------------------------------------------------------------+

try:
    from local_settings import *
except ImportError as e:
    print e

# Add the EC2 instance's private IPv4 address to ALLOWED_HOSTS
# so that health checks from the ALB will succeed.
import requests

# Amazon maintains a REST API for retrieving instance metadata.
response = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4')

# If the response isn't 200, maybe the server wasn't provisioned with AWS?
# Anyways, the request wasn't successful, so don't do anything with the response.
if response.status_code == 200:
    ALLOWED_HOSTS.append(response.text)


