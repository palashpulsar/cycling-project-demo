from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import VoiceInstruction 

# Create your views here.

def voice_save_del(request):
	print "We are in voice_save_del() function"
	if request.method == 'POST':
		if request.is_ajax():
			print "A POST ajax request is made."
			new_voice = VoiceInstruction(distance=request.POST.get('dis_Mark'), 
											position_of_distance=request.POST.get('dis_Mark_Pos'),  
											latitude=request.POST.get('dis_lat'), 
											longitude=request.POST.get('dis_lon'),
											voice_status=0,)
			new_voice.save()
			return HttpResponse('Successful Update of voice instruction')
	return HttpResponse("Voice should be saved")

def previousVoiceLocations():
	distance = []
	voice_obj = VoiceInstruction.objects.all()
	for obj in voice_obj:
		distance.append(obj.distance)
	return distance

