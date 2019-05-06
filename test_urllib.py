import urllib.request

url="https://graphhopper.com/api/1/route?point=51.131,12.414&point=48.224,3.867&vehicle=car&locale=de&calc_points=false&key=1620b7ee-90b2-4daa-9ef5-4aba2d279978"


fp=urllib.request.urlopen(url)
contenu=fp.read().decode("utf-8")

print(contenu)




