coordinates = [
    #coordinates less than 1 'unit' away from Ridecell (37.5, -122.4)
    {"id": 1, "lat":37.5, "lon": -122.4},
    {"id": 2, "lat":37, "lon": -122},
    {"id": 3, "lat":37.2, "lon": -122.2},
    #coordinates less than 20 'units' away from Ridecell (37.5, -122.4)
    {"id": 4, "lat":50.0, "lon": -100},
    {"id": 5, "lat":40, "lon": -130},
    #edge case coordinates (latitudes range from -90 to 90) and (longitudes range from -180 to 180)
    #these are also coordinates less than 200 'units' away from Ridecell (37.5, -122.4)
    {"id": 6, "lat":90, "lon": 180},
    {"id": 7, "lat":90, "lon": -180},
    {"id": 8, "lat":-90, "lon": 180},
    {"id": 9, "lat":-90, "lon": -180},
    {"id": 10, "lat":0, "lon": 0},
]