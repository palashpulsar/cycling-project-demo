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
# A demo for Derek
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Django static
# LINK: https://devcenter.heroku.com/articles/django-assets
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
print "PROJECT_ROOT: ", PROJECT_ROOT
print "BASE_DIR: ", BASE_DIR

# LINK: http://www.bogotobogo.com/python/Django/Python_Django_Image_Files_Uploading_Example.php
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'