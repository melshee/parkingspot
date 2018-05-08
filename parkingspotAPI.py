from flask import Flask
from flask import request
from pCoordinates import coordinates

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/available', methods=['GET', 'POST'])
def getAvailableSpots():
    if request.method == 'POST': #this block is only entered when the form is submitted
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
                      Latitude: <input type="text" name="latitude"><br>
                      Longitude: <input type="text" name="longitude"><br>
                      Radius: <input type="text" name="radius"><br>
                      <input type="submit" value="Submit"><br>
                  </form>'''

@app.route('/reserve')
def reserveSpot():
    return 'reserving requested spot'

