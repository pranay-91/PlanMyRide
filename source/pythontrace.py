import json, urllib
from urllib import urlencode
import googlemaps
import poly
import bearing
import datetime
import urllib2
import json 




api_key = 'AIzaSyDFnxLSssSOW2Z8dyWmlTk_HJOlzY4aNtc'

gmaps = googlemaps.Client(key=api_key)



#Returns a list of urls that we use to
#create our sequences of images 
def enter_route(start,destination,travel_mode,flag=False):

	now = datetime.datetime.now()
	url_list = []
	directions_result = gmaps.directions(start,
                                     destination,
                                     mode=travel_mode,
                                     departure_time=now)



	overview_polyline = directions_result[0]['overview_polyline']['points']

	dic_of_points = directions_result[0]['legs'][0]['steps']

	if flag:

		amount_of_point = len(points)

		for i in range(0,amount_of_point-1):

			curr_point = (points[i][1],points[i][0])
			next_point = (points[i+1][1],points[i+1][0])
			
			compassBearing = bearing.calculate_initial_compass_bearing(curr_point, next_point)
			url = """https://maps.googleapis.com/maps/api/streetview?size=400x400&location=%s&fov=90&pitch=10&heading=%s&key=%s"""%((str(curr_point[0])+ ',' + str(curr_point[1]), compassBearing,api_key))
			url_list.append(url)
	else:

		for step in dic_of_points:

			points = poly.decode(step['polyline']['points'])
			amount_of_point = len(points)

			for i in range(0,amount_of_point-1):

				curr_point = (points[i][1],points[i][0])
				next_point = (points[i+1][1],points[i+1][0])
			
				compassBearing = bearing.calculate_initial_compass_bearing(curr_point, next_point)
				url = """https://maps.googleapis.com/maps/api/streetview?size=400x400&location=%s&fov=90&pitch=10&heading=%s&key=%s"""%((str(curr_point[0])+ ',' + str(curr_point[1]), compassBearing,api_key))
				url_list.append(url) 

	return url_list 

# points in the google visualisation format convertor

def convert_to_visual_format(start,destination,travel_mode):

	now = datetime.datetime.now()
	url_list = []
	directions_result = gmaps.directions(start,
                                     destination,
                                     mode=travel_mode,
                                     departure_time=now)

	overview_polyline = directions_result[0]['overview_polyline']['points']['steps']


	points = poly.decode(overview_polyline)

	amount_of_point = len(points)
	
	path_of_points = []

	for i in range(0,amount_of_point-1):

		coord_dict = {}
		coord_dict['lat'] = points[i][1]
		coord_dict['lng'] = points[i][0]
		path_of_points.append(coord_dict)

	return path_of_points


now = datetime.datetime.now()

directions_result = gmaps.directions('Richmond,Vic',
                                     'Melbourne,Vic',
                                     mode='bicycling',
                                     departure_time=now)



overview_polyline = directions_result[0]['overview_polyline']['points']





