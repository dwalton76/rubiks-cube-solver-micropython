from rubikscubesolvermicropython.cube import RubiksCube333

import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)22s %(levelname)8s: %(message)s')
log = logging.getLogger(__name__)

# Solved 3x3x3
# UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB

# If the user did not specify a cube to solve, solve this random one
if len(sys.argv) < 2:
    cube_state = "UFRUUDRLFLBUFRUDLBDFUFFDBBBRRRDDBFLDLBFDLRLRUFUBRBLLUD"
elif len(sys.argv) == 2:
    cube_state = sys.argv[1]
else:
    print("Invalid syntax\n\n    micropython ./usr/bin/solver.py STATE\n")
    sys.exit(1)

print(cube_state)
cube = RubiksCube333(cube_state, 'URFDLB')
cube.solve()
print("\nSOLUTION (%d steps): %s\n" % (len(cube.solution), " ".join(cube.solution)))
