"""
The following script contains all codes that were removed from previous 
implementation of the app.
"""

# LINK: http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
				# start = time.time()
				# request.session['gpx_data']=gpx_extract_info(file)
				# end = time.time()
				# print "Time taken for fist function is: ", (end - start)

				# start = time.time()
				# gpx_ext_info(file)
				# end = time.time()
				# print "Time taken for second function is: ", (end - start)

def gpx_extract_info(gpx_file):
	# Identifying the location of the gpx file
	gpx = gpxpy.parse(gpx_file.docfile)
	t = 0
	gpx_data = {}
	gpx_data['latitude'] = []
	gpx_data['longitude'] = []	
	gpx_data['elevation'] = []
	gpx_data['distance'] = [] 
	for track in gpx.tracks:
		for segment in track.segments:
			for point in segment.points:
				gpx_data['latitude'].append(point.latitude)
				gpx_data['longitude'].append(point.longitude)
				gpx_data['elevation'].append(point.elevation)
				t = t+1
	# Calculating the distance
	for i in range(len(gpx_data['latitude'])):
		if(i==0):
			gpx_data['distance'].append(0)
		else:
			boston = (gpx_data['latitude'][i-1], gpx_data['longitude'][i-1])
			newyork = (gpx_data['latitude'][i], gpx_data['longitude'][i])
			gpx_data['distance'].append(gpx_data['distance'][i-1] + vincenty(boston, newyork))
	return gpx_data

def gpx_ext_info(gpx_file):
	gpx = gpxpy.parse(gpx_file.docfile)
	print "gpx: ", gpx
	data = {}
	dataset = []
	init = 1
	lat_init = None
	lon_init = None
	dis_init = None
	for track in gpx.tracks:
		for segment in track.segments:
			for point in segment.points:
				data['lat'] = point.latitude
				data['lon'] = point.longitude
				data['ele'] = point.elevation
				if init == 1:
					data['dis'] = 0
					lat_init = data['lat']
					lon_init = data['lon']
					dis_init = data['dis']
					init = 0
				else:
					boston = (lat_init, lon_init)
					newyork = (data['lat'], data['lon'])
					# data['dis'] = vincenty(boston, newyork) + dis_init
					data['dis'] = 0
					lat_init = data['lat']
					lon_init = data['lon']
					dis_init = data['dis']
				dataset.append(data.copy()) # LINK: http://stackoverflow.com/questions/5244810/python-appending-a-dictionary-to-a-list-i-see-a-pointer-like-behavior
	gpx_data = gpx_dataObj(data_json = json.dumps(dataset))
	gpx_data.save()
	return None

def csv_file_extraction(file):
	# LINK: http://stackoverflow.com/questions/14091387/creating-a-dictionary-from-a-csv-file
	# LINK: http://stackoverflow.com/questions/17262256/how-to-read-one-single-line-of-csv-data-in-python
	# LINK: http://stackoverflow.com/questions/2241891/how-to-initialize-a-dict-with-keys-from-a-list-and-empty-value-in-python
	# LINK: http://stackoverflow.com/questions/209840/map-two-lists-into-a-dictionary-in-python
	# LINK: http://stackoverflow.com/questions/1614236/in-python-how-do-i-convert-all-of-the-items-in-a-list-to-floats
	print "I am inside csv_file_extraction function"
	print "CSV file: ", file
	data = {}
	dataset = []
	with open(file, 'rb') as f:
		data_test = csv.reader(f)
		keys = next(data_test)
		print "keys: ", keys
		print "data: "
		for rows in data_test:
			data = dict(zip(keys, [float(i) for i in rows]))
			print data
			dataset.append(data)
	return None

def default_stage(request):
	form = gpx_file_form()
	gpx_delete() # There will be only one GPX file, and nothing else
	gpx_dataObj.objects.all().delete()
	VoiceInstruction.objects.all().delete()
	geoLocation.objects.all().delete()
	if request.method == 'POST':
		form = gpx_file_form(request.POST, request.FILES)
		if form.is_valid:
			if len(request.FILES) != 0: # User has entered the file
				file = gpx_file(docfile=request.FILES['docfile'])
				file.save()
				dataset = csv_extraction('stage', str(file.docfile))
				entering_gpx_dataObj(dataset, str(file.docfile))
				return HttpResponseRedirect("../mapviz")
				# return HttpResponse("Thanks for uploading file.")
		else:
			form = gpx_file_form()
	return render(request, 'athlete/gpx.html', {'form': form})