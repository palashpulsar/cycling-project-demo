from django.conf.urls import url

from . import views, audio

urlpatterns = [
	url(r'^login/$', views.login, name='login'),
	url(r'^upload/$', views.uploadGPX, name='upload'),	
	url(r'^mapviz/$', views.map_viz, name='mapviz'),
	# All audio activity happens here.
	url(r'^modal/record/$', audio.record, name='record'),
	url(r'^modal/play/$', audio.play, name='play'),
	url(r'^modal/save/$', audio.save, name='save'),
	url(r'^strategy/history/$', audio.voiceHistory, name='history'), # For voice history
]