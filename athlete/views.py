from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import gpx_file_form
from .models import gpx_file, gpx_dataObj
import gpxpy
from geopy.distance import great_circle
import os
import boto3
import time
import json
import csv
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
				csv_file_extraction(file)
				# return HttpResponseRedirect("../mapviz")
				return HttpResponse("Thanks for uploading file.")
		else:
			form = gpx_file_form()
	# LINK: http://stackoverflow.com/questions/22470637/django-show-validationerror-in-template
	return render(request, 'athlete/gpx.html', {'form': form})

def csv_file_extraction(file):
	print "I am inside csv_file_extraction function"
	data = {}
	dataset = []
	print type(file)
	# LINK: http://stackoverflow.com/questions/1526607/extracting-data-from-a-csv-file-in-python
	for d in csv.DictReader(open(file), delimiter=','):
		print d
		# counts.append(int(d['Counts']))
		# frequencies.append(int(d['frequency']))
	return None

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

