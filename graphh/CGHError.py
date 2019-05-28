from urllib.error import HTTPError
import urllib.request
import sys
import json


def valid_point(point):  # point = (lat, long)
  try:
   for coordinate in point: 
     float(coordinate)
  except ValueError:
    print("Error: coordinates are not valid")
    sys.exit()
    return False
  else: 
    if not len(point)==2:
      print("Error: point need to be lat and long")
      sys.exit()
      return False
    elif not (-90 <= point[0] <= 90 and -180 <= point[1] <= 180) :
      print("Error: latitude or longitude value is not valid")
      sys.exit()
      return False
  return True

def valid_vehicle(vehicle):
  l_vehicle = [
      "car", "small_truck", "truck",
      "scooter", "foot", "hike",
      "bike", "mtb", "racingbike"
      ]
  if vehicle in l_vehicle:
    return True
  else:
    print("Error: wrong vehicle")
    sys.exit()

def valid_locale(locale):
  l_locale = ["en", "fr", "de", "it"]
  if locale in l_locale:
    return True
  else:
    print("Error: wrong language")
    sys.exit()

def CGHError(error):

    if error.code == 400:
      e.msg = "Argument not correct"
      print(APIKeyRemaining(e), "remaining credits")
    elif e.code == 401:
      e.msg = "Key error"
    elif e.code == 429:
      e.msg = "API limit reached"
    elif e.code == 500:
      e.msg = "Internal server error"
      print(APIKeyRemaining(e), "remaining credits")
    elif e.code == 501:
      e.msg = "vehicle error"
      print(APIKeyRemaining(e), "remaining credits")
  return True


def APIKeyRemaining(error):
  header = str(error.headers).replace("\n", " ").split(" ")
  print(header)
  indice = header.index("X-RateLimit-Remaining:")
  return header[indice+1]
