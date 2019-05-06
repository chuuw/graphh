import urllib.request
import json

fp1 = open("credentials.json", "r" , encoding = "utf-8")
dossiercle = json.load(fp1)
key_access = dossiercle["graphhopper"]

urldebase =  "https://graphhopper.com/api/1/"


point = "point=48.224,3.867&point=51.131,12.414"

cle = "&key=" + key_access

url0 = urldebase + "matrix?" + "point=49.932707,11.588051" + "&point=50.241935,10.747375" + "&point=50.118817,11.983337"+ "&vehicle=car" + "&out_array=distances" + "&out_array=times" + cle

url1 = urldebase + "route?" + point + "&vehicle=car" + "&locale=fr" + "&calc_points=false" + cle

url3 = urldebase + "route?" + point + "&vehicle=car" + "&locale=fr" + "&details=max_speed+road_class" + cle

url4 = urldebase + "route?" + point + "&vehicle=car&points_encoded=false" + cle

url5 = urldebase + "geocode?" + "q=Place+Recteur+Henri+le+Moal+35043+Rennes" + "&locale=fr" + "&limit=1" + cle


url2 = urldebase = "route/info?" + cle

fp = urllib.request.urlopen(url0)
dico = json.load(fp)
print(dico)