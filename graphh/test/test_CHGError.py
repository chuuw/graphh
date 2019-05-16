import os
import sys

sys.path.append(os.path.join(".."))

import CGHError

l_points = [("a","b"), ("a", 1), (1, 2, 3), (1, 2, "c"), (-93, 2), (-101, 234),
            (1, 2)]

for point in l_points:
    print(CGHError.valid_point(point))

# j'ai mis en commentaire les sys.exit() dans valid_point dans CGHError
# pour faire les tests parce que sinon le programme se fermait juste
# après la première erreur et donc
# on ne pouvait pas faire plusieurs tests sur le même fichier,
# ce qui n'est pas pratique du tout
# je les ai remis sans commentaires après, même si je ne vois pas trop
# à quoi ils servent du coup

    

