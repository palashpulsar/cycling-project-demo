import os
from .base import *
import dj_database_url

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
# Heroku Database (Link: https://devcenter.heroku.com/articles/django-app-configuration):
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# LINK: http://agiliq.com/blog/2014/06/heroku-django-s3-for-serving-media-files/
INSTALLED_APPS += ('storages',)
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = 'pace-ire'
# For media file
# LINK: https://github.com/jamstooks/django-s3-folder-storage
MEDIA_URL = 'http://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = '/media/'
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# Fot static file
STATIC_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
# STATIC_ROOT = '/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
