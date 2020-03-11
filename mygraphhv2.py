import requests# Le package Requests est recommandé pour une interface client HTTP de niveau supérieur ce qui nous permet de gèrer les demandes get et post aisement
import unicodedata
import os
import json
import numpy# package pour matrix notament pour une presentation simple et utilisation pour l'utilisateur si il a
import pandas# de meme
import myCGHError# fichier modifier par rapport a requests et matrix mais pas encore finis en details


# De plus si il y a des prochaines version de ce code ca sera plus simple et possibilité d'implementer les autres api qui utilise notament les demande post ex: optimization
# ou encore avec la version payante augmenter le nombre parametre sur route

# ici on utilise requests au lieu urllib.request car: c'est plus simple et plus genaral
#possibiliter de faire des post avec urllib.request mais plus compliquer
# de plus pour HTTPError il se trouve aussi dans requests donc tres bien, mais a verifier comment reutiliser le code de GHCerror qui traite les HTTPError

class GraphHopper:

    url = "https://graphhopper.com/api/1/"

    def __init__(self, api_key, premium=False):
        #ici pourquoi mettre des attribut priver a voir
        self.api_key = api_key
        self.premium = premium

    def _url_requests(self, api, data, request="get"):


        #Donc ici on a modifier pour q'un utilisateur puisse faire des demande en get ou post puisque graphh le permet
        #mais par defaut on fais des requets en get
        # au lieu de l_parametre j'ai mis data qui est un dico qui contient toutes les données exemple pour geocode : data = {points=}

        complete_url = GraphHopper.url + api + "?"

        if request.upper() == "POST":
            complete_url += "key={}".format(self.api_key)
            reponse = requests.post(url=complete_url, json=data, headers={'content-type': 'application/json'}) # comment je sais voir doc graphhoper et internet request.post pour ces parametre
            # peut etre json si bug http error sinon regarder headers du post
        else:
            data["key"] = self.api_key
            reponse = requests.get(url=complete_url, params=data)#ici la fonction get du module requests vas construire l'adresse avec les infos dans data et donner la reponse

        try: #partie qui gere les erreurs
            reponse.raise_for_status() # ceci est une fonction qui gere les erreurs, c'est-a-dire que si la requete n'est pas valide il vas resortire error sinon none
        except requests.exceptions.HTTPError as e:
             myCGHError.CGHError(e)

        return reponse.json() #ici .json() (dans le module requests) permet de lire la reponse et de la transformer en json


    def _latlong_handle_request(self,l_latlong,request="get"):
        #l'utilisateur envoie les cordonnée en lattitude et longitude

        #ici c'est une fonction qui changer la latlong car ils doivent etre dans des format specifiques par rapport au demande Get et Post
        #pour post : il faut envoyer les coordonnées en inversé exemple : [[longitude,lattitude],[longitude,lattitude]], comment je sais voir la doc de graphhopper qui precise
        #pour get: il faut que les coordonées soit en chaine de caracteres exemple : [ 'longetitude, lattitude' , 'longetitude, lattitude' ]
        # car en get on construit l'url donc il faut le mettre en chaine de caractere (comme ce qu'il y a dans la version precedente)

        l_latlong_handle = []
        if request.upper() == "POST":
            for latlong in l_latlong:
                l_latlong_handle.append([latlong[1], latlong[0]])
        else:
            for point in l_latlong:
                l_latlong_handle.append(','.join([str(latlong) for latlong in point]))

        #pour comprendre : print(l_latlon_handle)
        return l_latlong_handle


    def route(self,  l_latlong, request="get", vehicle="car", locale="en", calc_points="true", instructions="true", points_encoded="true", elevation="false"):
        # ici pour faire une demande il faut creer le data qui est un dico
        # donc au lieu de faire leur liste on a fais un dico et qui sera generique peut import la demande post ou get
        # sauf pour les coordonnee que je traite avec une fonction

        data = dict()

        myCGHError.check_point(l_latlong, "route")
        l_latlong_handle = self._latlong_handle_request(l_latlong, request)
        data["points"] = l_latlong_handle

        myCGHError.check_vehicle(vehicle, self.premium)
        data["vehicle"] = vehicle

        #manque un check pour locale on peut en creer un
        data["locale"] = locale

        myCGHError.check_boolean(calc_points)
        data["calc_points"] = calc_points

        myCGHError.check_boolean(instructions)
        data["instructions"] = instructions

        myCGHError.check_boolean(points_encoded)
        data["points_encoded"] = points_encoded

        myCGHError.check_boolean(elevation)
        data["elevation"] = elevation

        return self._url_requests("route", data, request)

    def geocode(self, address, limit=1, locale="en"):
        #ici pareil on a fais un dico et que demande en get car y a pas post pour geocode
        #on peut rajouter un fournisseur mais a voir si on rajoute

        a = str(unicodedata.normalize('NFKD',str(address)).encode('ascii', 'ignore'))
        data = dict()
        data["q"] = "{}".format(a.replace(" ", "+"))
        data["limit"] = str(limit)
        data["locale"] = locale
        return self._url_requests("geocode", data)


    def reverse_geocode(self, latlong, locale="en"):
        #ici pareil
        data = dict()
        data["reverse"] = "true"
        myCGHError.check_point([latlong], "geocode")
        data["point"] = "{},{}".format(latlong[0], latlong[1])
        data["locale"] = locale
        return self._url_requests("geocode", data)



    def matrix(self, l_from_points, l_to_points, vehicle="car",request="get",fail_fast="true"):

        data = dict()
        #faire un check mais vas falloir changé le code GHC error, c-a-d on aura ca :
        #CGHError.check_point(l_latlong, "matrix")

        l_from_points_handle = self._latlong_handle_request(l_from_points, request)
        l_to_points_handle = self._latlong_handle_request(l_to_points, request)

        #ici on gere le faite que se soit une matice  par emple 1*3 ou 3*1, juste qui change c'est un "s" de point car sinon message error
        if (request.upper() == "GET") and (len(l_from_points) == 1 or len(l_to_points) == 1):
            data["from_point"] = l_from_points_handle
            data["to_point"] = l_to_points_handle
        else:
            data["from_points"] = l_from_points_handle
            data["to_points"] = l_to_points_handle

        myCGHError.check_vehicle(vehicle, self.premium)
        data["vehicle"] = vehicle

        # ici demande de matrix en post ou get , out_arrays sera toujours ses valeurs :
        data["out_arrays"] = ["distances", "times", "weights"]

        myCGHError.check_boolean(fail_fast.lower())
        data["fail_fast"] = fail_fast.lower()

        return self._url_requests("matrix", data, request)


    def matrix_numpy(self,l_from_points, l_to_points, out_array):
        myCGHError.check_out_array(out_array) #voir le fichier myGHCError
        # avec le module numpy
        dic = self.matrix(l_from_points, l_to_points)
        matrix = numpy.array(dic[out_array])
        return matrix

    def matrix_pandas(self,l_from_points, l_to_points, out_array):

        # avec pandas, on peut faire aussi avec numpy pour faciliter le code
        myCGHError.check_out_array(out_array)
        dic = self.matrix(l_from_points, l_to_points)
        matrix = dic[out_array]
        data = dict()
        for i in range(len(l_to_points)):
            data[str(l_to_points[i])] = matrix[i]
        for val in l_from_points:
            str(val)
        dataframe = pandas.DataFrame(data, index=l_from_points)
        return dataframe

    def matrix_liste(self, l_from_points, l_to_points, out_array):

        myCGHError.check_out_array(out_array)

        #sans le module numpy
        dic = self.matrix(l_from_points, l_to_points)
        matrix = dic[out_array]
        print(matrix)
        # on a essayer de faire une affichage fait maisson sans module
        self.affichagematrix(l_from_points, l_to_points, matrix)
        return matrix

    def affichagematrix(self, l_from_points, l_to_points, matrix):
        chaine = ""
        villedepart = ""
        cpt = 0
        for ville in l_from_points:
            villedepart += "\t{}".format(ville)

        chaine += villedepart+"\n"

        while cpt != len(matrix):
            liste = matrix[cpt]
            val = '\t'.join(str(elem) for elem in liste)
            chaine += "{}\t{}\n".format(l_to_points[cpt], val)
            cpt += 1

        print(chaine)


    # pour le reste fonction inchanger :

    def address_to_latlong(self, address):
        d = self.geocode(address, limit=1)
        lat = d["hits"][0]["point"]["lat"]
        lng = d["hits"][0]["point"]["lng"]
        return lat, lng


    def latlong_to_address(self, latlong):
        d = self.reverse_geocode(latlong)
        l_elem = []
        if "housenumber" in d["hits"][0].keys():
            num = d["hits"][0]["housenumber"]
            l_elem.append(num)
        if "street" in d["hits"][0].keys():
            st = d["hits"][0]["street"]
            l_elem.append(st)
        pc = d["hits"][0]["postcode"]
        l_elem.append(pc)
        c = d["hits"][0]["city"]
        l_elem.append(c)
        a = ""
        for elt in l_elem:
            a += "{} ".format(elt)
        return a.strip()

    def distance(self, l_latlong, unit="m"):
        dic = self.route(l_latlong, points_encoded="flase")
        myCGHError.check_unitdistance(unit)
        if unit == "m":
            return dic["paths"][0]["distance"]
        elif unit == "km":
            return (dic["paths"][0]["distance"]) / 1000

    def duration(self, l_latlong, vehicle="car", unit="ms"):
        dic = self.route(l_latlong, vehicle, points_encoded="false")
        myCGHError.check_unittime(unit)
        if unit == "ms":
            return dic["paths"][0]["time"]
        elif unit == "s":
            return (dic["paths"][0]["time"]) / 1000
        elif unit == "min":
            return ((dic["paths"][0]["time"]) / 1000) / 60
        elif unit == "h":
            return (((dic["paths"][0]["time"]) / 1000) / 60) / 60



#programme pricipale

# recuperer ma key :
dossier = "data"
fichier = "credentials.json"
chemin = os.path.join(dossier, fichier)
fp = open(chemin, "r", encoding="utf8")
dico = json.load(fp)
key = dico.get("GraphHopper", None)
monObjet = GraphHopper(api_key=key)

#Les tests :

# print(monObjet.route([(48.1113387, 2.3309152144131775), (48.1113387, -1.6800198)]),)
# print(monObjet.route([(48.1113387, 2.3309152144131775), (48.1113387, -1.6800198)], "POST"))
#
# print(monObjet.reverse_geocode([48.878743, 2.3309152144131775]))
# print(monObjet.address_to_latlong("Rennes"))
# print(monObjet.latlong_to_address([48.878743, 2.3309152144131775]))
# print(monObjet.distance([[48.878743, 2.3309152144131775], [48.1113387, -1.6800198]]))
# print(monObjet.duration([[48.878743, 2.3309152144131775], [48.1113387, -1.6800198]]))



#Pour matrix :
list_from_points = [(48.978743, 2.3309152144131775), (48.5113387, -1.6800198), (48.1113387, -1.6800198)]
list_to_points = [(48.978743, 2.3309152144131775), (48.5113387, -1.6800198), (48.1113387, -1.6800198)]


# print(monObjet.matrix(list_from_points, list_to_points))
# print(monObjet.matrix(list_from_points, list_to_points, request="POST"))
#
# print(monObjet.matrix_numpy(list_from_points, list_to_points, "distances"))
print(monObjet.matrix_pandas(list_from_points, list_to_points, "distances"))
# print(monObjet.reverse_geocode([51.512882367963456,-0.09576559066772462]))
#
# print(monObjet.matrixliste(list_from_points, list_to_points, "distances"))