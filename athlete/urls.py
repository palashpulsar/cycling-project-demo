from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'$', views.uploadCSV, name='local'),
	url(r'mapviz/', views.map_viz, name='mapviz'),
	url(r'fillingGeolocation/', views.fillingGeolocation, name='fillingGeolocation'),
	url(r'retrievingDrivenGeolocation/', views.retrievingDrivenGeolocation, 
		name='retrievingDrivenGeolocation'),
	url(r'test/', views.test, name='test'),
]
