import urllib.request
import json
import unicodedata

from graphh import CGHError
from urllib.error import HTTPError


class GraphHopper(object):
    url = "https://graphhopper.com/api/1/"

    def __init__(self, ak, premium = False):
        self.APIkey = ak
        self.prem = premium
    # initialisation of the class

    def url_handle(self, api, l_parameters):
        """
         api: name of the api used
         l_parameters: list of parameters to insert in the url
         example of parameter:
         "point=51.131,12.414" or "locale=en"
         """
        complete_url = GraphHopper.url + api + "?"
        for p in l_parameters:
            complete_url += "&{}".format(p)
        complete_url += "&key=" + self.APIkey
        try:
            fp = urllib.request.urlopen(complete_url)
            result = json.load(fp)
        except HTTPError as e:
            CGHError.CGHError(e)
        else:
            return result


    def geocode(self, address, limit=1, locale="en"):
        """
        :param address:
        :param limit:
        :param locale:
        :return dictionary:
        """
        a = str(unicodedata.normalize('NFKD', str(address)).encode('ascii', 'ignore'))
        l_param = []
        l_param.append("q={}".format(a.replace(" ", "+")))
        l_param.append("limit={}".format(str(limit)))
        l_param.append("locale={}".format(locale))

        return self.url_handle("geocode", l_param)

    def reverse_geocode(self, latlong, locale="en"):
        """
        :param latlong:
        :param locale:
        :return dictionary:
        """
        l_param = []
        l_param.append("reverse=true")

        CGHError.check_point(latlong)
        l_param.append("point={},{}".format(latlong[0], latlong[1]))
        l_param.append("locale={}".format(locale))

        return self.url_handle("geocode", l_param)

    def route(self, l_latlong , vehicle="car", locale="en"):
        """
        :param latlong1:
        :param latlong2:
        :param vehicle:
        :param locale:
        :return dictionary:
        """
        l_param = []

        CGHError.check_point(l_latlong)
        for latlong in l_latlong :
            l_param.append("point={},{}".format(latlong[0], latlong[1]))

        CGHError.check_vehicle(vehicle, self.prem)
        l_param.append("vehicle={}".format(vehicle))

        l_param.append("locale={}".format(locale))

        return self.url_handle("route", l_param)

    def distance(self, l_latlong, unit="m"):
        dic = self.route(l_latlong)
        CGHError.check_unitdistance(unit)
        if unit == "m" :
            return dic["paths"][0]["distance"]
        elif unit == "km" :
            return (dic["paths"][0]["distance"]) / 1000

    def time(self, l_latlong, vehicle="car", unit="ms"):
        dic = self.route(l_latlong, vehicle)
        CGHError.check_unittime(unit)
        if  unit == "ms" :
            return dic["paths"][0]["time"]
        elif unit == "s" :
            return (dic["paths"][0]["time"])/1000
        elif unit == "min" :
            return ((dic["paths"][0]["time"]) / 1000) / 60
        elif unit == "h" :
            return (((dic["paths"][0]["time"]) / 1000) / 60) / 60

    def adress_to_latlong(self, adress):
        d = self.geocode(adress, limit=1)
        lat = d["hits"][0]["point"]["lat"]
        lng = d["hits"][0]["point"]["lng"]
        return lat, lng

    def latlong_to_adress(self, latlong):
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
