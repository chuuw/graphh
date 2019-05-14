import os
import sys
sys.path.append(os.path.join(".."))
import CGH
import json
fp1 = open(os.path.join('..', "credentials.json"), "r" , encoding = "utf-8")
dossiercle = json.load(fp1)
key_access = dossiercle["graphhopper"]

G1 = CGH.GraphHopper(key_access)
#print(G1)
point1 = (48.121410, -1.703526)
point2 = (48.114858, -1.680012)
#print(G1.geocode(9))
#print(G1.itinerary(point1,point2, vehicle="eft"))
print(G1.distance(point1,point2))
print(G1.time(point1, point2))

#test reverse_geocode
print(G1.reverse_geocode((48.1572091,-1.6853144)))
d=G1.reverse_geocode((48.1572091,-1.6853144))
#for elt in d["hits"]:
#    print(elt)
print(d["hits"][0]["street"])
