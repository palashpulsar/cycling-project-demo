from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import gpx_file_form
from .models import gpx_file
# Create your views here.
def default(request):
	form = gpx_file_form()
	if request.method == 'POST':
		form = gpx_file_form(request.POST, request.FILES)
		if form.is_valid:
			if len(request.FILES) != 0: # User has entered the file
				file = gpx_file(docfile=request.FILES['docfile'])
				file.save()
				# return HttpResponse("GPX is uploaded.")
				return HttpResponseRedirect("../mapviz")
		else:
			form = gpx_file_form()
	# LINK: http://stackoverflow.com/questions/22470637/django-show-validationerror-in-template
	return render(request, 'athlete/gpx.html', {'form': form})

def map_viz(request):
	return HttpResponse("I AM HERE. CHECK THE URL")
