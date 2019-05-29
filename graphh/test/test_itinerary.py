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

print(G1.itinerary(point1, point2, locale = "fr", vehicle= "foot"))
print(G1.time(point2, point1, vehicle="foot", unit="min"))
#print(G1.time(point2, point1, vehicle="car", unit="j"))

print(G1.distance(point1, point2, unit="km"))
#print(G1.distance(point1, point2, unit="mm"))

errors = ("small_truck", "truck", "scooter", "hike", "mtb", "racingbike")