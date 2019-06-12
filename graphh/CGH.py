import urllib.request
import json
import unicodedata

from graphh import CGHError
from urllib.error import HTTPError


class GraphHopper(object):
    """

    """
    url = "https://graphhopper.com/api/1/"

    def __init__(self, ak, premium = False):
        self.APIkey = ak
        self.prem = premium

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
        """This function does geocoding.
        It transforms a given address into matching geographic coordinates.

        Parameters
        ----------
        address : str
            The address of the location that needs to be transformed.
        limit : int, optional
            The number of matching location you would like to get.
            By default, the function will only return one location.
        locale : str, optional
            The language of the answer.
            By default, the answer will be in english.

        Returns
        -------
        dict
            A dictionary containing the matching locations' information,
            including their geographic coordinates, and the number of ms it took.

        """
        a = str(unicodedata.normalize('NFKD', str(address)).encode('ascii', 'ignore'))
        l_param = []
        l_param.append("q={}".format(a.replace(" ", "+")))
        l_param.append("limit={}".format(str(limit)))
        l_param.append("locale={}".format(locale))
        return self.url_handle("geocode", l_param)

    def reverse_geocode(self, latlong, locale="en"):
        """This function does reverse geocoding.
        It transforms given geographic coordinates into matching addresses.

        Parameters
        ----------
        latlong : tuple
            The geographic coordinates that need to be transformed.
            The first element is the latitude and the second one is the longitude.
        locale : str, optional
            The language of the answer.
            By default, the answer will be in english.

        Returns
        -------
        dict
            A dictionary containing the matching locations' information,
            including their addresses, and the number of ms it took.

        """
        l_param = []
        l_param.append("reverse=true")
        CGHError.check_point(latlong)
        l_param.append("point={},{}".format(latlong[0], latlong[1]))
        l_param.append("locale={}".format(locale))
        return self.url_handle("geocode", l_param)

    def route(self, l_latlong , vehicle="car", locale="en",
              calc_points="true", instructions="true",
              points_encoded="true", elevation="false"):
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

        CGHError.check_boolean(instructions)
        l_param.append("instructions={}".format(instructions))

        CGHError.check_boolean(calc_points)
        l_param.append("calc_points={}".format(calc_points))

        CGHError.check_boolean(points_encoded)
        l_param.append("points_encoded={}".format(points_encoded))

        CGHError.check_boolean(elevation)
        l_param.append("elevation={}".format(elevation))

        return self.url_handle("route", l_param)

    def distance(self, l_latlong, unit="m"):
        dic = self.route(l_latlong, points_encoded="false")
        CGHError.check_unitdistance(unit)
        if unit == "m" :
            return dic["paths"][0]["distance"]
        elif unit == "km" :
            return (dic["paths"][0]["distance"]) / 1000

    def time(self, l_latlong, vehicle="car", unit="ms"):
        dic = self.route(l_latlong, vehicle, points_encoded="false")
        CGHError.check_unittime(unit)
        if  unit == "ms" :
            return dic["paths"][0]["time"]
        elif unit == "s" :
            return (dic["paths"][0]["time"])/1000
        elif unit == "min" :
            return ((dic["paths"][0]["time"]) / 1000) / 60
        elif unit == "h" :
            return (((dic["paths"][0]["time"]) / 1000) / 60) / 60

    def adress_to_latlong(self, address):
        """This function is a simplified version of the previous geocoding function.

        Parameters
        ----------
        address : str
            The address of the location that needs to be transformed.

        Returns
        -------
        tuple
            A tuple corresponding to the geographic coordinates of the location.
            The first element is the latitude and the second one is the longitude.

        """
        d = self.geocode(address, limit=1)
        lat = d["hits"][0]["point"]["lat"]
        lng = d["hits"][0]["point"]["lng"]
        return lat, lng

    def latlong_to_adress(self, latlong):
        """This function is a simplified version the previous reverse geocoding function.

        Parameters
        ----------
        latlong : tuple
            The geographic coordinates that need to be transformed.
            The first element is the latitude and the second one is the longitude.

        Returns
        -------
        str
            The address of the location.

        """
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

    def elevation_point(self, point):
        dict = self.route([point,point],instructions="false", elevation="true", points_encoded= "false")
        return dict["paths"][0]["points"]["coordinates"][0]
        #lat and long are inverse
