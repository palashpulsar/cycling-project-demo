from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from athlete.models import gpx_dataObj
from audio import previousVoiceLocations
import json

# Create your views here.

def cheer_interface(request):
	print "We are in cheer_template function."
	csv_obj = gpx_dataObj.objects.all()[0]
	if request.is_ajax():
		return JsonResponse(json.loads(csv_obj.data_json), safe=False)
	return render(request, 'audience/cheer_interface.html')
	# return HttpResponse("You are in cheering page")

def voiceHistory(request):
	# This function determines the 'distances' of previously saved voices
	# Collect the location of all previously saved
	distance = previousVoiceLocations()
	print distance
	return JsonResponse(distance, safe=False)
