from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from .forms import gpx_file_form
from .models import gpx_file, gpx_dataObj, geoLocation
from audience.models import VoiceInstruction
from .amazonS3 import gpx_delete, csv_file_extraction
from django.middleware.csrf import get_token
import json
import os
# Create your views here.

def uploadCSV(request):
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
				# entering_gpx_dataObj(dataset, str(file.docfile))
				# return HttpResponseRedirect("../mapviz")
				return HttpResponse("Thanks for uploading file")
		else:
			form = gpx_file_form()
	return render(request, 'athlete/gpx.html', {'form': form})

def deletePreviousFiles():
	# Deleting other CSV files in gpx/ folder
	# There will be one CSV (GPX later) file at a time
	gpx_dataObj.objects.all().delete()
	VoiceInstruction.objects.all().delete()
	geoLocation.objects.all().delete()
	path_gpx = os.path.join(settings.MEDIA_ROOT, 'gpx')
	for the_file in os.listdir(path_gpx):
		file_path = os.path.join(path_gpx, the_file)
		try:
			if os.path.isfile(file_path):
				if file_path.split('.')[1] != 'txt':
					os.unlink(file_path)
		except Exception as e:
			print(e)
	return

def test(request):
	gpx_json = gpx_dataObj.objects.all()[0]
	gpx_data = json.loads(gpx_json.data_json)
	# return HttpResponse("Test occurring")
	return JsonResponse(gpx_data, safe=False)

def default_local(request):
	form = gpx_file_form()
	# gpx_delete() # There will be only one GPX file, and nothing else
	gpx_dataObj.objects.all().delete()
	VoiceInstruction.objects.all().delete()
	geoLocation.objects.all().delete()
	if request.method == 'POST':
		form = gpx_file_form(request.POST, request.FILES)
		if form.is_valid:
			if len(request.FILES) != 0: # User has entered the file
				file = gpx_file(docfile=request.FILES['docfile'])
				file.save()
				dataset = csv_extraction('local', str(file.docfile))
				entering_gpx_dataObj(dataset, str(file.docfile))
				return HttpResponseRedirect("../mapviz")
				# return HttpResponse("Thanks for uploading file.")
		else:
			form = gpx_file_form()
	return render(request, 'athlete/gpx.html', {'form': form})

def entering_gpx_dataObj(dataset, filename = "No name"):
	print "len(dataset): ", len(dataset)
	data_json_obj = gpx_dataObj(filename = filename,
							data_json = json.dumps(dataset))
	data_json_obj.save()
	return None

def map_viz(request):
	gpx_json = gpx_dataObj.objects.all()[0]
	gpx_data = json.loads(gpx_json.data_json)
	if request.is_ajax():
		return JsonResponse(gpx_data, safe=False)
	return render(request, 'athlete/mapviz.html')

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



