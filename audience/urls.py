from django.conf.urls import url
from . import views, audio

urlpatterns = [
	url(r'cheer/$', views.cheer_interface, name='cheer'),
	# For voice saving function
	url(r'^cheer/save/$', audio.voice_save_del, name='save'),
	# For voice history
	url(r'^cheer/history/$', views.voiceHistory, name='history'),
]
