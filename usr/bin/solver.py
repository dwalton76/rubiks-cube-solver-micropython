from rubikscubesolvermicropython.cube import RubiksCube333

import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)22s %(levelname)8s: %(message)s')
log = logging.getLogger(__name__)


# 3x3x3
#    default='RRBBUFBFBRLRRRFRDDURUBFBBRFLUDUDFLLFFLLLLDFBDDDUUBDLUU')
#    default='UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB') # solved
if len(sys.argv) < 2:
    cube_state = "RRBBUFBFBRLRRRFRDDURUBFBBRFLUDUDFLLFFLLLLDFBDDDUUBDLUU"
    #cube_state = 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB' # solved
else:
    cube_state = sys.argv[1]

cube = RubiksCube333(cube_state, 'URFDLB')
cube.solve()
print("SOLUTION (%d steps): %s" % (len(cube.solution), " ".join(cube.solution)))
