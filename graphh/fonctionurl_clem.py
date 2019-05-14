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
    def formepoint(self, point):
        return "{},{}".format(point[0],point[1])
        
    def url_def(self, listedargument):
        url = GraphHopper.url + listedargument[0] + "?"
        for argument in listedargument[1:]:
            url += argument + "&"
        url += "key=" + self.APIkey

        fp = urllib.request.urlopen(url)
        d_res = json.load(fp)
        return d_res

    def url_def2(self, api, dicodargument):
        url = GraphHopper.url + api + "?"
        for argument in dicodargument.keys():
            if type(dicodargument[argument]) == tuple or list:
                for arg in dicodargument[argument]:
                    url += "{}={}&".format(argument, arg)
            else:
                url += "{}={}&".format(argument, dicodargument[argument])
            
        url += "key=" + self.APIkey
        fp = urllib.request.urlopen(url)
        d_res = json.load(fp)
        return d_res
