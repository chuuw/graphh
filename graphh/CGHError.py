import requests

def check_point(l_latlong, api):
    if len(l_latlong) == 0:
        raise ValueError("You must specify at least point")

    if len(l_latlong) < 2 and (api != "geocode" and api != "matrix"):
        raise ValueError("You must specify at least 2 points")
    for point in l_latlong:
        try:
            for coordinate in point:
                float(coordinate)
        except ValueError as e:
            e = ValueError("Coordinates are not valid")
            raise e
        else:
            if not len(point) == 2:
                e = ValueError("Point needs to be lat and long")
                raise e
            elif not (-90 <= point[0] <= 90 and -180 <= point[1] <= 180):
                e = ValueError("Latitude or longitude value is not valid")
                raise e


def check_vehicle(vehicle, prem):
    l_vehicle = ["car", "foot", "bike"]
    l_vehicle_prem = l_vehicle + ["small_truck", "truck", "scooter", "hike", "mtb", "racingbike"]
    if prem == False :
        if not vehicle in l_vehicle:
            e = ValueError("{} is not a valid vehicle, must be in the list : {}".format(vehicle, l_vehicle))
            raise e
    else:
        if not vehicle in l_vehicle_prem:
            e = ValueError("{} is not a valid vehicle, must be in the list : {}".format(vehicle, l_vehicle))
            raise e

def check_unittime(unit):
  l_unit = ["ms", "s", "min", "h"]
  if not unit in l_unit :
      e = ValueError("{} is not a valid time unit, must be in the list : {}".format(unit, l_unit))
      raise e

def check_unitdistance(unit):
  l_unit = ["m", "km"]
  if not unit in l_unit:
      e = ValueError("{} is not a valid distance unit, must be in the list : {}".format(unit, l_unit))
      raise e

def check_boolean(arg):
    if arg not in ["true","false"]:
        raise ValueError("{} is not valid, must be 'true'or 'false'".format(arg))


def CGHError(e):
    if e.response.status_code == 400:
      e = str(e.response.status_code)+" Invalid argument : " + APIKeyRemaining(e) + " remaining credits"
      raise requests.exceptions.HTTPError(e)
    elif e.response.status_code == 401:
      e = str(e.response.status_code)+" Key error"
      raise requests.exceptions.HTTPError(e)
    elif e.response.status_code == 429:
      e = str(e.response.status_code)+" API limit reached"
      raise requests.exceptions.HTTPError(e)
    elif e.response.status_code == 500:
      e = str(e.response.status_code)+" Internal server error : " + APIKeyRemaining(e) + " remaining credits"
      raise requests.exceptions.HTTPError(e)
    elif e.response.status_code == 501:
      e = str(e.response.status_code)+" Vehicle error : " + APIKeyRemaining(e) + " remaining credits"
      raise requests.exceptions.HTTPError(e)


def APIKeyRemaining(error):
    header = error.response.headers
    cpt = header['X-RateLimit-Remaining']
    return cpt

def check_out_array(arg):
    l_out_array = ["distances", "times", "weights"]
    if not arg in l_out_array:
        e = ValueError("{} is not a valid arguments, must be in the list : {}".format(arg, l_out_array))
        raise e

def check_format_matrix(arg):
    l_out_array = ["pandas", "numpy", "default"]
    if not arg in l_out_array:
        e = ValueError("{} is not a valid arguments, must be in the list : {}".format(arg, l_out_array))
        raise e

def check_dim(arg1, arg2, prem):
    if (prem == False) and (arg1 > 5 or arg2 > 5):
        e = ValueError("Sorry you are not premium, you can only put 5 cities")
        raise e
        
def check_package(package_imported, module):
    if not package_imported:
        raise ImportError("{} was not imported correctly.".format(module))
