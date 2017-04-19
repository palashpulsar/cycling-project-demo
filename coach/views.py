from django.shortcuts import render
from gpx_file_processing import gpx_extract_info, delete_previous_gpx_files
from stravalib import Client
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import gpx_file_form
from .models import VoiceInstruction, gpxFile

# Create your views here.

"""
STRAVA Section begins here
"""

# Strava Credential
MY_STRAVA_CLIENT_ID = 13223
MY_STRAVA_CLIENT_SECRET = 'de312560924bfc7347c4f3e193ae84b19f149be1'

# Coach login
def login(request):
	port = 8000
	url = 'http://localhost:%d/coach/upload' % port
	client = Client()
	# The following line generates the url to which our application will be redirected.
	url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID,
                               redirect_uri=url)
	return HttpResponseRedirect(url)

# Coach upload of route
def uploadGPX(request):
	# This function's primary task is to upload a GPX file. Additionally, it does the following tasks:
	# 1. Render the upload form.
	# 2. Deletes all previous files and voices.
	# 3. Redirects to mapviz
	code = request.GET.get('code')
	client = Client()
	STORED_ACCESS_TOKEN = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID,
                                              client_secret=MY_STRAVA_CLIENT_SECRET,
                                              code=code)
	client = Client(access_token=STORED_ACCESS_TOKEN)
	coach = client.get_athlete() # Get coach's details

	form = gpx_file_form()
	if request.method == 'POST':
		form = gpx_file_form(request.POST, request.FILES)
		if form.is_valid:
			if len(request.FILES) != 0: # User has entered the file
				delete_previous_gpx_files()
				file = gpxFile(file=request.FILES['docfile'])
				file.save()
				request.session['gpx_data']=gpx_extract_info(file)
				return HttpResponseRedirect("../mapviz")
		else:
			form = gpx_file_form()
	return render(request, 'coach/upload.html', {'form': form, 'coach': coach})

def map_viz(request):
	# This function sends the gpx data for visualization
	gpx_data = request.session.get('gpx_data')
	if request.is_ajax():
		return JsonResponse(gpx_data, safe=False)
	return render(request, 'coach/mapviz.html')