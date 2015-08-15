import pythontrace


output_page = open('../templates/results.html','w')
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
   			  	</head>
   			  	%s
   			  	</html>"""%(java_str,body())


title = 'Results'
java_string = java_script_file('Epping,Victoria','Kinglake,Victoria','bicycling')

output_page.write(create_html_file(title,java_string))
output_page.close()
