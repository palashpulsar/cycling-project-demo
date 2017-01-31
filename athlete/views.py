from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import gpx_file_form
from .models import gpx_file, gpx_dataObj
import os
import boto3
import time
import json
import csv
from settings.local import MEDIA_ROOT
# from settings.stage import MEDIA_ROOT

# Create your views here.

def test(request):
	gpx_json = gpx_dataObj.objects.all()[0]
	gpx_data = json.loads(gpx_json.data_json)
	# return HttpResponse("Test occurring")
	return JsonResponse(gpx_data, safe=False)

def default(request):
	# LINK: http://stackoverflow.com/questions/1526607/extracting-data-from-a-csv-file-in-python
	# LINK: http://stackoverflow.com/questions/24704630/how-to-upload-and-read-csv-file-in-django-using-csv-dictreader
	# LINK: http://stackoverflow.com/questions/22470637/django-show-validationerror-in-template
	form = gpx_file_form()
	gpx_delete() # There will be only one GPX file, and nothing else
	gpx_dataObj.objects.all().delete()
	if request.method == 'POST':
		form = gpx_file_form(request.POST, request.FILES)
		if form.is_valid:
			if len(request.FILES) != 0: # User has entered the file
				file = gpx_file(docfile=request.FILES['docfile'])
				file.save()
				# dataset = csv_file_extraction(request.FILES['docfile'])
				dataset = csv_file_extraction(file.docfile.path)
				entering_gpx_dataObj(dataset)
				# return HttpResponseRedirect("../mapviz")
				return HttpResponse("Thanks for uploading file.")
		else:
			form = gpx_file_form()
	return render(request, 'athlete/gpx.html', {'form': form})

def entering_gpx_dataObj(dataset, name = "No name"):
	data_json_obj = gpx_dataObj(filename = name,
							data_json = json.dumps(dataset))
	data_json_obj.save()
	return None

def csv_file_extraction(file):
	# LINK: http://stackoverflow.com/questions/14091387/creating-a-dictionary-from-a-csv-file
	# LINK: http://stackoverflow.com/questions/17262256/how-to-read-one-single-line-of-csv-data-in-python
	# LINK: http://stackoverflow.com/questions/2241891/how-to-initialize-a-dict-with-keys-from-a-list-and-empty-value-in-python
	# LINK: http://stackoverflow.com/questions/209840/map-two-lists-into-a-dictionary-in-python
	# LINK: http://stackoverflow.com/questions/1614236/in-python-how-do-i-convert-all-of-the-items-in-a-list-to-floats
	print "I am inside csv_file_extraction function"
	print file
	data = {}
	dataset = []
	with open(file, 'rb') as f:
		data_test = csv.reader(f)
		keys = next(data_test)
		print "keys: ", keys
		print "data: "
		for rows in data_test:
			data = dict(zip(keys, [float(i) for i in rows]))
			print data
			dataset.append(data)
	return None

def map_viz(request):
	# LINK: https://docs.djangoproject.com/en/dev/ref/models/querysets/#latest
	gpx_json = gpx_dataObj.objects.all()[0]
	gpx_data = json.loads(gpx_json.data_json)
	if request.is_ajax():
		return JsonResponse(gpx_data, safe=False)
	return render(request, 'athlete/mapviz.html')

def gpx_delete():
	# LINK: http://stackoverflow.com/questions/30249069/listing-contents-of-a-bucket-with-boto3
	# LINK: http://stackoverflow.com/questions/11426560/amazon-s3-boto-how-to-delete-folder
	gpx_file.objects.all().delete()
	gpx_dataObj.objects.all().delete()
	# Deleting the file from the S3 gpx folder.
	s3 = boto3.resource('s3')
	bucket = s3.Bucket('pace-ire')
	folder = 'gpx/'
	for obj in bucket.objects.filter(Prefix = folder):
		if obj.key != folder:
			obj.delete()

