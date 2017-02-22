from django.conf.urls import url
from . import views, audio

urlpatterns = [
	url(r'cheer/$', views.cheer_interface, name='cheer'),
	# For voice saving function
	url(r'^cheer/save/$', audio.voice_save_del, name='save'),
	# For voice history
	url(r'^cheer/history/$', views.voiceHistory, name='history'),

	# For modal section
	# recording
	url(r'^modal/record/$', audio.test_record, name='record'),
	# url(r'^modal/recordLocal/$', audio.test_record_local, name='record'),
	# playng the recorded sound
	url(r'^modal/play/$', audio.test_play, name='play'),
	# saving the recorded sound
	url(r'^modal/save/$', audio.test_save, name='save'),

	# Testing of pyaudio
	url(r'^test/$', audio.pyaudioTest, name='test'),
]
