import boto3
import csv
from .models import gpx_file, gpx_dataObj

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

def csv_extraction(development, filename):
	print "I am inside csv_extraction function."
	print "filename: ", filename
	file = None
	data = {}
	dataset = []
	s3 = boto3.resource('s3')
	bucket = s3.Bucket('pace-ire')
	folder = 'gpx/'
	for obj in bucket.objects.filter(Prefix = folder):
		if development == 'local':
			if obj.key != folder:
				file = obj
		elif development == 'stage':
			if obj.key == filename:
				file = obj
	csv_file = file.get()['Body'].read()
	string_csvData = csv.reader(csv_file.split())
	dataList_string = list(string_csvData)
	keys = dataList_string[0]
	del dataList_string[0]
	print "keys: ", keys
	for rows in dataList_string:
		data = dict(zip(keys, [float(i) for i in rows]))
		print data
		dataset.append(data)
	return dataset