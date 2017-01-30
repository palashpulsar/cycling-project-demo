"""
The following script manually (or locally) generates CSV files from GPX files.
Extracting latitude, longitude, distance and elevation from GPX file is
causing memory leaks in Heroku. Hence this script was made to avoid memory leaks.
"""

from vincenty import vincenty
import csv
import gpxpy
import os

def indetifyingAllKeys(dataset):
	all_keys = []
	for i in range(len(dataset)):
		for key in dataset[i]:
			if key not in all_keys:
				all_keys.append(key)
	return all_keys

Target_Folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Cycling/Routes/GPX/')
Destination_Folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Cycling/Routes/CSV/')
print Target_Folder
for gpx_file in os.listdir(Target_Folder):
	if '.gpx' in gpx_file:
		print "You are looking at a GPX file: %s" % gpx_file
		f = open(Target_Folder+gpx_file, 'r') # LINK: http://stackoverflow.com/questions/29034730/using-gpxpy-to-parse-gpx-file-results-in-not-well-formed-invalid-token-error
		gpx = gpxpy.parse(f)
		print gpx
		data = {}
		dataset = []
		init = 1
		lat_init = None
		lon_init = None
		dis_init = None
		for track in gpx.tracks:
			for segment in track.segments:
				for point in segment.points:
					data['latitude'] = point.latitude
					data['longitude'] = point.longitude
					data['elevation'] = point.elevation
					if init == 1:
						data['distance'] = 0
						lat_init = data['latitude']
						lon_init = data['longitude']
						dis_init = data['distance']
						init = 0
					else:
						boston = (lat_init, lon_init)
						newyork = (data['latitude'], data['longitude'])
						data['distance'] = vincenty(boston, newyork) + dis_init
						lat_init = data['latitude']
						lon_init = data['longitude']
						dis_init = data['distance']
					dataset.append(data.copy())
		# print dataset
		keys = indetifyingAllKeys(dataset)
		print keys
		with open(Destination_Folder+gpx_file.split('.')[0]+'.csv', 'wb') as output_file:
			dict_writer = csv.DictWriter(output_file, keys)
			dict_writer.writeheader()
			dict_writer.writerows(dataset)