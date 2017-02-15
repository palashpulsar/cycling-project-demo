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
	# playng the recorded sound
	url(r'^modal/play/$', audio.test_play, name='play'),
]
