from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import gpx_file_form
from .models import gpx_file
import gpxpy
from vincenty import vincenty
import os
from settings.base import MEDIA_URL

# Create your views here.
def default(request):
	form = gpx_file_form()
	gpx_delete() # There will be only one GPX file, and nothing else
	if request.method == 'POST':
		form = gpx_file_form(request.POST, request.FILES)
		if form.is_valid:
			if len(request.FILES) != 0: # User has entered the file
				file = gpx_file(docfile=request.FILES['docfile'])
				file.save()
				request.session['gpx_data']=gpx_extract_info(file)			
				return HttpResponseRedirect("../mapviz")
		else:
			form = gpx_file_form()
	# LINK: http://stackoverflow.com/questions/22470637/django-show-validationerror-in-template
	return render(request, 'athlete/gpx.html', {'form': form})

def map_viz(request):
	# LINK: https://docs.djangoproject.com/en/dev/ref/models/querysets/#latest
	gpx_data = request.session.get('gpx_data')
	if request.is_ajax():
		return JsonResponse(gpx_data)
	return render(request, 'athlete/mapviz.html')

def gpx_delete():
	gpx_file.objects.all().delete()
	path_gpx = os.path.join(MEDIA_URL, 'gpx')
	print MEDIA_URL, " -> MEDIA_URL"
	print "I AM HERE"
	for the_file in os.listdir(path_gpx):
		file_path = os.path.join(path_gpx, the_file)
		if not file_path.endswith('.txt'):
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
			except Exception as e:
				print(e)

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

