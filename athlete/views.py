from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from .forms import gpx_file_form
from .models import gpx_file, gpx_dataObj, geoLocation
from .processingFunctions import deletePreviousFiles, csv_file_extraction, entering_gpx_dataObj
from django.middleware.csrf import get_token
import json
import os
# Create your views here.

def uploadCSV(request):
	# This function's primary task is to upload a CSV file. Additionally, it does the following tasks:
	# 1. Render the upload form.
	# 2. Deletes all previous files and voices.
	# 3. Redirects to mapviz
	form = gpx_file_form()
	if request.method == 'POST':
		form = gpx_file_form(request.POST, request.FILES)
		if form.is_valid:
			if len(request.FILES) != 0: # User has entered the file
				deletePreviousFiles()
				file = gpx_file(docfile=request.FILES['docfile'])
				file.save()
				dataset = csv_file_extraction(os.path.join(settings.MEDIA_ROOT, str(file.docfile)))
				print dataset
				entering_gpx_dataObj(dataset, str(file.docfile))
				return HttpResponseRedirect("../mapviz")
				# return HttpResponse("Thanks for uploading file")
		else:
			form = gpx_file_form()
	return render(request, 'athlete/gpx.html', {'form': form})


def map_viz(request):
	# This function sends the gpx data for visualization
	gpx_json = gpx_dataObj.objects.all()[0]
	gpx_data = json.loads(gpx_json.data_json)
	if request.is_ajax():
		return JsonResponse(gpx_data, safe=False)
	return render(request, 'athlete/mapviz.html')


# The following two functions need to be tested later.
def fillingGeolocation(request):
	print "request: ", request
	if request.method == 'POST':
		if request.is_ajax():
			lat = float(request.POST.get('lat'))
			lon = float(request.POST.get('lon'))
			print "latitude: ", lat, "longitude: ", lon, "csrfmiddlewaretoken: ", request.POST.get('csrfmiddlewaretoken')
			new_geo = geoLocation(latitude=lat, longitude=lon)
			new_geo.save()
	return HttpResponse("Filling up the geolocation table")

def retrievingDrivenGeolocation(request):
	if request.is_ajax():
		drivenGeoLocation = {}
		drivenGeoLocation['latitude'] = []
		drivenGeoLocation['longitude'] = []
		geoLocation_objs = geoLocation.objects.all()
		for obj in geoLocation_objs:
			drivenGeoLocation['latitude'].append(obj.latitude)
			drivenGeoLocation['longitude'].append(obj.longitude)
		print "drivenGeoLocation: ", drivenGeoLocation
		return JsonResponse(drivenGeoLocation)
	return None



