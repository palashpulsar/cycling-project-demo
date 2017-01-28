import os
from .base import *
import dj_database_url
import custom_storages

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

INSTALLED_APPS += ('storages',)
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = 'pace-ire'

#LINK: https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
# For media file
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s.s3.amazonaws.com/%s/" % (AWS_STORAGE_BUCKET_NAME, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

# For static file
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATIC_URL = "https://%s.s3.amazonaws.com/%s/" % (AWS_STORAGE_BUCKET_NAME, STATICFILES_LOCATION)