from __future__ import unicode_literals

from django.db import models

# Create your models here.
class VoiceInstruction(models.Model):
	distance = models.FloatField()
	position_of_distance = models.PositiveIntegerField()
	latitude = models.DecimalField(max_digits=9, decimal_places=6)
	longitude = models.DecimalField(max_digits=9, decimal_places=6)
	voice = models.FileField(upload_to='sound/', null=True)
	# For detecting if voice has been played or not.
	voice_status = models.PositiveSmallIntegerField()
	# 1: Voice has already been played
	# 0: Voice has not yet been played
