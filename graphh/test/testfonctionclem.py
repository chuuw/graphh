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
testroute= G1.url_def2("route", {"point" : (G1.formepoint(point1),G1.formepoint(point2)) })

#   marche aussi si on utilise pas la fonction formepoint

testroute1 = G1.url_def2("route", {"point":("51.131,12.414","48.224,3.867")})

#   mais les avantages se trouvent lorsqu'il y a d'autres arguments en
#   entrée de la fonction par exemple geocode(vehicle=car, local=fr, ..) 
vehicle = "car"
locale = "fr"

testgeocodedico = G1.url_def2("geocode", {"point": G1.formepoint(point1),
                                          "vehicle" : vehicle, "locale" : locale})

#alors qu'avec le systeme de liste c'est plus long:

testgeocodeliste = G1.url_def1(["geocode", "point={}".format(G1.formepoint(point1)),
                                "vehicle={}".format(vehicle), "local={}".format(local)])

#   l'inconveniant c'est que lorsque qu'il y a plusieur point
#   il faut les mettre dans un tuple ou une liste
                    

    
