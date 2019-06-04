import os
import sys

sys.path.append(os.path.join(".."))

import CGH
import json

fp1 = open(os.path.join('..', "credentials.json"), "r" , encoding = "utf-8")
keyfile = json.load(fp1)
key_access = keyfile["graphhopper"]

G1 = CGH.GraphHopper(key_access)

point1 = (48.121410, -1.703526)
point2 = (48.114858, -1.680012)
point4 = (48.134858, -1.540012)
point3 = (48.154858, -1.720012)
lpoint = (point1,point2, point3)

#print(G1.route(lpoint, locale = "fr", vehicle = "bike"))
#print(G1.time(lpoint, vehicle="foot", unit="min"))
#print(G1.time(point2, point1, vehicle="car", unit="j"))

#print(G1.distance(lpoint, unit="km"))
#print(G1.distance(point1, point2, unit="mm"))

errors = ("small_truck", "truck", "scooter", "hike", "mtb", "racingbike")

print(G1.elevation_point(point1))