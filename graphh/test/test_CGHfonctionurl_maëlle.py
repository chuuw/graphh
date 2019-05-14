import urllib.request
import json
import unicodedata
#import CGHError

# url complet :
# https://graphhopper.com/api/1/route?point=51.131,12.414&point=48.224,3.867&
# vehicle=ezfke&locale=de&calc_points=false&key=1620b7ee-90b2-4daa-9ef5-4aba2d279978

class GraphHopper(object):
    url = "https://graphhopper.com/api/1/"

    def __init__(self, Ak):
        self.APIkey = Ak
    #initialisation de la classe

    def url_handle(self, api, l_parameters):
        #api: name of the api used
        #l_parameters: list of parameters to insert in the url
        #example of parameter:
        #"point=51.131,12.414" or "locale=en"
        complete_url = GraphHopper.url + api + "?"
        for p in l_parameters:
            complete_url += "&{}".format(p)
        fp = urllib.request.urlopen(complete_url)
        return json.load(fp)

fp1 = open("credentials.json", "r" , encoding = "utf-8")
dossiercle = json.load(fp1)
key_access = dossiercle["graphhopper"]
G1 = GraphHopper(key_access)

#test api route
a="route"
l=["point=51.131,12.414","point=48.224,3.867","key=1620b7ee-90b2-4daa-9ef5-4aba2d279978"]
print(G1.url_handle(a, l))

#test api geocode
a2="geocode"
l2=["point=48.1572091,-1.6853144","key=1620b7ee-90b2-4daa-9ef5-4aba2d279978","reverse=true"]
print(G1.url_handle(a2, l2))
