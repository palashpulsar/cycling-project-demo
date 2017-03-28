import boto3
import csv
from .models import gpx_file, gpx_dataObj
import os

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