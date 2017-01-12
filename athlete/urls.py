from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'default/', views.default, name='default'),
	url(r'success/', views.success, name='success'),
]
