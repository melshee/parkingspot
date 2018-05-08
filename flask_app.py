from flask import Flask
from flask import request
from pCoordinates import coordinates

app = Flask(__name__)
links = '''<div>
            <a href="http://melshee.pythonanywhere.com/api/parkingspots/available">See available parking spots</a>
           </div>
           <div>
            <a href="http://melshee.pythonanywhere.com/api/parkingspots/reserve">Reserve a parking spot</a>
           </div>
           <div>
            <a href="http://melshee.pythonanywhere.com">Go back to main page</a>
           </div> '''

@app.route('/api/parkingspots/available', methods=['GET', 'POST'])
def getAvailableSpots():
    if request.method == 'POST': #only enters here when the form is submitted
        available_spots = []
        available_spots_list = "<ul>"

        if (request.form['latitude'] == "" or request.form['longitude'] == "" or request.form['radius'] == ""):
            return "<h3>" + "Error: please fill out entire form" + "</h3>"
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        radius = float(request.form['radius'])

        #input validation
        if (latitude > 90 or latitude < -90): # Latitudes range from -90 to 90
            return "<h3>" + "Error: please input a latitude between -90 and 90" + "</h3>"
        if (longitude > 180 or longitude < -180): #Longitudes range from -180 to 180
            return "<h3>" + "Error: please input a longitude between -180 and 180" + "</h3>"
        if (radius < 0): #radius can't be negative
            return "<h3>" + "Error: please input a radius greater than or equal to 0" + "</h3>"

        if len(coordinates) == 0: #no spots available in any location
            return "<h3>" + "No parking spots can be reserved right now. Please check back later" + "</h3>"
        else:
            for c in coordinates:
                if (c["lat"] <= latitude + radius and c["lat"] >= latitude - radius) and \
                    (c["lon"] <= longitude + radius and c["lon"] >= longitude - radius):
                    available_spots.append(c)
                    available_spots_list = available_spots_list + "<li>" + str(c) + "</li>"

        if len(available_spots) == 0: #no spots available in specified radius
            return "<h3>" + "No parking spots available within this radius" + "</h3>"


        available_spots_list = available_spots_list + "</ul>"
        return str(available_spots_list) + links


    if request.method == 'GET':
        return '''<form method="POST">
                      Input the latitude, longitude, and radius you would like to look for parking spots in<br>
                      Latitude: <input type="number" name="latitude" step="0.1"><br>
                      Longitude: <input type="number" name="longitude" step="0.1"><br>
                      Radius: <input type="number" name="radius" step="0.1"><br>
                      <input type="submit" value="Submit"><br>
                  </form>''' + links

@app.route('/api/parkingspots/reserve', methods=['GET', 'POST'])
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
                return "reserved parking spot # " + id + " has been reserved!" + links

        if(not removed): #the car you want to reserve is not available
            return "Parking spot #" + id + " doesn't exist or cannot be reserved right now."

    if request.method == 'GET':
        return '''<form method="POST">
                      Input the id of the parking spot you want to reserve <br>
                      ID: <input type="number" name="id"><br>
                      <input type="submit" value="Submit"><br>
                  </form>''' + links

@app.route('/')
def main():
    list = "<ul>"

    for c in coordinates:
        list = list + "<li>" + str(c) + "</li>"

    list = list + "</ul>"

    return 'Welcome to Melissa\'s simple parking spot reservation API. It features two protocols: <br>' + \
            '<ol> \
                <li><a href="http://melshee.pythonanywhere.com/api/parkingspots/available">/api/parkingspots/available</a></li> \
                    <ul> \
                        <li>input: latitude, longitude, and radius</li> \
                        <li>returns: all available parking spots within the specified radius</li> \
                    </ul> \
                <li><a href="http://melshee.pythonanywhere.com/api/parkingspots/reserve">/api/parkingspots/reserve</a></li> \
                    <ul> \
                        <li>input: id of parking spot</li> \
                        <li>returns: response message whether reservation was successful or not</li> \
                        <li>If successfully reserved, the spot is removed from the list of available parking spots.</li> \
                    </ul> \
            </ol>' + \
            'The set of parking spots (in pCoordinates.py) is listed below:' + list + \
            'Some useful tests to try for requests made to /api/parkingspots/available: <br> \
                <ul> \
                    <li>input: latitude=37.5, longitude=-122.4, radius=0</li> \
                        <ul>Expected output: 1 spot: id=1 </ul> \
                    <li>input: latitude=37.5, longitude=-122.4, radius=1</li> \
                        <ul>Expected output: 3 spots: id=1, id=2, id=3 </ul> \
                    <li>input: latitude=37.5, longitude=-122.4, radius=50</li> \
                        <ul>Expected output: 5 spots: id=1, id=2, id=3, id=4, id=5  </ul> \
                    <li>input: latitude=37.5, longitude=-122.4, radius=200</li> \
                        <ul>Expected output: 10 spots: (all 10 ids)  </ul> \
                </ul>' + \
            'Edge cases for requests made to /api/parkingspots/available: <br> \
                <ul> \
                    <li>input: latitude, longitude, and/or radius forms are left blank</li> \
                        <ul>Expected output: "Error: please fill out entire form" </ul> \
                    <li>input: latitude < -180 or latitud > 180</li> \
                        <ul>Expected output: "Error: please input a latitude between -90 and 90" </ul> \
                    <li>input: longitude < -180 or longitude > 180</li> \
                        <ul>Expected output: "Error: please input a longitude between -180 and 180"  </ul> \
                    <li>input: radius < 0</li> \
                        <ul>Expected output: "Error: please input a radius greater than or equal to 0"  </ul> \
                </ul>' + \
            'Edge cases for requests made to /api/parkingspots/requests: <br> \
                <ul> \
                    <li>input: id < 0</li> \
                        <ul>Expected output: "Error: invalid id" </ul> \
                    <li>input: if of spot that has already been reserved</li> \
                        <ul>Expected output: "Parking spot #{id} doesn\'t exist or cannot be reserved right now." </ul> \
                </ul>'

