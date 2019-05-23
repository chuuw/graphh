import urllib.request
import json
import unicodedata
import CGHError

class GraphHopper(object):
    url = "https://graphhopper.com/api/1/"

    def __init__(self, ak):
        self.APIkey = ak
    # initialisation of the class

    def url_handle(self, api, l_parameters):
        # api: name of the api used
        # l_parameters: list of parameters to insert in the url
        # example of parameter:
        # "point=51.131,12.414" or "locale=en"
        complete_url = GraphHopper.url + api + "?"
        for p in l_parameters:
            complete_url += "&{}".format(p)
        complete_url += "&key=" + self.APIkey
        if CGHError.CGHError(complete_url):
            fp = urllib.request.urlopen(complete_url)
            return json.load(fp)

    def geocode(self, address, limit=1, locale = "en"):
        """
        :param address:
        :param limit:
        :return dictionary:
        """
        a = str(unicodedata.normalize('NFKD', str(address)).encode('ascii', 'ignore'))
        l_param = []
        l_param.append("q={}".format(a.replace(" ", "+")))
        l_param.append("limit={}".format(str(limit)))
        if CGHError.valid_locale(locale):
            l_param.append("locale={}".format(locale))
        return self.url_handle("geocode",l_param)

    def reverse_geocode(self, latlong):
        """
        :param latlong:
        :return dictionary:
        """
        l_param = []
        if CGHError.valid_point(latlong):
            l_param.append("point={},{}".format(latlong[0], latlong[1]))
        l_param.append("reverse=true")
        return self.url_handle("geocode", l_param)

    def itinerary(self, latlong1, latlong2, vehicle="car", locale="en"):
        """
        :param latlong1:
        :param latlong2:
        :param vehicle:
        :return dictionary:
        """
        l_param = []
        if CGHError.valid_point(latlong1) and CGHError.valid_point(latlong2):
            l_param.append("point={},{}".format(latlong1[0], latlong1[1]))
            l_param.append("point={},{}".format(latlong2[0], latlong2[1]))
        if CGHError.valid_vehicle(vehicle):
            l_param.append("vehicle={}".format(vehicle))
        if CGHError.valid_locale(locale):
            l_param.append("locale={}".format(locale))
        return self.url_handle("route", l_param)

    def distance(self, latlong1, latlong2):
        dic = self.itinerary(latlong1, latlong2)
        return dic["paths"][0]["distance"]

    def time(self, latlong1, latlong2, vehicle="car"):
        dic = self.itinerary(latlong1, latlong2, vehicle)
        return dic["paths"][0]["time"]

    def adress_to_latlong(self, adress):
        d = self.geocode(adress, limit=1)
        lat = d["hits"][0]["point"]["lat"]
        long = d["hits"][0]["point"]["lng"]
        return (lat, long)

    def latlong_to_adress(self, latlong):
        d = self.reverse_geocode(latlong)
        

