# LINK: https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/

from django.conf import settings
from .stage import STATICFILES_LOCATION, MEDIAFILES_LOCATION
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
	location = STATICFILES_LOCATION

class MediaStorage(S3Boto3Storage):
	location = MEDIAFILES_LOCATION