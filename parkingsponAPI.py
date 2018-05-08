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
        if len(coordinates) != 0: #add special empty message
            for c in coordinates:
                # if (clat <= 1000 or c.lat <= 1000) and (c.lon <= 1000 or c.lon <= 1000):
                available_spots.append(c["id"])

        return "<h2>" + str(available_spots) + "</h2>"
    if request.method == 'GET':
        return '''<form method="POST">
                      Latitude: <input type="text" name="latitude"><br>
                      Longitude: <input type="text" name="radius"><br>
                      Radius: <input type="text" name="radius"><br>
                      <input type="submit" value="Submit"><br>
                  </form>'''

@app.route('/reserve')
def reserveSpot():
    return 'reserving requested spot'

