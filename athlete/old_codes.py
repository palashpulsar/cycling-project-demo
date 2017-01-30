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