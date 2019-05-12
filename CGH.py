import urllib.request
import json
import urllib.parse
import unicodedata

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

    #def reverse_geocode(self ,point):
        # prend en entrée un tuple (la lattitude et la longitude)
        # retourne un dictionnaire

    def itinerary(self, point1, point2, vehicle="car"):
        # prend en entrée 2 tuples (lat, long)
        # retourne un dictionnaire
        url = GraphHopper.url + "route?point=" + str(point1[0])+ "," + str(point1[1]) + "&point=" + str(point2[0]) + "," + str(point2[1]) + "&vehicle=" + vehicle + "&key=" + self.APIkey
        print(url)
        fp = urllib.request.urlopen(url)
        return json.load(fp)

    #def distance(self):

    #def time(self):

    #def repr_itinerary(self):


fp1 = open("credentials.json", "r" , encoding = "utf-8")
dossiercle = json.load(fp1)
key_access = dossiercle["graphhopper"]

G1 = GraphHopper(key_access)
print(G1)
point1 = (48.224,3.867)
point2 = (51.131,12.414)
print(G1.geocode(9))
print(G1.itinerary(point1,point2))

      

