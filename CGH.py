import urllib.request
import json

# url complet :
# https://graphhopper.com/api/1/route?point=51.131,12.414&point=48.224,3.867&
# vehicle=ezfke&locale=de&calc_points=false&key=1620b7ee-90b2-4daa-9ef5-4aba2d279978

class GraphHopper(object):
    url = "https://graphhopper.com/api/1/"

    def __init__(self, Ak):
        self.APIkey = Ak
    #initialisation de la classe





fp1 = open("credentials.json", "r" , encoding = "utf-8")
dossiercle = json.load(fp1)
key_access = dossiercle["graphhopper"]

G1 = GraphHopper(key_access)

