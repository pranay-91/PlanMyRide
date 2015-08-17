import pythontrace
import urllib2
import json 
import datetime
import googlemaps
import poly


#output_page = open('../templates/results.html','w')
#testing_page = open('../templates/testing.html','w')
html_str = ''
java_str = ''
IMAGE_INTERVAL = 500

api_key = 'AIzaSyDFnxLSssSOW2Z8dyWmlTk_HJOlzY4aNtc'

gmaps = googlemaps.Client(key=api_key)



def java_script_file(start,end,mode):


	java_str = """

		  var x = -1;

		  function displayNextImage() {

              x = (x === images.length - 1) ? 0 : x + 1;
              document.getElementById("img").src = images[x];
              
          }

          function imgError(image){
              image.onerror = "";
              image.src = "";
              return true;
          }

          function displayPreviousImage() {
              x = (x <= 0) ? images.length - 1 : x - 1;
              document.getElementById("img").src = images[x];

          }

          function startTimer() {
              setInterval(displayNextImage, %d);
          }

          var images = %s;

          function imgError(image){
              image.onerror = "";
              image.src = "";
              return true;
          }

          """%(IMAGE_INTERVAL,pythontrace.enter_route(start,end,mode))
	return java_str





def body():

	return """<body onload = "startTimer()">
       		  	<img id="img" onerror="imgError(this);"/>
       			<button type="button" onclick="displayPreviousImage()">Previous</button>
       			<button type="button" onclick="displayNextImage()">Next</button>
   			  </body>"""

def title(name):

	return "<title>%s</title>"%(name)

def create_html_file(title_name,java_str):

	return """<!DOCTYPE html>
			  <html>
   			  	<head>
   			  		<script type="text/javascript">%s</script>
   			  			  <script src="https://www.google.com/jsapi"></script>
   			  		      <script src="https://maps.googleapis.com/maps/api/js?signed_in=true&callback=initMap"async defer></script>
   			  	</head>
   			  	%s
   			  	</html>"""%(java_str,body())


def create_visual_elevation(route_name,points):

	elevation_file = ''
	elevation_file += """$(function () {
    					 	$('#container').highcharts({
        					
        					chart: {
            					type: 'area'
        					},
        					title: {
            					text: 'US and USSR nuclear stockpiles'
        					},
        					subtitle: {
            					text: 'Source: <a href="http://thebulletin.metapress.com/content/c4120650912x74k7/fulltext.pdf">' +
                				'thebulletin.metapress.com</a>'
        					},
        					xAxis: {
            					allowDecimals: true,
            				labels: {

                			formatter: function () {
                    			return this.value; // clean, unformatted number for year
                			}
            			}
        			},
        				yAxis: {
            				title: {
                				text: 'Elevation'
            			},
            			labels: {
                		
            }
        },
        tooltip: {
            pointFormat: '{series.name} produced <b>{point.y:,.0f}</b><br/>Distance {point.x}'
        },
        plotOptions: {
            area: {
                pointStart: 0,
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            }
        },
        series: [ {
            name: '%s',
            data: %s
            }]

        });
	});"""%(route_name,points)	
	
	return elevation_file

def generate_url_for_elevation(start,end,mode_to):

  now = datetime.datetime.now()
  directions_result = gmaps.directions(start,
                                     end,
                                     mode=str(mode_to),
                                     departure_time=now)
  locations = directions_result[0]['overview_polyline']['points']
  return """https://maps.googleapis.com/maps/api/elevation/json?locations=enc:%s&key=%s"""%(locations,api_key)


def json_to_elevation(url):

  response = urllib2.urlopen(str(url))
  data = json.load(response)
  elevation = []
  for i in data['results']:
    elevation.append(i['elevation'])

  return elevation








url = generate_url_for_elevation('Epping,Victoria','Kinglake,Victoria','bicycling')
print url
print json_to_elevation(url)




