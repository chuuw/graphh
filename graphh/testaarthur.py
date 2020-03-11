from graphh import GraphHopper

gh_client = GraphHopper(api_key="76360ba3-af69-4ba9-8826-e0eaf6794366")
print(gh_client)
print(gh_client.address_to_latlong("Plaine-Haute"))

# la fonction adress_to_latlong nous retourne une posotion en longitude/latitude d'une adresse
# Et nous renvoie une position par default pour une valeur incoreccte => (32.25223965, 35.36075970421772)

latlong_LaMez = gh_client.address_to_latlong("La Meziere")
latlong_Vignoc = gh_client.address_to_latlong("Vignoc")
latlong_Ph = gh_client.address_to_latlong("Plaine-Haute")
latlong_Rennes = gh_client.address_to_latlong("Rennes, Republique")

print(gh_client.distance([latlong_LaMez,latlong_Vignoc], unit = "km"))
print(gh_client.duration([latlong_Ph,latlong_Rennes],unit="h"))
