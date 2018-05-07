from pCoordinates import coordinates
# from pCoordinates import reserved

#sending a request
          method: "POST",
          url: "/api/v1/parkingspots/available",
          data: {
            {
              "lat": 37.5,
              "lon": -122.4,
              "radius": 50
            }
          },
          success: returned_data => {
            print(returned_data);
          }

#backend
def api_request():
if( url == "/api/v1/parkingspots/available" && method == "POST")
  available_spots = []

  if len(coordinates) != 0
    for c in coordinates: 
      if((c.lat <= lat + radius || c.lat <= lat - radius) && (c.lon <= lon + radius || c.lon <= lon  radius))
        available_spots.append(c)           
  
  return available_spots

else if( url =="/api/v1/parkingspots/reserve/<id>" && method == "GET") 
  bool removed = false

  if len(coordinates) == 0 #no parking spots are available to be reserved
    return "no parking spots can be reserved right now. Please check back later"

  for c in coordinates: 
    if(c.id == id)
      coordinates.remove(c)
      removed = true
      return "reserved parking spot #" + id + "enjoy!"

  if(removed == false) #the car you want to reserve is not available
    return "Parking spot #" + id + "cannot be reserved right now. Please check back later"



#tests
#no cars are available within the radius
#the car you want to reserve is not available

