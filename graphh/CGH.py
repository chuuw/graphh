# coding: utf-8
import json
import unicodedata

from graphh import CGHError
from urllib.request import urlopen
from urllib.error import HTTPError

class GraphHopper(object):
    """GraphHopper API class.

    Parameters
    ----------
     api_key: str
        API key to be used for queries
     premium: bool
        Whether the account corresponding to this key is a premium account
        or not

    Examples
    --------
    >>> from graphh import GraphHopper
    >>> gh_client = GraphHopper(api_key=YOUR_API_KEY)
    >>> gh_client.address_to_latlong("Rennes, République")
    (48.1098593, -1.6787526)
    >>> latlong_Paris = gh_client.address_to_latlong("Paris")
    >>> latlong_Madrid = gh_client.address_to_latlong("Madrid")
    >>> gh_client.distance([latlong_Paris, latlong_Madrid], unit="km")
    1269.9657
    >>> gh_client.duration([latlong_Paris, latlong_Madrid], unit="h")
    11.641364444444443
    >>> import pprint
    >>> pprint.pprint(gh_client.route([latlong_Paris, latlong_Madrid]))
    {'hints': {'visited_nodes.average': '947.0', 'visited_nodes.sum': '947'},
     'info': {'copyrights': ['GraphHopper', 'OpenStreetMap contributors'],
              'took': 43},
     'paths': [{'ascend': 11624.469142794609,
                'bbox': [-3.778313, 40.412748, 2.346683, 48.878851],
                'descend': 11026.474138140678,
                'details': {},
                'distance': 1269965.7,
                'instructions': [{'distance': 246.715,
                                  'heading': 165.02,
                                  'interval': [0, 2],
                                  'sign': 0,
                                  'street_name': 'Rue Blanche',
                                  'text': 'Continue onto Rue Blanche',
                                  'time': 67674},
    ...
    """
    url = "https://graphhopper.com/api/1/"

    def __init__(self, api_key, premium=False):
        self.api_key = api_key
        self.premium = premium

    def _url_handle(self, api, l_parameters):
        """This function does an url request with given parameters

        Parameters
        ----------
         api: str
            name of the api used
         l_parameters: list
            list of parameters to insert in the url

        Returns
        -------
        dict
            The dictionary return by url request
         """
        complete_url = GraphHopper.url + api + "?"
        for p in l_parameters:
            complete_url += "&{}".format(p)
        complete_url += "&key=" + self.api_key
        try:
            fp = urlopen(complete_url)
            data = fp.read()
            encoding = fp.info().get_content_charset('utf-8')
            result = json.loads(data.decode(encoding))
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
            including their geographic coordinates, and the number of ms it
            took.

        """
        a = str(unicodedata.normalize('NFKD',
                                      str(address)).encode('ascii', 'ignore'))
        l_param = []
        l_param.append("q={}".format(a.replace(" ", "+")))
        l_param.append("limit={}".format(str(limit)))
        l_param.append("locale={}".format(locale))
        return self._url_handle("geocode", l_param)

    def reverse_geocode(self, latlong, locale="en"):
        """This function does reverse geocoding.
        It transforms given geographic coordinates into matching addresses.

        Parameters
        ----------
        latlong : tuple
            The geographic coordinates that need to be transformed.
            The first element is the latitude and the second one is the
            longitude.
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
        CGHError.check_point([latlong], "geocode")
        l_param.append("point={},{}".format(latlong[0], latlong[1]))
        l_param.append("locale={}".format(locale))
        return self._url_handle("geocode", l_param)

    def route(self, l_latlong , vehicle="car", locale="en",
              calc_points="true", instructions="true",
              points_encoded="true", elevation="false"):
        """This function give an itinerary between given points

        Parameters
        ----------
        l_latlong : tuple list
            The tuple list (latitude, longitude) of the considerated points
        vehicle : str, optional
            The type of vehicle chosen in the list : ["car", "foot", "bike"]
            if the acount is not premium
            And can be chosen in the list : ["small_truck", "truck", "scooter",
            "hike", "mtb", "racingbike"] if it is
        locale : str, optional
            The language of the answer.
            By default, the answer will be in english.
        calc_points : boolean, optional
            If the points for the route should be calculated at all.
            default = true
        instructions : boolean, optional
            If instructions should be calculated and returned
            default = true
        points_encoded : boolean, optional
            If false, the coordinates in point and snapped_waypoints are
            returned as lists of positions
            using the order [lon,lat,elevation]. If true, the coordinates will
            be encoded as a string.
            default = true
        elevation : boolean, optional
            If true, a third coordinate, the altitude, is included to all
            positions in the response

        Returns
        -------
        dict
            A dictionary of the matching itinerary containing distance, time,
            ascend, descend, points (encoded or not),
            instructions with street name and description what the user has to
            do in order to follow the route.
        """
        l_param = []

        CGHError.check_point(l_latlong, "route")
        for latlong in l_latlong:
            l_param.append("point={},{}".format(latlong[0], latlong[1]))

        CGHError.check_vehicle(vehicle, self.premium)
        l_param.append("vehicle={}".format(vehicle))

        l_param.append("locale={}".format(locale))

        CGHError.check_boolean(instructions)
        l_param.append("instructions={}".format(instructions.lower()))

        CGHError.check_boolean(calc_points)
        l_param.append("calc_points={}".format(calc_points.lower()))

        CGHError.check_boolean(points_encoded)
        l_param.append("points_encoded={}".format(points_encoded.lower()))

        CGHError.check_boolean(elevation)
        l_param.append("elevation={}".format(elevation.lower()))

        return self._url_handle("route", l_param)

    def distance(self, l_latlong, unit="m"):
        """This function give the distance between precised points for a given
        itinerary

        Parameters
        ----------
        l_latlong: list
            The list of the tuples (latitude, longitude) of the considerated
            points
        unit: str
            The unit of the distance returned chosen between "m" and "km"
            By default the unit will be in meters

        Returns
        -------
        float
            The number of the distance for the itinerary for the unit chosen
        """
        dic = self.route(l_latlong, points_encoded="false")
        CGHError.check_unitdistance(unit)
        if unit == "m" :
            return dic["paths"][0]["distance"]
        elif unit == "km" :
            return (dic["paths"][0]["distance"]) / 1000

    def duration(self, l_latlong, vehicle="car", unit="ms"):
        """This function give the time between precised points for a given
        itinerary

        Parameters
        ----------
        l_latlong: list
            The list of the tuples (latitude, longitude) of the considerated
            points
        vehicle: str
            The type of vehicle chosen in the list : ["car", "foot", "bike"]
            if the acount is not premium
            And can be chosen in the list : ["small_truck", "truck", "scooter",
            "hike", "mtb", "racingbike"] if it is
            By default the vehicle will be car
        unit: str
            The unit of the distance returned chosen between "ms", "s", "min"
            and "h"
            By default the unit will be in milliseconds

        Returns
        -------
        float
            The number of the time for the itinerary for the unit and vehicle
            chosen
        """
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

    def address_to_latlong(self, address):
        """This function is a simplified version of the geocoding function.

        Parameters
        ----------
        address : str
            The address of the location that needs to be transformed.

        Returns
        -------
        tuple
            A tuple corresponding to the geographic coordinates of the
            location.
            The first element is the latitude and the second one is the
            longitude.

        """
        d = self.geocode(address, limit=1)
        lat = d["hits"][0]["point"]["lat"]
        lng = d["hits"][0]["point"]["lng"]
        return lat, lng

    def latlong_to_address(self, latlong):
        """This function is a simplified version of the reverse geocoding
        function.

        Parameters
        ----------
        latlong : tuple
            The geographic coordinates that need to be transformed.
            The first element is the latitude and the second one is the
            longitude.

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

    def elevation_point(self, latlong):
        """This function give an elevation for a given geographic coordinates

        Parameters
        ----------
        latlong : tuple
            The geographic coordinates that need to be transformed.
            The first element is the latitude and the second one is the
            longitude.

        Returns
        -------
        float
            Elevation of one geographic coordinate couple
        """
        dict = self.route([latlong,latlong],instructions="false",
                          elevation="true", points_encoded= "false")
        return dict["paths"][0]["points"]["coordinates"][0][2]
