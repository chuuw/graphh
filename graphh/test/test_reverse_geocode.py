import os
import sys

sys.path.append(os.path.join(".."))

import CGH
import json


fp1 = open(os.path.join('..', "credentials.json"), "r", encoding="utf-8")
key_file = json.load(fp1)
key_access = key_file["graphhopper"]

G1 = CGH.GraphHopper(key_access)

print(G1.reverse_geocode((48.1572091, -1.6853144)))
# print(G1.reverse_geocode((48.1572091, -1.6853144, "a"))) --> ValueError

