import os
import sys
sys.path.append(os.path.join(".."))
import CGH
import json
fp1 = open(os.path.join('..', "credentials.json"), "r" , encoding = "utf-8")
dossiercle = json.load(fp1)
key_access = dossiercle["graphhopper"]

G1 = CGH.GraphHopper(key_access)

point1 = (48.121410, -1.703526)
point2 = (48.114858, -1.680012)

#print(G1.itinerary(point1, point2, locale = "fr", vehicle= "bike"))
print(G1.time(point2,point1, vehicle="car"))
#print(G1.distance(point1,point2))