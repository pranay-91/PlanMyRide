from flask import Flask, render_template, redirect, request, jsonify

import os
import json
import sys

sys.path.append( 'source' )
import pythontrace
import generate_route

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')



app = Flask(__name__, template_folder=tmpl_dir)

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])



def home():
	if request.method == "GET":
		locations = []
		elevations = []
		return render_template('./index.html', locations=locations, elevations=elevations)

	start=request.form['start_loc']
	end=request.form['end_loc']
	locations = pythontrace.enter_route(start, end, 'driving')
	elevations = generate_route.json_to_elevation(generate_route.generate_url_for_elevation(start,end,'driving'))


	return render_template('./index.html', locations=locations,elevations=elevations)



@app.route('/test')
def test():
	return render_template('./test.html')

#@app.route('/results')
#def results():
#	return render_template('./results.html')
	#if request.method == "GET":
#		return redirect(url_for('home'))



if __name__ == '__main__':
	app.run(debug=True)
