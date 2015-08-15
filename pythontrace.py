import json, urllib
from urllib import urlencode
import googlemaps
import poly
import bearing
start = "Southbank, Victoria"
finish = "Richmond, Victoria"

url = 'http://maps.googleapis.com/maps/api/directions/json?%s' % urlencode((
            ('origin', start),
            ('destination', finish)
 ))
ur = urllib.urlopen(url)
result = json.load(ur)

location = []
for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
    j = result['routes'][0]['legs'][0]['steps'][i]['polyline'] 
    location.append(poly.decode(j['points']))
    #print poly.decode(j['points'])

for polyline in location:

	amount_of_point = len(polyline)
	iseven = False


	for i in range(0,amount_of_point-1):

		curr_point = (polyline[i][1],polyline[i][0])
		next_point = (polyline[i+1][1],polyline[i+1][0])
		
		compassBearing = bearing.calculate_initial_compass_bearing(curr_point, next_point)
		url = """https://maps.googleapis.com/maps/api/streetview?size=400x400&location=%s&fov=90&pitch=10&heading=%s"""%((str(curr_point[0])+ ',' + str(curr_point[1]), compassBearing))
		print url 