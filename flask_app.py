from flask import Flask
from flask import request
from pCoordinates import coordinates

app = Flask(__name__)

@app.route('/')
def main():
    return 'Welcome to Melissa\'s simple parking spot reservation API. It features 2 protocols: <br>' + \
            '<ol> \
                <li>/available</li> \
                    <ul>returns all available parking spots within the specified radius of \
                        a latitude and longitude point (also needs to be specified). \
                    </ul> \
                <li>/reserve/{id}</li> \
                    <ul>reserved the parking spot with the given id (if possible). If successfully \
                        reserved, the spot is removed from the list of available parking spots. \
                    </ul> \
            </ol>'

@app.route('/available', methods=['GET', 'POST'])
def getAvailableSpots():
    if request.method == 'POST': #only enters here when the form is submitted
        available_spots = []

        if (request.form['latitude'] == "" or request.form['longitude'] == "" or request.form['radius'] == ""):
            return "<h3>" + "Error: please fill out entire form" + "</h3>"
        latitude = int(request.form['latitude'])
        longitude = int(request.form['longitude'])
        radius = int(request.form['radius'])

        #input validation
        if (latitude > 90 or latitude < -90): # Latitudes range from -90 to 90
            return "<h3>" + "Error: please input a latitude between -90 and 90" + "</h3>"
        if (longitude > 180 or longitude < -180): #Longitudes range from -180 to 180
            return "<h3>" + "Error: please input a longitude between -180 and 180" + "</h3>"
        if (radius < 0): #radius can't be positive
            return "<h3>" + "Error: please input a radius greater than or equal to 0" + "</h3>"

        if len(coordinates) == 0: #no spots available in any location
            return "<h3>" + "No parking spots can be reserved right now. Please check back later" + "</h3>"
        else:
            for c in coordinates:
                if (c["lat"] <= latitude + radius and c["lat"] >= latitude - radius) and \
                    (c["lon"] <= longitude + radius and c["lon"] >= longitude - radius):
                    available_spots.append(c)

        if len(available_spots) == 0: #no spots available in specified radius
            return "<h3>" + "No parking spots available within this radius" + "</h3>"
        return "<h3>" + str(available_spots) + "</h3>" + \
                  '''<div>
                    <a href="http://melshee.pythonanywhere.com/available">See available parking spots</a>
                   </div>''' + \
                  '''<div>
                    <a href="http://melshee.pythonanywhere.com/reserve">Reserve a parking spot</a>
                   </div>'''

    if request.method == 'GET':
        return '''<form method="POST">
                      Input the latitude, longitude, and radius you would like to look for parking spots in<br>
                      Latitude: <input type="number" name="latitude"><br>
                      Longitude: <input type="number" name="longitude"><br>
                      Radius: <input type="number" name="radius"><br>
                      <input type="submit" value="Submit"><br>
                  </form>''' + \
                  '''<div>
                    <a href="http://melshee.pythonanywhere.com/available">See available parking spots</a>
                   </div>''' + \
                  '''<div>
                    <a href="http://melshee.pythonanywhere.com/reserve">Reserve a parking spot</a>
                   </div>'''

@app.route('/reserve', methods=['GET', 'POST'])
def reserveSpot():
    if request.method == 'POST': #only enters here when the form is submitted
        removed = False
        id = request.form['id']

        if int(id) < 0:
            return "<h3>" + "Error: invalid id" + "</h3>"

        if len(coordinates) == 0: #no parking spots are available to be reserved
            return "<h3>" + "No parking spots can be reserved right now." + "<h3>"

        for s in coordinates:
            if s["id"] == int(id):
                coordinates.remove(s)
                removed = True
                return "reserved parking spot # " + id + " has been reserved!" + \
                        '''<div>
                            <a href="http://melshee.pythonanywhere.com/available">See available parking spots</a>
                           </div>''' + \
                        '''<div>
                            <a href="http://melshee.pythonanywhere.com/reserve">Reserve a parking spot</a>
                           </div>'''

        if(not removed): #the car you want to reserve is not available
            return "Parking spot #" + id + " doesn't exist or cannot be reserved right now."

    if request.method == 'GET':
        return '''<form method="POST">
                      Input the id of the parking spot you want to reserve <br>
                      ID: <input type="number" name="id"><br>
                      <input type="submit" value="Submit"><br>
                  </form>''' + \
                  '''<div>
                  <a href="http://melshee.pythonanywhere.com/available">See available parking spots</a>
                  </div>''' + \
                  '''<div>
                    <a href="http://melshee.pythonanywhere.com/reserve">Reserve a parking spot</a>
                  </div>'''

