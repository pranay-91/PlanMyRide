import pythontrace


output_page = open('../templates/results.html','w')
testing_page = open('../templates/testing.html','w')
html_str = ''
java_str = ''
IMAGE_INTERVAL = 500



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

def elevation_visualisation(path):

	java_str = ''
	java_str += "google.load('visualization', '1', {packages: ['columnchart']});"
	java_str += """function initMap() {

				   var path = %s;
				   var map = new google.maps.Map(document.getElementById('Map'), {
				   		zoom: 8,
				   		center: path[1],
				   		mapTypeId: 'terrain'
				   	});
					
					 // Create an ElevationService.
  					var elevator = new google.maps.ElevationService;

  					// Draw the path, using the Visualization API and the Elevation service.
  					displayPathElevation(path, elevator, map);
					}"""%(path)

	java_str += """function displayPathElevation(path, elevator, map) {
  					// Display a polyline of the elevation path.
 					 new google.maps.Polyline({
    				 	path: path,
    					strokeColor: '#0000CC',
    					opacity: 0.4,
    					map: map
  					});

  					// Create a PathElevationRequest object using this array.
  					// Ask for 256 samples along that path.
  					// Initiate the path request.
  					elevator.getElevationAlongPath({
    				'path': path,
    				'samples': 256
  					}, plotElevation);
				}"""


	java_str += """// Takes an array of ElevationResult objects, draws the path on the map
				  // and plots the elevation profile on a Visualization API ColumnChart.
				 function plotElevation(elevations, status) {
  				 	
  				 	var chartDiv = document.getElementById('elevation_chart');
  					
  					if (status !== google.maps.ElevationStatus.OK) {
    					// Show the error code inside the chartDiv.
    					chartDiv.innerHTML = 'Cannot show elevation: request failed because ' +
        				status;
    				
    				return;
  				}
  				
  				// Create a new chart in the elevation_chart DIV.
  				var chart = new google.visualization.ColumnChart(chartDiv);

				  // Extract the data from which to populate the chart.
				  // Because the samples are equidistant, the 'Sample'
				  // column here does double duty as distance along the
				  // X axis.
				  var data = new google.visualization.DataTable();
				  data.addColumn('string', 'Sample');
				  data.addColumn('number', 'Elevation');
				  for (var i = 0; i < elevations.length; i++) {
				    data.addRow(['', elevations[i].elevation]);
				  }

				  // Draw the chart using the data within its DIV.
				  chart.draw(data, {
				    height: 150,
				    legend: 'none',
    				titleY: 'Elevation (m)'
  					});
			}"""
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

def test(path):

	html_str = ""
	html_str += """<!DOCTYPE html>
				   <html>
  				   <head>
    			   		<meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    					<meta charset="utf-8">
    					<title>Showing elevation along a path</title>
    					<style>
      					
      					html, body {
        					height: 100%;
        					margin: 0;
        					padding: 0;
      					}
      
      					#map {
        					height: 100%;
      					}

    					</style>
    					<script src="https://www.google.com/jsapi"></script>
  				</head>
  				<body>
    				<div>
      					<div id="map" style="height:250px;"></div>
      					<div id="elevation_chart"></div>

      					<script>%s</script>

						<script src="https://maps.googleapis.com/maps/api/js?signed_in=true&callback=initMap
          				async defer></script>
    			   </div>
  				   </body>
				   </html>"""%(elevation_visualisation(path))
	return html_str
	


title = 'Results'
java_string = java_script_file('Epping,Victoria','Kinglake,Victoria','bicycling')

output_page.write(create_html_file(title,java_string))
output_page.close()
path = pythontrace.convert_to_visual_format('Epping,Victoria','Kinglake,Victoria','bicycling')

testing_page.write(test(path))
testing_page.close()

