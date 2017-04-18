from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^login/$', views.login, name='login'),
	url(r'^upload/$', views.uploadGPX, name='upload'),	
	url(r'^mapviz/$', views.map_viz, name='mapviz'),
]