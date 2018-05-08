from flask import Flask
from flask import request
from pCoordinates import coordinates
import sys

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/available', methods=['GET', 'POST'])
def getAvailableSpots():
    if request.method == 'POST': #only enters here when the form is submitted
        available_spots = []
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        radius = request.form['radius']

        if len(coordinates) == 0:#no spots available in any location
            return "<h3>" + "No parking spots can be reserved right now. Please check back later" + "</h3>"
        else:
            for c in coordinates:
                if (c["lat"] <= int(latitude) + int(radius) and c["lat"] >= int(latitude) - int(radius)) and \
                    (c["lon"] <= int(longitude) + int(radius) and c["lon"] >= int(longitude) - int(radius)):
                    available_spots.append(c)

        if len(available_spots) == 0:#no spots available in specified radius
            return "<h3>" + "No parking spots available within this radius" + "</h3>"
        return "<h3>" + str(available_spots) + "</h3>"
    if request.method == 'GET':
        return '''<form method="POST">
                      Input the latitude, longitude, and radius you would like to look for parking spots in<br>
                      Latitude: <input type="text" name="latitude"><br>
                      Longitude: <input type="text" name="longitude"><br>
                      Radius: <input type="text" name="radius"><br>
                      <input type="submit" value="Submit"><br>
                  </form>'''

@app.route('/reserve', methods=['GET', 'POST'])
def reserveSpot():
    if request.method == 'POST': #only enters here when the form is submitted
        removed = False
        id = request.form['id']

        if len(coordinates) == 0: #no parking spots are available to be reserved
            return "<h3>" + "No parking spots can be reserved right now." + "<h3>"

        for s in coordinates:
            if s["id"] == int(id):
                coordinates.remove(s)
                removed = True
                return "reserved parking spot # " + id + " has been reserved!"

        if(not removed): #the car you want to reserve is not available
            return "Parking spot #" + id + " doesn't exist or cannot be reserved right now."

    if request.method == 'GET':
        return '''<form method="POST">
                      Input the id of the parking spot you want to reserve <br>
                      ID: <input type="text" name="id"><br>
                      <input type="submit" value="Submit"><br>
                  </form>'''

