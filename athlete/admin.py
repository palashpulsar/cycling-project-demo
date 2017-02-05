from django.contrib import admin
from .models import gpx_file, gpx_dataObj, geoLocation
# Register your models here.

admin.site.register(gpx_file)
admin.site.register(gpx_dataObj)
admin.site.register(geoLocation)

