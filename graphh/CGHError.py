def check_point(l_latlong, api):
    if len(list(l_latlong)) < 2 and api != "geocode":
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
    if e.code == 400:
      e.msg= "Invalid argument : " + APIKeyRemaining(e) + " remaining credits"
      raise e
    elif e.code == 401:
      e.msg= "Key error"
      raise e
    elif e.code == 429:
      e.msg= "API limit reached"
      raise e
    elif e.code == 500:
      e.msg= "Internal server error : " + APIKeyRemaining(e) + " remaining credits"
      raise e
    elif e.code == 501:
      e.msg = "Vehicle error : " + APIKeyRemaining(e) + " remaining credits"
      raise e


def APIKeyRemaining(error):
  header = str(error.headers).replace("\n", " ").split(" ")
  indice = header.index("X-RateLimit-Remaining:")
  return header[indice+1]