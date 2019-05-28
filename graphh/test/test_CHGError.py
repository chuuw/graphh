import os
import sys

sys.path.append(os.path.join(".."))

from graphh import CGHError

### TEST check_point
# CGHError.check_point(("a","b")) OK
# CGHError.check_point(("a", 1))) OK
# CGHError.check_point((1, 2, 3)) OK
# CGHError.check_point((1, 2, "c")) OK
# CGHError.check_point((-93, 2)) OK
# CGHError.check_point((-101, 234)) OK
# CGHError.check_point((1, 2)) OK

