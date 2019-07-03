from rubikscubesolvermicropython.cube import RubiksCube333, print_mem_stats

import logging
import sys

print_mem_stats("Initial")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)22s %(levelname)8s: %(message)s')
log = logging.getLogger(__name__)

print_mem_stats("post logging")

# Solved 3x3x3
# UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB

# If the user did not specify a cube to solve, solve this random one
if len(sys.argv) < 2:
    cube_state = "RRBBUFBFBRLRRRFRDDURUBFBBRFLUDUDFLLFFLLLLDFBDDDUUBDLUU"
else:
    cube_state = sys.argv[1]

cube = RubiksCube333(cube_state, 'URFDLB')
cube.solve()
print("\nSOLUTION (%d steps): %s\n" % (len(cube.solution), " ".join(cube.solution)))
print_mem_stats("Final")
