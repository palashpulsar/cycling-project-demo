import gpxpy
from vincenty import vincenty
import os
from .models import VoiceInstruction, gpxFile, geoLocation
from django.conf import settings

def gpx_extract_info(gpx_file):
	# Identifying the location of the gpx file
	gpx = gpxpy.parse(gpx_file.file)
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

def delete_previous_gpx_files():
	# Deleting other CSV files in gpx/ folder
	# There will be one CSV (GPX later) file at a time
	gpxFile.objects.all().delete()
	VoiceInstruction.objects.all().delete()
	geoLocation.objects.all().delete()
	path_gpx = os.path.join(settings.MEDIA_ROOT, 'gpx')
	path_voice = os.path.join(settings.MEDIA_ROOT, 'sound')
	for the_file in os.listdir(path_gpx):
		file_path = os.path.join(path_gpx, the_file)
		try:
			if os.path.isfile(file_path):
				if file_path.split('.')[1] != 'txt':
					os.unlink(file_path)
		except Exception as e:
			print(e)
	for voice_file in os.listdir(path_voice):
		file_path = os.path.join(path_voice, voice_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print e
	return