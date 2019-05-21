from urllib.error import HTTPError
import urllib.request
import sys
import json

def valid_point(point): # point = (lat, long)
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

def CGHError(url):
  try:
    fp=urllib.request.urlopen(url)
    contenu=json.load(fp)
  except HTTPError as e:
    if e.code == 400:
      print("Error: argument not correct")
      print(APIKeyRemaining(e), "remaining credits")
    elif e.code == 401:
      print("Error: key error")
    elif e.code == 429:
      print("Error: API limit reached")
    elif e.code == 500:
      print("Error: Internal server error")
      print(APIKeyRemaining(e), "remaining credits")
    elif e.code == 501:
      print("Error: Vehicle error")
      print(APIKeyRemaining(e), "remaining credits")
    sys.exit()
  return True

def APIKeyRemaining(error):
  header = str(error.headers).replace("\n", " ").split(" ")
  print(header)
  indice = header.index("X-RateLimit-Remaining:")
  return header[indice+1]
