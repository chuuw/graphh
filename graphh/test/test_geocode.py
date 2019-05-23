import os
import sys

sys.path.append(os.path.join(".."))

import CGH
import json


fp1 = open(os.path.join('..', "credentials.json"), "r", encoding="utf-8")
key_file = json.load(fp1)
key_access = key_file["graphhopper"]

G1 = CGH.GraphHopper(key_access)

print(G1.geocode("4 allée du clos prioul Montgermont"))
print(G1.geocode("30 mail éric tabarly Montgermont"))
print(G1.geocode("5 North Abbey street cork ireland",limit=2))



