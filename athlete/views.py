from django.shortcuts import render
from django.http import HttpResponse
from .forms import gpx_file_form

# Create your views here.
def default(request):
	form = gpx_file_form()
	return render(request, 'athlete/gpx.html', {'form': form})

def success(request):
	return HttpResponse("GPX file is now uploaded.")
