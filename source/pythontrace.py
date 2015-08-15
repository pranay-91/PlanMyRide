import json, urllib
from urllib import urlencode
import googlemaps
import poly
import bearing
import datetime



api_key = 'AIzaSyDFnxLSssSOW2Z8dyWmlTk_HJOlzY4aNtc'

gmaps = googlemaps.Client(key=api_key)


#Returns elevation in meters

def elevation(lat, lon):
	elevation = gmaps.elevation((lat, lon))
	return elevation[0]['elevation']


#Returns a list of urls that we use to
#create our sequences of images 
def enter_route(start,destination,travel_mode):

	now = datetime.datetime.now()
	url_list = []
	directions_result = gmaps.directions(start,
                                     destination,
                                     mode=travel_mode,
                                     departure_time=now)


	overview_polyline = directions_result[0]['overview_polyline']['points']


	points = poly.decode(overview_polyline)

	amount_of_point = len(points)

	for i in range(0,amount_of_point-1):

		curr_point = (points[i][1],points[i][0])
		next_point = (points[i+1][1],points[i+1][0])
			
		compassBearing = bearing.calculate_initial_compass_bearing(curr_point, next_point)
		url = """https://maps.googleapis.com/maps/api/streetview?size=400x400&location=%s&fov=90&pitch=10&heading=%s&key=%s"""%((str(curr_point[0])+ ',' + str(curr_point[1]), compassBearing,api_key))
		url_list.append(url) 

	return url_list 
