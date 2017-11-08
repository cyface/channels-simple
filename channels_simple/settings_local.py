"""
Django settings for project - Local Overrides

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# pylint: disable=W0614,W0401,W0123

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

try:
    from .settings import *
except ImportError:
    pass

DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'channels_db',
        'PORT': 5432,
    }
}

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.99.100']
