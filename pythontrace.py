import json, urllib
from urllib import urlencode
import googlemaps
import poly
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
	for coord in polyline:
		url = """https://maps.googleapis.com/maps/api/streetview?size=400x400&location=%s&fov=90&pitch=10"""%(str(coord[1])+","+str(coord[0]))
		print url 

