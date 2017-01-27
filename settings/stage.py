import os
from .base import *
import dj_database_url

INSTALLED_APPS += ('storages',)

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
# A demo for Derek
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# LINK: http://offbytwo.com/2012/01/18/deploying-django-to-heroku.html
# https://devcenter.heroku.com/articles/s3-upload-python
# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID'] #"AKIAIX6IMI5Q5Z2UM4FQ"
AWS_ACCESS_KEY_ID = "AKIAIX6IMI5Q5Z2UM4FQ"
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'] #"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"
AWS_SECRET_ACCESS_KEY = "e+aqK+eUkmXtXsdK3yFxrmKHBnh3WWHT5tHvBztn"
# AWS_PASSWORD = "){87y*VE(B[0"
AWS_STORAGE_BUCKET = 'pace-stage'
AWS_S3_CUSTOM_DOMAIN = "pace-stage.s3-website.eu-central-1.amazonaws.com"
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# LINK: http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'