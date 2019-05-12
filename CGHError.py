from urllib.error import HTTPError
import urllib.request

def pointerror(point):
  try:
   for coordinate in point: 
     float(coordinate)
  except ValueError:
    print("coordinate are not valid")
    return False
  else: 
    if not len(point)==2:
      print("point need be lat and long")
      return False
  return True

def CGHError(url):
  try:
    fp=urllib.request.urlopen(url)
    contenu=fp.read().decode("utf-8")
  except HTTPError as e:
    if e.code == 400:
      print("request is not correct")
      return False
    elif e.code == 401:
      print("key error")
      return False
    elif e.code == 429:
      print("API limit reached")
      return False
    elif e.code == 500:
      print("Internal server error")
      return False
    elif e.code == 501:
      print("Vehicle error")
      return False
  return True
    
