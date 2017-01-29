from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import gpx_file_form
from .models import gpx_file, gpx_dataObj
import gpxpy
from vincenty import vincenty
import os
import boto3
import time
import json
# from settings.stage import MEDIA_ROOT

# Create your views here.

def test(request):
	gpx_json = gpx_dataObj.objects.all()[0]
	gpx_data = json.loads(gpx_json.data_json)
	# return HttpResponse("Test occurring")
	return JsonResponse(gpx_data, safe=False)

def default(request):
	form = gpx_file_form()
	gpx_delete() # There will be only one GPX file, and nothing else
	if request.method == 'POST':
		form = gpx_file_form(request.POST, request.FILES)
		if form.is_valid:
			if len(request.FILES) != 0: # User has entered the file
				file = gpx_file(docfile=request.FILES['docfile'])
				file.save()

				# LINK: http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
				# start = time.time()
				# request.session['gpx_data']=gpx_extract_info(file)
				# end = time.time()
				# print "Time taken for fist function is: ", (end - start)

				# start = time.time()
				# gpx_ext_info(file)
				# end = time.time()
				# print "Time taken for second function is: ", (end - start)

				# return HttpResponseRedirect("../mapviz")
				return HttpResponse("Thanks for uploading file.")
		else:
			form = gpx_file_form()
	# LINK: http://stackoverflow.com/questions/22470637/django-show-validationerror-in-template
	return render(request, 'athlete/gpx.html', {'form': form})

def map_viz(request):
	# LINK: https://docs.djangoproject.com/en/dev/ref/models/querysets/#latest
	gpx_json = gpx_dataObj.objects.all()[0]
	gpx_data = json.loads(gpx_json.data_json)
	if request.is_ajax():
		return JsonResponse(gpx_data, safe=False)
	return render(request, 'athlete/mapviz.html')

def gpx_delete():
	gpx_file.objects.all().delete()
	gpx_dataObj.objects.all().delete()
	# Deleting the file from the S3 gpx folder.
	s3 = boto3.resource('s3')
	bucket = s3.Bucket('pace-ire')
	folder = 'gpx/'
	# LINK: http://stackoverflow.com/questions/30249069/listing-contents-of-a-bucket-with-boto3
	for obj in bucket.objects.filter(Prefix = folder):
		if obj.key != folder:
			# LINK: http://stackoverflow.com/questions/11426560/amazon-s3-boto-how-to-delete-folder
			obj.delete()

def gpx_extract_info(gpx_file):
	# Identifying the location of the gpx file
	gpx = gpxpy.parse(gpx_file.docfile)
	t = 0
	gpx_data = {}
	gpx_data['latitude'] = []
	gpx_data['longitude'] = []	
	gpx_data['elevation'] = []
	gpx_data['distance'] = [] 
	for track in gpx.tracks:
		for segment in track.segments:
			for point in segment.points:
				gpx_data['latitude'].append(point.latitude)
				gpx_data['longitude'].append(point.longitude)
				gpx_data['elevation'].append(point.elevation)
				t = t+1
	# Calculating the distance
	for i in range(len(gpx_data['latitude'])):
		if(i==0):
			gpx_data['distance'].append(0)
		else:
			boston = (gpx_data['latitude'][i-1], gpx_data['longitude'][i-1])
			newyork = (gpx_data['latitude'][i], gpx_data['longitude'][i])
			gpx_data['distance'].append(gpx_data['distance'][i-1] + vincenty(boston, newyork))
	return gpx_data

def gpx_ext_info(gpx_file):
	gpx = gpxpy.parse(gpx_file.docfile)
	data = {}
	dataset = []
	init = 1
	lat_init = None
	lon_init = None
	dis_init = None
	for track in gpx.tracks:
		for segment in track.segments:
			for point in segment.points:
				data['lat'] = point.latitude
				data['lon'] = point.longitude
				data['ele'] = point.elevation
				if init == 1:
					data['dis'] = 0
					lat_init = data['lat']
					lon_init = data['lon']
					dis_init = data['dis']
					init = 0
				else:
					boston = (lat_init, lon_init)
					newyork = (data['lat'], data['lon'])
					data['dis'] = vincenty(boston, newyork) + dis_init
					lat_init = data['lat']
					lon_init = data['lon']
					dis_init = data['dis']
				dataset.append(data.copy()) # LINK: http://stackoverflow.com/questions/5244810/python-appending-a-dictionary-to-a-list-i-see-a-pointer-like-behavior
	gpx_data = gpx_dataObj(data_json = json.dumps(dataset))
	gpx_data.save()
	return None
