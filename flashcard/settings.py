"""
Django settings for flashcard project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from datetime import datetime, timedelta
import os
import sys

# import sensitive information and be sure to have SECRET_KEY setup
from .settings_secret import (  # noqa: F401
    SECRET_KEY,
    DEBUG,
    DATABASES_PSQL_NAME, DATABASES_PSQL_USER, DATABASES_PSQL_PASSWORD,
    DATABASES_PSQL_HOST, DATABASES_PSQL_PORT,
    EMAIL_DEBUG, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD,
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    AWS_STATIC_BUCKET_URL,
    AWS_TEST_MEDIA_BUCKET_NAME, AWS_MEDIA_BUCKET_NAME,
    AWS_TEST_MEDIA_CLOUDFRONT_URL, AWS_MEDIA_CLOUDFRONT_URL,
    AWS_SES_REGION_NAME, AWS_SES_REGION_ENDPOINT, AWS_SES_RETURN_PATH,
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG mode defined in settings_secret.py

ADMINS = [
    ('Noddy', 'nceruchalu@gmail.com'),
]
MANAGERS = ADMINS

ALLOWED_HOSTS = ['.nnoduka.com', '.flashcard.nnoduka.com', '.localhost']

# A tuple of IP addresses, as strings, that:
# - Show debug comments, when DEBUG is True
# - Receive X headers in admindocs if the XViewMiddleware is installed
# - See the Debug Toolbar
if DEBUG:
    ALLOWED_HOSTS += ['127.0.0.1', '.ngrok.io', '*']
    INTERNAL_IPS = ['127.0.0.1', '::1', 'localhost']


# ------------------------------------------------------------------------------
# Application definition
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'storages',
    'accounts.apps.AccountsConfig',
    'cards.apps.CardsConfig',
]

MIDDLEWARE = [
    'common.middleware.WebfactionFixes',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flashcard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates').replace('\\', '/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'flashcard.wsgi.application'


# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASES_PSQL_NAME,
        'USER': DATABASES_PSQL_USER,
        'PASSWORD': DATABASES_PSQL_PASSWORD,
        'HOST': DATABASES_PSQL_HOST,
        'PORT': DATABASES_PSQL_PORT,
    }
}


# ------------------------------------------------------------------------------
# Password validation
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa: E501
        'OPTIONS': {
            'user_attributes': ('email', 'first_name', 'last_name'),
        },
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator'),
    },
]


# ------------------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


# ------------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.1/howto/static-files/

if DEBUG:
    STATIC_URL = '/static/'
else:
    STATIC_URL = AWS_STATIC_BUCKET_URL

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static').replace('\\', '/'),
]


# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.1/topics/logging/

# This logging configuration does the following:
# - identifies the configuration as being in `dictConfig version 1` format.
# - defines 3 formatters:
#   + dango.server, that outputs the server time and the log message
#   + simple, that just outputs the log level name and the log message.
#   + verbose, that outputs the log level name, the  log message, plus the time,
#     process, thread and module that generate the log message.
#
# - defines 2 filters:
#   + require_debug_true, DEBUG must be True for a handler to be called
#   + require_debug_false, DEBUG must be False for a handler to be called
#
# - defines 5 handlers:
#   + console, a StreamHandler, which will print any DEBUG (or higher) message
#     to stderr. This handler uses the simple output format.
#   + django.server, a StreamHandler which will print any INFO (or higher)
#     message to stderr.
#   + mail_admins, an AdminEmailHandler, which will email any ERROR (or higher)
#     message to the site admins,
#   + syslog, a SysLogHandler, which will send any DEBUG (or higher) message
#     to syslog.
#   + loggly_https, an HTTPSHandler, which will send any DEBUG (or higher)
#     message to Loggly Gen2 HTTPS endpoint.
#
# - configures 4 loggers:
#   + django, which passes all messages at ERROR or higher to the mail_admins
#     handler when not in DEBUG mode. In debug mode this logger passes messages
#     to the console handler.
#   + django.server, which passes all messages at INFO or higher to the
#     django.server handler
#   + loggly_logs, which passes all messages at DEBUG or higher to the syslog
#     handler when not in DEBUG mode. In debug mode this logger passes messages
#     to the console handler.
#   + loggly_https, which passes all messages at DEBUG or higher to the loggly
#     HTTPs handler when not in DEBUG mode. In debug mode this logger passes
#      messages to the console handler.
#

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
         },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'  # noqa: E501
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local7',
            'formatter': 'simple',
            'address': (('localhost', 514) if sys.platform == 'darwin' else
                        '/dev/log'),
        },
        'loggly_https': {
            'level': 'DEBUG',
            'class': 'loggly.handlers.HTTPSHandler',
            'formatter': 'simple',
            'url': 'https://logs-01.loggly.com/inputs/598d7b10-f650-46cf-b9cc-43648619f6cf/tag/django',  # noqa: E501
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'loggly_logs': {
            'handlers': ['syslog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'loggly_https': {
            'handlers': ['loggly_https'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

if DEBUG:
    # make all loggers but django.server use the console handler.
    for logger in LOGGING['loggers']:
        if logger != 'django.server':
            LOGGING['loggers'][logger]['handlers'] = ['console']

# loggly logger name (tcnpayment.loggly.com)
LOGGER_NAME_LOGGLY = 'loggly_https'


# ---------------------------------------------------------------------------- #
# Email settings
# ---------------------------------------------------------------------------- #
if EMAIL_DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django_ses.SESBackend'

# The email addressed used in the 'from' fields have to be
# <email>@nnoduka.com or <email>@<subdomain>.nnoduka.com as
# the nnoduka.com domain should be verified on AWS
DEFAULT_FROM_EMAIL = 'Noddy <support@nnoduka.com>'

SERVER_EMAIL = 'Noddy Server <postmaster@nnoduka.com>'


# ---------------------------------------------------------------------------- #
# Amazon AWS storage settings
# ---------------------------------------------------------------------------- #
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_S3_USE_SSL = not DEBUG

# Specify AWS S3 bucket to upload files to
if DEBUG:
    AWS_STORAGE_BUCKET_NAME = AWS_TEST_MEDIA_BUCKET_NAME
else:
    AWS_STORAGE_BUCKET_NAME = AWS_MEDIA_BUCKET_NAME

AWS_REDUCED_REDUNDANCY = True

# Cache ref: http://www.mobify.com/blog/beginners-guide-to-http-cache-headers/
expires = datetime.now() + timedelta(days=365)
AWS_HEADERS = {
    'Expires': expires.strftime('%a, %d %b %Y 20:00:00 GMT'),
    'Cache-Control': 'public, max-age=31536000, s-maxage=31536000',
}

# Read files from AWS cloudfront (requires using s3boto storage backend)
if DEBUG:
    AWS_S3_CUSTOM_DOMAIN = AWS_TEST_MEDIA_CLOUDFRONT_URL
else:
    AWS_S3_CUSTOM_DOMAIN = AWS_MEDIA_CLOUDFRONT_URL


# ------------------------------------------------------------------------------
# Debug Toolbar settings
# ------------------------------------------------------------------------------
DEBUG_TOOLBAR_PATCH_SETTINGS = False

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '{static_url}js/jquery-3.3.1.min.js'.format(
        static_url=STATIC_URL)
}


# ------------------------------------------------------------------------------
# Project-level settings
# ------------------------------------------------------------------------------
# The maximum size in bytes that a request body may be before a
# SuspiciousOperation (RequestDataTooBig) is raised
DATA_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024  # 25MB

# max image file size: 25MB
MAX_IMAGE_SIZE = 25 * 1024 * 1024

# max uploaded file size: 25MB
MAX_FILE_SIZE = 25 * 1024 * 1024


# ------------------------------------------------------------------------------
# `accounts` settings
# ------------------------------------------------------------------------------
# specify custom user model
AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'


# ------------------------------------------------------------------------------
# `cards` settings
# ------------------------------------------------------------------------------
CARDS_PAGE_SIZE = 5
