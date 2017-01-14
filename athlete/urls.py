from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'default/', views.default, name='default'),
	url(r'mapviz/', views.map_viz, name='mapviz'),
]
