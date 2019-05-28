from urllib.error import HTTPError
import urllib.request
import sys
import json


def check_point(point):
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


def check_vehicle(vehicle):
    l_vehicle = [
        "car", "small_truck", "truck",
        "scooter", "foot", "hike",
        "bike", "mtb", "racingbike"
    ]
    if not vehicle in l_vehicle:
        e = ValueError("{} is not a valid vehicle".format(vehicle))
        raise e


def check_locale(locale):
    l_locale = ["en", "fr", "de", "it"]
    if not locale in l_locale:
        e = ValueError("{} is not a valid language".format(locale))
        raise e


def valid_unittime(unit):
  l_unit = ["ms", "s", "min", "h"]
  if unit in l_unit :
    return True
  else:
    print("Error : wrong time unit")
    sys.exit()


def valid_unitdistance(unit):
  l_unit = ["m", "km"]
  if unit in l_unit :
    return True
  else:
    print("Error : wrong distance unit")
    sys.exit()


def CGHError(e):
    if e.code == 400:
      e.msg= "argument not correct"
      raise HTTPError
      print(APIKeyRemaining(e), "remaining credits")
    elif e.code == 401:
      e.msg= "key error"
      raise HTTPError
    elif e.code == 429:
      e.msg= "API limit reached"
      raise HTTPError
    elif e.code == 500:
      e.msg= "Internal server error"
      raise HTTPError
      print(APIKeyRemaining(e), "remaining credits")
    elif e.code == 501:
      e.msg = "Vehicle error"
      raise HTTPError
      print(APIKeyRemaining(e), "remaining credits")


def APIKeyRemaining(error):
  header = str(error.headers).replace("\n", " ").split(" ")
  print(header)
  indice = header.index("X-RateLimit-Remaining:")
  return header[indice+1]