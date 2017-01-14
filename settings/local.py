import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pace_strategy',
        'USER': 'palashsarkar',
		'PASSWORD': 'FinLanD666',
		'HOST': '',
		'PORT': '',
    }
}