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

        if len(coordinates) != 0: #TODO add special empty message
            for c in coordinates:
                if (c["lat"] <= int(latitude) + int(radius) and c["lat"] >= int(latitude) - int(radius)) and \
                    (c["lon"] <= int(longitude) + int(radius) and c["lon"] >= int(longitude) - int(radius)):
                    available_spots.append(c)

        return "<h2>" + str(available_spots) + "</h2>"
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

