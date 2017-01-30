from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.

class gpx_file(models.Model):
	docfile = models.FileField(upload_to='gpx/')

class gpx_dataObj(models.Model):
	filename = models.CharField(max_length=30, null = True)
	data_json = JSONField()
