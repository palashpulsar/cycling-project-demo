from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'stage/', views.default_stage, name='stage'),
	url(r'local/', views.default_local, name='local'),
	url(r'mapviz/', views.map_viz, name='mapviz'),
	url(r'fillingGeolocation/', views.fillingGeolocation, name='fillingGeolocation'),
	url(r'retrievingDrivenGeolocation/', views.retrievingDrivenGeolocation, 
		name='retrievingDrivenGeolocation'),
	url(r'test/', views.test, name='test'),
]
