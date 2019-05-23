import os
import sys

sys.path.append(os.path.join(".."))

import CGH
import json


fp1 = open(os.path.join('..', "credentials.json"), "r", encoding="utf-8")
key_file = json.load(fp1)
key_access = key_file["graphhopper"]

G1 = CGH.GraphHopper(key_access)

# test geocode
# print(G1.geocode("4 allée du clos prioul Montgermont"))
# print(G1.geocode("30 mail éric tabarly Montgermont"))
# print(G1.geocode("5 North Abbey street cork ireland",limit=2))

# test adress_to_latlong
print(G1.adress_to_latlong("4 allée du clos prioul Montgermont"))

# test latlong_to_adress
print(G1.latlong_to_adress(((48.1572091, -1.6853144))))
# print(G1.reverse_geocode((48.203718, -1.824844)))
print(G1.latlong_to_adress(((48.203718, -1.824844))))

