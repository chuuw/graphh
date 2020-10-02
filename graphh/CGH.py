import requests
import unicodedata
import json
import warnings
from graphh import CGHError



class GraphHopper:
    """
    GraphHopper API class.
    
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
                                  'time': 67674}, ...
    """
    url = "https://graphhopper.com/api/1/"

    def __init__(self, api_key, premium=False):
        self.api_key = api_key
        self.premium = premium

    def _url_requests(self, api, data, request="get"):
        """ This function does an url request (GET or POST) with given parameters

        Parameters
        ----------
        api: str
            name of the api used
        data: dict
            dict of parameters to insert in the url
        request: str, optional
            Type of request : GET or POST
            By default, the request will be GET

        Returns
        -------
        dict
            The dictionary return by url request (GET or POST)
            
        """
        complete_url = GraphHopper.url + api + "?"

        if request.upper() == "POST":
            complete_url += "key={}".format(self.api_key)
            reponse = requests.post(url=complete_url, json=data,
                                    headers={'content-type': 'application/json'})
        else:
            data["key"] = self.api_key
            reponse = requests.get(url=complete_url, params=data)

        try:
            reponse.raise_for_status()
        except requests.exceptions.HTTPError as e:
             CGHError.CGHError(e)

        return reponse.json()



    def _latlong_handle_request(self,l_latlong,request="get"):
        """" This function changes the format of the coordinates according to the request

        Parameters
        ----------
        l_latlong: list
            Tuple list  (latitude, longitude) of the considerated points
        request: str, optional
            Type of request : GET or POST
            By default, the request will be GET

        Returns
        -------
        list
            list of the coordinates according to the request
        """
        l_latlong_handle = []
        if request.upper() == "POST":
            for latlong in l_latlong:
                l_latlong_handle.append([latlong[1], latlong[0]])
        else:
            for point in l_latlong:
                l_latlong_handle.append(','.join([str(latlong) for latlong in point]))

        return l_latlong_handle



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
        a = str(unicodedata.normalize('NFKD',str(address)).encode('ascii', 'ignore'))
        data = dict()
        data["q"] = "{}".format(a.replace(" ", "+"))
        data["limit"] = str(limit)
        data["locale"] = locale
        return self._url_requests("geocode", data)



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
        data = dict()
        data["reverse"] = "true"
        CGHError.check_point([latlong], "geocode")
        data["point"] = "{},{}".format(latlong[0], latlong[1])
        data["locale"] = locale
        return self._url_requests("geocode", data)


    def route(self,  l_latlong, request="get", vehicle="car",
                    locale="en", calc_points="true", instructions="true",
                    points_encoded="true", elevation="false"):
        """This function give an itinerary between given points

        Parameters
        ----------
        l_latlong : list
            Tuple list  (latitude, longitude) of the considerated points
        request: str, optional
            Type of request : GET or POST
            By default, the request will be GET
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
        data = dict()

        CGHError.check_point(l_latlong, "route")
        l_latlong_handle = self._latlong_handle_request(l_latlong, request)
        data["points"] = l_latlong_handle

        CGHError.check_vehicle(vehicle, self.premium)
        data["vehicle"] = vehicle

        data["locale"] = locale

        CGHError.check_boolean(calc_points)
        data["calc_points"] = calc_points

        CGHError.check_boolean(instructions)
        data["instructions"] = instructions

        CGHError.check_boolean(points_encoded)
        data["points_encoded"] = points_encoded

        CGHError.check_boolean(elevation)
        data["elevation"] = elevation

        return self._url_requests("route", data, request)



    def matrix_request(self, l_from_points, l_to_points,request="get",
                    vehicle="car"):
        """This function gives the different possible matrix
            between the points: distance, temp, weight

        Parameters
        ----------
        l_from_points : list
            Tuple list  (latitude, longitude) of the starting points for the routes
        l_to_points : list
            Tuple list (latitude, longitude) of the destination points for the routes
        request: str, optional
            Type of request : GET or POST
            By default, the request will be GET
        vehicle : str, optional
            The type of vehicle chosen in the list : ["car", "foot", "bike"]
            if the acount is not premium
            And can be chosen in the list : ["small_truck", "truck", "scooter",
            "hike", "mtb", "racingbike"] if it is
        Returns
        -------
        dict
            A dictionary containing distances, times and weights matrices
        """
        data = dict()

        CGHError.check_point(l_from_points, "matrix")
        CGHError.check_point(l_to_points, "matrix")
        l_from_points_handle = self._latlong_handle_request(l_from_points, request)
        l_to_points_handle = self._latlong_handle_request(l_to_points, request)

        if (request.upper() == "GET") and (len(l_from_points) == 1 or len(l_to_points) == 1):
            data["from_point"] = l_from_points_handle
            data["to_point"] = l_to_points_handle
        else:
            data["from_points"] = l_from_points_handle
            data["to_points"] = l_to_points_handle

        CGHError.check_vehicle(vehicle, self.premium)
        data["vehicle"] = vehicle

        data["out_arrays"] = ["distances", "times", "weights"]

        return self._url_requests("matrix", data, request)



    def matrix(self,l_from_address, l_to_address,out_array, format="default", vehicle="car", request="get"):
        """This function gives one matrix between the points: distances, times or weights

        Parameters
        ----------
        l_from_address : list
            The list containing the cities, address of the points
        l_to_address : list
            The list containing the cities, address of the points
        out_array: str
            Specifies which array should be included in the response from the list ["distances", "times", "weights"]
            The units of the entries of distances are meters, 
            of times are seconds and of weights is arbitrary and
            it can differ for different vehicles or versions of this API
        format: str, optional
            Specifies how the array should be drawn from the list ["pandas","numpy","default"]
            By default, the array is values "default"       
        vehicle : str, optional
            The type of vehicle chosen in the list : ["car", "foot", "bike"]
            if the acount is not premium
            And can be chosen in the list : ["small_truck", "truck", "scooter",
            "hike", "mtb", "racingbike"] if it is
        request: str, optional
            Type of request : GET or POST
            By default, the request will be GET

        Returns
        -------
        3 possibilities :
            dataframe : data frame
                A data frame  with for names columns the address for l_to_address
                and names rows the address for l_from_address and data of matrix
            matrix : array
                A array data of the function matrix
            list : list
                A list of data list of the function matrix
        """
        CGHError.check_dim(len(l_from_address), len(l_to_address), self.premium)
        CGHError.check_out_array(out_array)
        CGHError.check_format_matrix(format)
        l_from_points = list()
        l_to_points = list()

        for start in l_from_address:
            l_from_points.append(self.address_to_latlong(start))
        for destination in l_to_address:
            l_to_points.append(self.address_to_latlong(destination))

        dic = self.matrix_request(l_from_points, l_to_points, vehicle=vehicle, request=request)

        if format.lower() == "pandas":
            return self.matrix_pandas(dic, out_array, l_from_address, l_to_address)
        elif format.lower() == "numpy":
            matrix = self.matrix_numpy(dic, out_array)
            return matrix
        else:
            liste = dic[out_array]
            return liste
         
    def matrix_pandas(self, dic, out_array, l_from_address, l_to_address):
        """This function gives a dataframe between the points: distances, times or weights

        Parameters
        ----------
        dic: dictionary 
            A dictionary containing distances, times and weights matrices         
        out_array: str
            Specifies which array should be included in the response from the list ["distances", "times", "weights"]
            The units of the entries of distances are meters, 
            of times are seconds and of weights is arbitrary and
            it can differ for different vehicles or versions of this API
        l_from_address : list
            The list containing the cities, address of the points
        l_to_address : list
            The list containing the cities, address of the points     
       
        Returns
        -------
            dataframe : data frame
                A data frame  with for names columns the address for l_to_address
                and names rows the address for l_from_address and data of matrix
        """
        try:
            import pandas
            import numpy
            matrix = numpy.array(dic[out_array])
            dataframe = pandas.DataFrame(matrix.reshape(len(l_from_address), len(l_to_address)), index=l_from_address,
                                         columns=l_to_address)
        except ImportError:
            pandas_imported = False
            numpy_imported = False
            CGHError.check_package(pandas_imported, "pandas")
            CGHError.check_package(numpy_imported, "numpy")
        else:
            return dataframe

    def matrix_numpy(self, dic, out_array):
        """This function gives a matrix (numpy) between the points: distances, times or weights

        Parameters
        ----------
        dic: dictionary 
            A dictionary containing distances, times and weights matrices         
        out_array: str
            Specifies which array should be included in the response from the list ["distances", "times", "weights"]
            The units of the entries of distances are meters, 
            of times are seconds and of weights is arbitrary and
            it can differ for different vehicles or versions of this API     
       
        Returns
        -------
            dataframe : data frame
                A data frame  with for names columns the address for l_to_address
                and names rows the address for l_from_address and data of matrix
        """
        try:
            import numpy
            matrix = numpy.array(dic[out_array])
        except ImportError:
            numpy_imported = False
            CGHError.check_package(numpy_imported, "numpy")
        else:
            return matrix

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
        if abs(lat - 28.62707) < 0.0001 and abs(lng + 80.62087) < 0.0001 :
            warnings.warn("The coordinates match with Cap Canaveral, Florida\n.It can happen when the function can't find the adress. Try adding more informations to your adress, like state or country.",stacklevel=2)
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
        if 'postcode' in d["hits"][0].keys():
            pc = d["hits"][0]["postcode"]
            c = d["hits"][0]["city"]
            l_elem.append(pc)
            l_elem.append(c)
        if 'city' in d["hits"][0].keys():
            c = d["hits"][0]["city"]
            l_elem.append(c)
        else:
            n = d["hits"][0]["name"]
            l_elem.append(n)
        if 'state' in d["hits"][0].keys():
            st = d["hits"][0]["state"]
            l_elem.append(st)
        if 'country' in d["hits"][0].keys():
            c = d["hits"][0]["country"]
            l_elem.append(c)
        a = ""
        for elt in l_elem:
            a += "{} ".format(elt)
        return a.strip()


    def distance(self, l_latlong, unit="m"):
        """This function gives the distance between precised points for a given
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
        if unit == "m":
            return dic["paths"][0]["distance"]
        elif unit == "km":
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
        if unit == "ms":
            return dic["paths"][0]["time"]
        elif unit == "s":
            return (dic["paths"][0]["time"]) / 1000
        elif unit == "min":
            return ((dic["paths"][0]["time"]) / 1000) / 60
        elif unit == "h":
            return (((dic["paths"][0]["time"]) / 1000) / 60) / 60

        
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
        dict = self.route([latlong, latlong], instructions="false",
                          elevation="true", points_encoded="false")
        return dict["paths"][0]["points"]["coordinates"][0][2]

