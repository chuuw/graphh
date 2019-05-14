import os
import sys
import json
sys.path.append(os.path.join(".."))
import fonctionurl_clem
fp1 = open(os.path.join('..', "credentials.json"), "r" , encoding = "utf-8")
dossiercle = json.load(fp1)
key_access = dossiercle["graphhopper"]
G1 = fonctionurl_clem.GraphHopper(key_access)
point1 = (48.121410, -1.703526)
point2 = (48.114858, -1.680012)
testroute = G1.url_def(["route", "point=51.131,12.414","point=48.224,3.867"])
testroute2= G1.url_def2("route", {"point" : (G1.formepoint(point1),G1.formepoint(point2)) })
print(testroute2)
