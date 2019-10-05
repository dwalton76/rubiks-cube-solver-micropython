
import time
from rubikscubesolvermicropython.cube import RubiksCube333

cube_state = "RRBBUFBFBRLRRRFRDDURUBFBBRFLUDUDFLLFFLLLLDFBDDDUUBDLUU"
cube = RubiksCube333(cube_state, 'URFDLB')

def solve_cube(count):
    ref_cube = cube
    r = range(count)

    for i in r:
        ref_cube.solve()
        ref_cube.re_init()

def time_it(f, n):
    t0 = time.ticks_us()
    f(n)
    t1 = time.ticks_us()
    dt = time.ticks_diff(t1, t0)
    fmt = "{:5.3f} sec, {:6.3f} usec/solve, {:8.4f} solves/sec"
    print(fmt.format(dt * 1e-6, dt / n, n / dt * 1e3))


time_it(solve_cube, 1000)

# baseline 0.08 solves/sec
