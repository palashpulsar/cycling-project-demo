from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import VoiceInstruction 
import pyaudio
# NOTE: http://stackoverflow.com/questions/33513522/when-installing-pyaudio-pip-cannot-find-portaudio-h-in-usr-local-include
import wave
import tempfile
from django.conf import settings
from django.core.files import File
import os

# Create your views here.

def record(request):

	tf = tempfile.NamedTemporaryFile(dir = os.path.join(settings.MEDIA_ROOT, 'recordedVoice'), prefix="temporary_", suffix = ".wav", delete = False)
	path_to_temporary_audio = tf.name
	print "path_to_temporary_audio: ", path_to_temporary_audio

	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	CHUNK = 1024	
	RECORD_SECONDS = 5

	audio = pyaudio.PyAudio()
 
	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
						rate=RATE, input=True,
						frames_per_buffer=CHUNK)
	print "recording..."
	frames = []
 
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	print "finished recording"

	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()

	waveFile = wave.open(path_to_temporary_audio, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()
	# print "get_default_output_device_info(): ", audio.get_default_output_device_info()
	# device_count = audio.get_device_count()
	# print "device_count: ", device_count
	request.session['temporary_audio_file'] = path_to_temporary_audio
	print "File is saved somewhere."
	return HttpResponse("Voice to be recorded")

def play(request):
	# Works only with google chrome.
	path_to_temporary_audio = request.session.get('temporary_audio_file')
	filename_url = {}
	filename_url['url'] = path_to_temporary_audio[len(settings.BASE_DIR):]
	if request.is_ajax():
		return JsonResponse(filename_url)	
	return HttpResponse("Voice to be played")

def save(request):
	path_to_temporary_audio = request.session.get('temporary_audio_file')
	if request.method == 'POST':
		if request.is_ajax():
			dis_Mark = request.POST.get('dis_Mark')
			previous_distances = previousVoiceLocations()
			# HOW TO AVOID DUPLICATE SAVINGS OF AUDIO??
			# print type(dis_Mark)
			# if float(dis_Mark) not in previous_distances:
			# 	print "This is a new entry"
			# else:
			# 	print "AN already entry exst. Cannot override."
			# for entry in previous_distances:
			# 	print type(entry)
			dis_Mark_Pos = request.POST.get('dis_Mark_Pos')
			dis_lat = request.POST.get('dis_lat')
			dis_lon = request.POST.get('dis_lon')
			voice = python_to_django_file_conversion(path_to_temporary_audio)
			voice_rename = modify_filename(voice, dis_Mark_Pos)
			new_voice = VoiceInstruction(voice=voice_rename, 
											distance=dis_Mark, 
											position_of_distance=dis_Mark_Pos, 
											voice_status=0, 
											latitude=dis_lat, 
											longitude=dis_lon)
			new_voice.save()
			print "voice file path is %r" % new_voice.voice.path
			os.remove(path_to_temporary_audio)
	return HttpResponse("Voice to be saved")

def previousVoiceLocations():
	distance = []
	voice_obj = VoiceInstruction.objects.all()
	for obj in voice_obj:
		distance.append(obj.distance)
	return distance

def python_to_django_file_conversion(python_file):
	f = open(python_file)
	django_file = File(f)
	return django_file

def modify_filename(filename, mark):
	# NOTE: http://stackoverflow.com/questions/25652809/django-file-upload-and-rename
	ext = filename.name.split('.')[-1]
	file_rename = "%s_%s.%s" % ("voice", str(mark), ext)
	filename.name = file_rename
	return filename

def pyaudioTest(request):
	audio = pyaudio.PyAudio()
	print "get_default_host_api_info(): ", audio.get_default_host_api_info()
	print "get_default_input_device_info(): ", audio.get_default_input_device_info()
	print "get_default_output_device_info(): ", audio.get_default_output_device_info()
	return HttpResponse("Testing o pyaudio")

def modal_close(request):
	# If temporary file exists, then delete it.
	if os.path.isfile(path_to_temporary_audio): # http://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists-using-python
		os.remove(path_to_temporary_audio)
		print "Recorded file deleted"
	# If not, then proceed normally.
	return HttpResponse("Successful deletion and clearing of content.")

def python_to_django_file_conversion(python_file):
	f = open(python_file)
	django_file = File(f)
	return django_file

def modify_filename(filename, mark):
	# NOTE: http://stackoverflow.com/questions/25652809/django-file-upload-and-rename
	ext = filename.name.split('.')[-1]
	file_rename = "%s_%s.%s" % ("voice", str(mark), ext)
	filename.name = file_rename
	return filename

def saved_voice_positions(segment_start_pos, segment_end_pos):
	voice_files = VoiceInstruction.objects.order_by('position_of_distance')
	voice_pos = []
	for i in voice_files:
		if(i.position_of_distance >= segment_start_pos and i.position_of_distance <= segment_end_pos):
			voice_pos.append(i.position_of_distance)
			# voice_pos.append(i.position_of_distance - segment_start_pos) # Position of voice with respect to the current segmented distance
	return voice_pos