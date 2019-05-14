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

    def geocode(self, adresse, limite=1):
        # prend en entrée une adresse en chaîne de caractère
        # retourne un dictionnaire
        adresse = str(unicodedata.normalize('NFKD', str(adresse)).encode('ascii', 'ignore'))
        url1=GraphHopper.url+"geocode?q="+adresse.replace(" ","+")+"&limit="+str(limite)+"&key="+self.APIkey
        fp = urllib.request.urlopen(url1)
        dico = json.load(fp)
        return dico

    def reverse_geocode(self, latlong):
        # prend en entrée un tuple (la lattitude et la longitude)
        # retourne un dictionnaire
        l_param=[]
        l_param.append("point={},{}".format(latlong[0],latlong[1]))
        l_param.append("key={}".format(self.APIkey))
        l_param.append("reverse=true")
        return self.url_handle("geocode",l_param)


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


fp1 = open("credentials.json", "r" , encoding = "utf-8")
dossiercle = json.load(fp1)
key_access = dossiercle["graphhopper"]

G1 = GraphHopper(key_access)
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
