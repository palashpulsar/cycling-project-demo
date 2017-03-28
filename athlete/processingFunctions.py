import boto3
import csv
from .models import gpx_file, gpx_dataObj
import os
from audience.models import VoiceInstruction
from .models import gpx_file, gpx_dataObj, geoLocation
from django.conf import settings
import json

def gpx_delete():
	gpx_file.objects.all().delete()
	gpx_dataObj.objects.all().delete()
	# Deleting the file from the S3 gpx folder.
	s3 = boto3.resource('s3')
	bucket = s3.Bucket('pace-ire')
	folder = 'gpx/'
	for obj in bucket.objects.filter(Prefix = folder):
		if obj.key != folder:
			obj.delete()
	return None

def csv_file_extraction(file):
	print "I am inside csv_file_extraction function"
	print "CSV file: ", file
	data = {}
	dataset = []
	with open(file, 'rb') as f:
		data_test = csv.reader(f)
		keys = next(data_test)
		print "keys: ", keys
		print "data: "
		for rows in data_test:
			data = dict(zip(keys, [float(i) for i in rows]))
			dataset.append(data)
	return dataset


def deletePreviousFiles():
	# Deleting other CSV files in gpx/ folder
	# There will be one CSV (GPX later) file at a time
	gpx_file.objects.all().delete()
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

def entering_gpx_dataObj(dataset, filename = "No name"):
	print "len(dataset): ", len(dataset)
	data_json_obj = gpx_dataObj(filename = filename,
							data_json = json.dumps(dataset))
	data_json_obj.save()
	return