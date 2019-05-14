import urllib.request
import json
import unicodedata
import CGHError

# url complet :
# https://graphhopper.com/api/1/route?point=51.131,12.414&point=48.224,3.867&
# vehicle=ezfke&locale=de&calc_points=false&key=1620b7ee-90b2-4daa-9ef5-4aba2d279978

class GraphHopper(object):
    url = "https://graphhopper.com/api/1/"

    def __init__(self, Ak):
        self.APIkey = Ak
    #initialisation de la classe


    def geocode(self, adresse, limite=1):
        # prend en entrée une adresse en chaîne de caractère
        # retourne un dictionnaire
        adresse = str(unicodedata.normalize('NFKD', str(adresse)).encode('ascii', 'ignore'))
        url1=GraphHopper.url+"geocode?q="+adresse.replace(" ","+")+"&limit="+str(limite)+"&key="+self.APIkey
        fp = urllib.request.urlopen(url1)
        dico = fp.read().decode("utf-8")
        return dico

    def reverse_geocode(self, latlong):
        # prend en entrée un tuple (la lattitude et la longitude)
        # retourne un dictionnaire
        url2=GraphHopper.url+"geocode?point="+str(latlong[0])+","+str(latlong[1])+"&reverse=true&key="+self.APIkey
        fp = urllib.request.urlopen(url2)
        d_res = json.load(fp)
        return d_res


    def itinerary(self, point1, point2, vehicle="car"):
        # prend en entrée 2 tuples (lat, long)
        # retourne un dictionnaire
        if CGHError.pointerror(point1) and CGHError.pointerror(point2):
            url = GraphHopper.url + "route?point=" + str(point1[0])+ "," + str(point1[1]) + "&point=" + str(point2[0]) + "," + str(point2[1]) + "&vehicle=" + vehicle + "&key=" + self.APIkey
            if CGHError.CGHError(url):
                fp = urllib.request.urlopen(url)
                return json.load(fp)

    def distance(self, point1, point2):
        if CGHError.pointerror(point1) and CGHError.pointerror(point2):
            url = GraphHopper.url + "route?point=" + str(point1[0]) + "," + str(point1[1]) + "&point=" + str(point2[0]) + "," + str(point2[1]) + "&key=" + self.APIkey
            fp = urllib.request.urlopen(url)
            dic=json.load(fp)
            return "distance : "+str(dic["paths"][0]["distance"])+" m"


    def time(self, point1, point2, vehicle="car"):
        if CGHError.pointerror(point1) and CGHError.pointerror(point2):
            url = GraphHopper.url + "route?point=" + str(point1[0]) + "," + str(point1[1]) + "&point=" + str(point2[0]) + "," + str(point2[1]) + "&vehicle=" + vehicle +  "&key=" + self.APIkey
            fp = urllib.request.urlopen(url)
            dic=json.load(fp)
            return "time : "+str(dic["paths"][0]["time"])+" ms"

    #def repr_itinerary(self):

