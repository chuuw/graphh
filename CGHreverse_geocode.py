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

    def reverse_geocode(self ,point):
        # prend en entrée un tuple (la lattitude et la longitude)
        # retourne un dictionnaire
        url2=GraphHopper.url+"geocode?point="+str(point[0])+","+str(point[1])+"&reverse=true&key="+self.APIkey
        # pour que ça marche bien il faut forcément que les coordonnées géographiques
        # soient données dans le bon ordre du coup
        fp = urllib.request.urlopen(url2)
        d_res = json.load(fp)
        return d_res

    #def itinerary(self, point1, point2, vehicule="car", limite=1):
        # prend en entrée 2 tuples (lat, long)
        # retourne un dictionnaire

    #def distance(self):

    #def time(self):

    #def repr_itinerary(self):


fp1 = open("credentials.json", "r" , encoding = "utf-8")
dossiercle = json.load(fp1)
key_access = dossiercle["graphhopper"]

G1 = GraphHopper(key_access)
print(G1)

#print(G1.geocode(9))

#test reverse_geocode
print(G1.reverse_geocode((48.1572091,-1.6853144)))
d=G1.reverse_geocode((48.1572091,-1.6853144))
#for elt in d["hits"]:
#    print(elt)
print(d["hits"][0]["street"])

