from django.contrib import admin
from .models import gpxFile, VoiceInstruction

# Register your models here.
admin.site.register(gpxFile)
admin.site.register(VoiceInstruction)


