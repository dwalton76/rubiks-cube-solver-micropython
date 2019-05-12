#!/usr/bin/env python3

from rubikscubesolvermicropython.cube import RubiksCube333

import logging
import datetime as dt
import resource
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)22s %(levelname)8s: %(message)s')
log = logging.getLogger(__name__)

# Color the errors and warnings in red
logging.addLevelName(logging.ERROR, "\033[91m   %s\033[0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName(logging.WARNING, "\033[91m %s\033[0m" % logging.getLevelName(logging.WARNING))


# 3x3x3
#    default='RRBBUFBFBRLRRRFRDDURUBFBBRFLUDUDFLLFFLLLLDFBDDDUUBDLUU')
#    default='UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB') # solved
if len(sys.argv) < 2:
    cube_state = "RRBBUFBFBRLRRRFRDDURUBFBBRFLUDUDFLLFFLLLLDFBDDDUUBDLUU"
else:
    cube_state = sys.argv[1]

start_time = dt.datetime.now()
cube = RubiksCube333(cube_state)
cube.solve()
print("SOLUTION: %s" % " ".join(cube.solution))
end_time = dt.datetime.now()
log.info("Memory : {:,} bytes".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
log.info("Time   : %s" % (end_time - start_time))
