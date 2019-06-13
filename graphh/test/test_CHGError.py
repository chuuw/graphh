import os
import sys
import json

sys.path.append(os.path.join(".."))

from graphh import CGHError
from graphh import CGH

# TEST check_point
# CGHError.check_point(("a","b")) OK
# CGHError.check_point(("a", 1))) OK
# CGHError.check_point((1, 2, 3)) OK
# CGHError.check_point((1, 2, "c")) OK
# CGHError.check_point((-93, 2)) OK
# CGHError.check_point((-101, 234)) OK
# CGHError.check_point((1, 2)) OK

# TEST check_vehicle
# CGHError.check_vehicle("banane") OK
# CGHError.check_vehicle(12) OK
# CGHError.check_vehicle("carr") OK
# CGHError.check_vehicle("small_truck") OK

# TEST check_locale
# CGHError.check_locale("chocolat") OK
# CGHError.check_locale(123) OK
# CGHError.check_locale((1,2)) OK
# CGHError.check_locale("enn") OK
# CGHError.check_locale("it") OK

# """test wrong api access key"""
point1 = (48.121410, -1.703526)
point2 = (48.114858, -1.680012)
G1 = CGH.GraphHopper("d37dcab2-7f16-4342-b40e-845c3d004c55")
print(G1.route(point1,point1, locale="fr&points_encoded=false&elevation=true"))


