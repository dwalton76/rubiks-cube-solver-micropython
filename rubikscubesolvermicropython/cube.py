
from micropython import const
from rubikscubesolvermicropython.rotate import *
import utime

U = const(0)
L = const(1)
F = const(2)
R = const(3)
B = const(4)
D = const(5)

side2str = {
    U : "U",
    F : "F",
    D : "D",
    B : "B",
    R : "R",
    L : "L",
}

# This numbering looks a bit odd but this is how the sides were numbered
# in the original NXT solver.  This should only be used in get_step_string().
get_step_string_side2str = {
    0 : "U",
    1 : "F",
    2 : "D",
    3 : "B",
    4 : "R",
    5 : "L",
}

rotate_map = {
    "B": rotate_B,
    "B'": rotate_B_prime,
    "B2": rotate_B2,
    "D": rotate_D,
    "D'": rotate_D_prime,
    "D2": rotate_D2,
    "F": rotate_F,
    "F'": rotate_F_prime,
    "F2": rotate_F2,
    "L": rotate_L,
    "L'": rotate_L_prime,
    "L2": rotate_L2,
    "R": rotate_R,
    "R'": rotate_R_prime,
    "R2": rotate_R2,
    "U": rotate_U,
    "U'": rotate_U_prime,
    "U2": rotate_U2,
    "x": rotate_x,
    "x'": rotate_x_prime,
    "x2": rotate_x2,
    "y": rotate_y,
    "y'": rotate_y_prime,
    "y2": rotate_y2,
    "z": rotate_z,
    "z'": rotate_z_prime,
    "z2": rotate_z2
}

cube_layout = """
          00 01 02
          03 04 05
          06 07 08

09 10 11  18 19 20  27 28 29  36 37 38
12 13 14  21 22 23  30 31 32  39 40 41
15 16 17  24 25 26  33 34 35  42 43 44

          45 46 47
          48 49 50
          51 52 53
"""


# There are 24 combinations to try in terms of which colors
# are on side U and side F
rotations_24 = (
    (const(0), ()),
    (const(1), ("y",)),
    (const(1), ("y'",)),
    (const(2), ("y", "y")),
    (const(2), ("x", "x")),
    (const(3), ("x", "x", "y")),
    (const(3), ("x", "x", "y'")),
    (const(4), ("x", "x", "y", "y")),
    (const(2), ("y'", "x")),
    (const(3), ("y'", "x", "y")),
    (const(3), ("y'", "x", "y'")),
    (const(4), ("y'", "x", "y", "y")),
    (const(1), ("x",)),
    (const(2), ("x", "y")),
    (const(2), ("x", "y'")),
    (const(3), ("x", "y", "y")),
    (const(2), ("y", "x")),
    (const(3), ("y", "x", "y")),
    (const(3), ("y", "x", "y'")),
    (const(4), ("y", "x", "y", "y")),
    (const(1), ("x'",)),
    (const(2), ("x'", "y")),
    (const(2), ("x'", "y'")),
    (const(3), ("x'", "y", "y")),
)


def print_mem_stats(desc):
    import gc
    print('{} free: {} allocated: {}'.format(desc, gc.mem_free(), gc.mem_alloc()))


profile_stats_time = {}
profile_stats_calls = {}

def timed_function(f, *args, **kwargs):
    myname = str(f).split(' ')[1]

    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)

        if myname not in profile_stats_time:
            profile_stats_time[myname] = 0
            profile_stats_calls[myname] = 0

        profile_stats_time[myname] += utime.ticks_diff(utime.ticks_us(), t)
        profile_stats_calls[myname] += 1

        return result

    return new_func


# @timed_function
def get_lines_in_file(file_data, line_width, line_index, lines_to_get):
    """
    result = []
    start = line_width * line_index
    end = start + (line_width * lines_to_get)
    data = file_data[start:end]

    for line in data.splitlines():
        result.append(int(line, 16))

    return result
    """
    return [int(x, 16) for x in file_data[line_width * line_index : (line_width * line_index) + (line_width * lines_to_get)].splitlines()]


# @timed_function
def cube2str(cube):
    """
    Return a human readable string for `cube`
    """
    result = """
        %s %s %s
        %s %s %s
        %s %s %s

 %s %s %s  %s %s %s  %s %s %s  %s %s %s
 %s %s %s  %s %s %s  %s %s %s  %s %s %s
 %s %s %s  %s %s %s  %s %s %s  %s %s %s

        %s %s %s
        %s %s %s
        %s %s %s
""" % (
    cube[0], cube[1], cube[2], # U row 1
    cube[3], cube[4], cube[5], # U row 2
    cube[6], cube[7], cube[8], # U row 3

    cube[9], cube[10], cube[11],  # L row 1
    cube[18], cube[19], cube[20], # F row 1
    cube[27], cube[28], cube[29], # R row 1
    cube[36], cube[37], cube[38], # B row 1

    cube[12], cube[13], cube[14], # L row 2
    cube[21], cube[22], cube[23], # F row 2
    cube[30], cube[31], cube[32], # R row 2
    cube[39], cube[40], cube[41], # B row 2

    cube[15], cube[16], cube[17], # L row 3
    cube[24], cube[25], cube[26], # F row 3
    cube[33], cube[34], cube[35], # R row 3
    cube[42], cube[43], cube[44], # B row 3

    cube[45], cube[46], cube[47], # D row 1
    cube[48], cube[49], cube[50], # D row 2
    cube[51], cube[52], cube[53]  # D row 3
    )

    for (side_number, side_name) in side2str.items():
        result = result.replace(str(side_number), side_name)

    return result


# @timed_function
def cube2strcolor(cube):
    """
    Add color to the `cube` string
    """
    cube_string = cube2str(cube)
    cube_string = cube_string.replace("U", "\033[97mU\033[0m") # White
    cube_string = cube_string.replace("L", "\033[90mL\033[0m") # Orange
    cube_string = cube_string.replace("F", "\033[92mF\033[0m") # Green
    cube_string = cube_string.replace("R", "\033[91mR\033[0m") # Red
    cube_string = cube_string.replace("B", "\033[94mB\033[0m") # Blue
    cube_string = cube_string.replace("D", "\033[93mD\033[0m") # Yellow
    return cube_string


# @timed_function
def get_alg_cubing_net_url(solution):
    """
    Return an alg.cubing.net URL for `solution`
    """
    url = "https://alg.cubing.net/?puzzle=3x3x3&alg="

    for x in solution:
        if x.startswith('COMMENT'):
            url += r'''%2F%2F''' + x.replace("COMMENT", "") + "%0A%0A"
        else:
            url += x + "_"

    url += "&type=alg"
    url += "&title=SpikeCuber"
    url = url.replace("'", "-")
    url = url.replace(" ", "_")
    return url


CORNER_TUPLES = (
    (0, 29, 2, 36), (1, 36, 29, 2), (2, 2, 36, 29), # UBR
    (3, 38, 0, 9), (4, 9, 38, 0), (5, 0, 9, 38), # ULB
    (6, 11, 6, 18), (7, 18, 11, 6), (8, 6, 18, 11), # UFL
    (9, 20, 8, 27), (10, 27, 20, 8), (11, 8, 27, 20), # URF
    (12, 24, 45, 17), (13, 17, 24, 45), (14, 45, 17, 24), # DLF
    (15, 15, 51, 44), (16, 44, 15, 51), (17, 51, 44, 15), # DBL
    (18, 42, 53, 35), (19, 35, 42, 53), (20, 53, 35, 42), # DRB
    (21, 33, 47, 26), (22, 26, 33, 47), (23, 47, 26, 33), # DFR
)


EDGE_TUPLES = (
    (0, 37, 1), (1, 1, 37), # UB
    (2, 10, 3), (3, 3, 10), # UL
    (4, 19, 7), (5, 7, 19), # UF
    (6, 28, 5), (7, 5, 28), # UR
    (8, 21, 14), (9, 14, 21), # LF
    (10, 12, 41), (11, 41, 12), # BL
    (12, 16, 48), (13, 48, 16), # DL
    (14, 39, 32), (15, 32, 39), # RB
    (16, 43, 52), (17, 52, 43), # DB
    (18, 30, 23), (19, 23, 30), # FR
    (20, 34, 50), (21, 50, 34), # DR
    (22, 25, 46), (23, 46, 25), # DF
)


def RFIX(RR):
    """
    Normalize to range -1 to 2
    """
    return ((int(RR) + 1) & 3) - 1


# @timed_function
def get_step_string(f, r):
    """
    Give the face `f` and rotation `r`, return the string equivalent such as U, U', U2, etc
    """
    r &= 3

    # r is 1/4 forward, 1/4 backward or 1/2 turn
    if r == 1:
        return get_step_string_side2str[f]
    elif r == 2:
        return "{}2".format(get_step_string_side2str[f])
    elif r == 3:
        return "{}'".format(get_step_string_side2str[f])
    else:
        raise Exception("rotate r '%s' is invalid" % r)


FULL_CUBE_ROTATES = set(("x", "x'", "x2", "y", "y'", "y2", "z", "z'", "z2"))

# @timed_function
def get_solution_len_minus_rotates(solution):
    """
    Return the length of `solution` ignoring comments and whole cube rotations
    """
    ref_FULL_CUBE_ROTATES = FULL_CUBE_ROTATES
    count = 0

    for step in solution:

        if step.startswith("COMMENT"):
            continue

        if step in ref_FULL_CUBE_ROTATES:
            continue

        count += 1

    return count


# @timed_function
def apply_rotations(size, step, rotations):
    """
    Apply the `rotations` to `step` and return the `step`. This is used by
    compress_solution() to remove all of the whole cube rotations from
    the solution.
    """

    if step.startswith("COMMENT"):
        return step

    for rotation in rotations:
        # remove the number at the start of the rotation...for a 4x4x4 cube
        # there might be a 4U rotation (to rotate about the y-axis) but we
        # don't need to keep the '4' part.
        rotation = rotation[1:]

        if rotation == "U" or rotation == "D'":
            if "U" in step:
                pass
            elif "L" in step:
                step = step.replace("L", "F")
            elif "F" in step:
                step = step.replace("F", "R")
            elif "R" in step:
                step = step.replace("R", "B")
            elif "B" in step:
                step = step.replace("B", "L")
            elif "D" in step:
                pass

        elif rotation == "U'" or rotation == "D":
            if "U" in step:
                pass
            elif "L" in step:
                step = step.replace("L", "B")
            elif "F" in step:
                step = step.replace("F", "L")
            elif "R" in step:
                step = step.replace("R", "F")
            elif "B" in step:
                step = step.replace("B", "R")
            elif "D" in step:
                pass

        elif rotation == "F" or rotation == "B'":
            if "U" in step:
                step = step.replace("U", "L")
            elif "L" in step:
                step = step.replace("L", "D")
            elif "F" in step:
                pass
            elif "R" in step:
                step = step.replace("R", "U")
            elif "B" in step:
                pass
            elif "D" in step:
                step = step.replace("D", "R")

        elif rotation == "F'" or rotation == "B":
            if "U" in step:
                step = step.replace("U", "R")
            elif "L" in step:
                step = step.replace("L", "U")
            elif "F" in step:
                pass
            elif "R" in step:
                step = step.replace("R", "D")
            elif "B" in step:
                pass
            elif "D" in step:
                step = step.replace("D", "L")

        elif rotation == "R" or rotation == "L'":
            if "U" in step:
                step = step.replace("U", "F")
            elif "L" in step:
                pass
            elif "F" in step:
                step = step.replace("F", "D")
            elif "R" in step:
                pass
            elif "B" in step:
                step = step.replace("B", "U")
            elif "D" in step:
                step = step.replace("D", "B")

        elif rotation == "R'" or rotation == "L":
            if "U" in step:
                step = step.replace("U", "B")
            elif "L" in step:
                pass
            elif "F" in step:
                step = step.replace("F", "U")
            elif "R" in step:
                pass
            elif "B" in step:
                step = step.replace("B", "D")
            elif "D" in step:
                step = step.replace("D", "F")

        else:
            raise Exception("%s is an invalid rotation" % rotation)

    return step


# @timed_function
def compress_solution(solution):
    """
    Remove the whole cube rotations from `solution`
    """
    result = []
    rotations = []
    tmp_solution = []

    for step in solution:
        if step == "x":
            tmp_solution.append("3R")
        elif step == "x'":
            tmp_solution.append("3R'")
        elif step == "x2":
            tmp_solution.append("3R")
            tmp_solution.append("3R")

        elif step == "y":
            tmp_solution.append("3U")
        elif step == "y'":
            tmp_solution.append("3U'")
        elif step == "y2":
            tmp_solution.append("3U")
            tmp_solution.append("3U")

        elif step == "z":
            tmp_solution.append("3F")
        elif step == "z'":
            tmp_solution.append("3F'")
        elif step == "z2":
            tmp_solution.append("3F")
            tmp_solution.append("3F")

        else:
            tmp_solution.append(step)

    for step in tmp_solution:
        if step[0] == "3":
            rotations.append(apply_rotations(3, step, rotations))
        else:
            result.append(apply_rotations(3, step, rotations))

    return result


class RubiksCube333(object):
    """
    A class for solving a 3x3x3 Rubiks Cube
    """

    def __init__(self, state, order):
        SQUARES_PER_SIDE = 9
        self.FACELET_COUNT = SQUARES_PER_SIDE * 6

        self.solution = []
        self.state = []
        state = list(state)

        if order == 'URFDLB':
            self.state.extend(state[0:SQUARES_PER_SIDE])                            # U
            self.state.extend(state[(SQUARES_PER_SIDE * 4):(SQUARES_PER_SIDE * 5)]) # L
            self.state.extend(state[(SQUARES_PER_SIDE * 2):(SQUARES_PER_SIDE * 3)]) # F
            self.state.extend(state[(SQUARES_PER_SIDE * 1):(SQUARES_PER_SIDE * 2)]) # R
            self.state.extend(state[(SQUARES_PER_SIDE * 5):(SQUARES_PER_SIDE * 6)]) # B
            self.state.extend(state[(SQUARES_PER_SIDE * 3):(SQUARES_PER_SIDE * 4)]) # D
        elif order == 'ULFRBD':
            self.state.extend(state[0:SQUARES_PER_SIDE])                            # U
            self.state.extend(state[(SQUARES_PER_SIDE * 1):(SQUARES_PER_SIDE * 2)]) # L
            self.state.extend(state[(SQUARES_PER_SIDE * 2):(SQUARES_PER_SIDE * 3)]) # F
            self.state.extend(state[(SQUARES_PER_SIDE * 3):(SQUARES_PER_SIDE * 4)]) # R
            self.state.extend(state[(SQUARES_PER_SIDE * 4):(SQUARES_PER_SIDE * 5)]) # B
            self.state.extend(state[(SQUARES_PER_SIDE * 5):(SQUARES_PER_SIDE * 6)]) # D
        else:
            raise Exception("Add support for order %s" % order)

        for x in range(self.FACELET_COUNT):
            if self.state[x] == "U":
                self.state[x] = 0
            elif self.state[x] == "L":
                self.state[x] = 1
            elif self.state[x] == "F":
                self.state[x] = 2
            elif self.state[x] == "R":
                self.state[x] = 3
            elif self.state[x] == "B":
                self.state[x] = 4
            elif self.state[x] == "D":
                self.state[x] = 5

        self.state = bytearray(self.state)
        self.state_scratchpad = bytearray(self.FACELET_COUNT)
        self.state_backup = bytearray(self.FACELET_COUNT)

        self.state_scratchpad[:] = self.state
        self.state_backup[:] = self.state

        #self.state_scratchpad = self.state[:]
        #self.state_backup = self.state[:]
        self.index_init_all()

    # @timed_function
    def re_init(self):
        self.solution = []
        self.state = self.state_backup[:]

    # @timed_function
    def load_tables(self):

        # Get the directory where cube.py was installed...example:
        # /usr/lib/micropython/rubikscubesolvermicropython/cube.py
        directory = "/".join(__file__.split("/")[:-1]) + "/"

        with open(directory + "mtd0.txt", "r") as fh:
            self.mtd0 = fh.read()

        with open(directory + "mtd1.txt", "r") as fh:
            self.mtd1 = fh.read()

        with open(directory + "mtd2.txt", "r") as fh:
            self.mtd2 = fh.read()

        with open(directory + "mtd3.txt", "r") as fh:
            self.mtd3 = fh.read()

        with open(directory + "mtd4.txt", "r") as fh:
            self.mtd4 = fh.read()

        with open(directory + "mtd5.txt", "r") as fh:
            self.mtd5 = fh.read()

        with open(directory + "mtd6.txt", "r") as fh:
            self.mtd6 = fh.read()

        with open(directory + "mtd7.txt", "r") as fh:
            self.mtd7 = fh.read()

        with open(directory + "mtd8.txt", "r") as fh:
            self.mtd8 = fh.read()

        # We should be able to drop in different phases/tables in the future
        self.phases = (
            (const(0), "two edges", (), ((D, F), (D, R)),                           const(3), self.mtd0, const(527), const(5)),
            (const(1), "one corner, one edge", ((D, F, R),), ((F, R),),             const(4), self.mtd1, const(479), const(7)),
            (const(2), "one edge", (), ((D, B),),                                   const(3), self.mtd2, const(17),  const(5)),
            (const(3), "one corner, one edge", ((D, R, B),), ((R, B),),             const(5), self.mtd3, const(335), const(9)),
            (const(4), "one edge", (), ((D, L),),                                   const(3), self.mtd4, const(13),  const(5)),
            (const(5), "one corner, one edge", ((D, B, L),), ((B, L),),             const(5), self.mtd5, const(215), const(9)),
            (const(6), "one corner, one edge", ((D, L, F),), ((L, F),),             const(5), self.mtd6, const(149), const(9)),
            (const(7), "last three corners", ((U, R, F), (U, F, L), (U, L, B)), (), const(7), self.mtd7, const(647), const(13)),
            (const(8), "last three edges", (), ((U, R), (U, F), (U, L)),            const(8), self.mtd8, const(95),  const(15)),
        )

    # @timed_function
    def get_kociemba_string(self):
        """
        Return the cube state as a kociemba string
        """
        kociemba_sequence = (
            0, 1, 2, 3, 4, 5, 6, 7, 8, # U
            27, 28, 29, 30, 31, 32, 33, 34, 35, # R
            18, 19, 20, 21, 22, 23, 24, 25, 26, # F
            45, 46, 47, 48, 49, 50, 51, 52, 53, # D
            9, 10, 11, 12, 13, 14, 15, 16, 17, # L
            36, 37, 38, 39, 40, 41, 42, 43, 44, # B
        )
        result = []
        for x in kociemba_sequence:
            result.append(side2str[self.state[x]])
        return "".join(result)

    # @timed_function
    def rotate(self, step):
        """
        Apply `step` to the cube and append `step` to our solution list
        """

        # On a laptop the following list comp is the fastest way to do the rotate. This involves
        # allocating memory for the new list everytime though.  That malloc is about 600x slower
        # on Spike than it is on my laptop.
        #
        # self.state = [ref_state[x] for x in ref_swaps_333[step]]

        # So what we do instead is use a scratchpad bytearray to do the rotate without
        # any mallocs
        rotate_function = rotate_map.get(step)
        rotate_function(self.state, self.state_scratchpad)

        self.solution.append(step)

    # @timed_function
    def rotate_side_X_to_Y(self, x, y):
        """
        Rotate the entire cube so that side `x` is on side `y`
        """

        if y == "U":
            pos_to_check = 4
        elif y == "L":
            pos_to_check = 13
        elif y == "F":
            pos_to_check = 22
        elif y == "R":
            pos_to_check = 31
        elif y == "B":
            pos_to_check = 40
        elif y == "D":
            pos_to_check = 49

        F_pos_to_check = 22
        D_pos_to_check = 49

        while self.state[pos_to_check] != x:

            if self.state[F_pos_to_check] == x and y == "U":
                self.rotate("x")

            elif self.state[F_pos_to_check] == x and y == "D":
                self.rotate("x'")

            elif self.state[D_pos_to_check] == x and y == "F":
                self.rotate("x")

            elif self.state[D_pos_to_check] == x and y == "U":
                self.rotate("x")
                self.rotate("x")

            else:
                self.rotate("y")

    # @timed_function
    def rotate_U_to_U(self):
        """
        Rotate side U to the top
        """
        self.rotate_side_X_to_Y(U, "U")

    # @timed_function
    def rotate_F_to_F(self):
        """
        Rotate side F to the front
        """
        self.rotate_side_X_to_Y(F, "F")

    # @timed_function
    def recolor(self, recolor_map):
        """
        Recolor the squares of the cube per `recolor_map`
        """
        ref_state = self.state
        r = range(self.FACELET_COUNT)
        for x in r:
            ref_state[x] = recolor_map[ref_state[x]]

    # @timed_function
    def index_init_all(self):
        """
        Initialize all indexes. This is called at the start of the solve for a cube.
        """
        NPIECE = 3
        self.idx_idx = [None] * NPIECE
        self.idx_nc = 0
        self.idx_ne = 0
        self.idx = 0
        self.idx_ic = 24
        self.idx_ie = 24

    # @timed_function
    def index_init(self):
        """
        Initialize indexes. This is called at the start of each phase for solving a cube.
        """
        self.idx_nc = 0
        self.idx_ne = 0
        self.idx = 0

    # @timed_function
    def index_last(self):
        """
        Initialize indexes for the last phase
        """
        self.idx = ((self.idx >> 2) <<1 ) | (self.idx & 1);

    # @timed_function
    def index_corner(self, f0, f1, f2):
        """
        Set idx, idx_ic and idx_nc for corner `f0/f1/f2`
        """
        ref_CORNER_TUPLES = CORNER_TUPLES
        ref_state = self.state

        for (ic, corner0, corner1, corner2) in ref_CORNER_TUPLES:
            if ref_state[corner0] == f0 and ref_state[corner1] == f1 and ref_state[corner2] == f2:
                break
        else:
            raise Exception("Could not find corner f0/f1/f2 %s/%s/%s in\n%s\n" % (f0, f1, f2, cube2str(self.state)))

        ref_idx_ic = self.idx_ic
        ref_idx_nc = self.idx_nc
        ref_idx_idx = self.idx_idx
        ref_idx = self.idx
        r = range(ref_idx_nc)

        for i in r:
            if ic > ref_idx_idx[i]:
                ic -= 3

        self.idx = (ref_idx * ref_idx_ic) + ic
        self.idx_idx[ref_idx_nc] = ic
        self.idx_nc += 1
        self.idx_ic -= 3

    # @timed_function
    def index_edge(self, f0, f1):
        """
        Set idx, idx_ie and idx_ne for edge `f0/f1`
        """
        ref_EDGE_TUPLES = EDGE_TUPLES
        ref_state = self.state

        for (ie, edge0, edge1) in ref_EDGE_TUPLES:
            if ref_state[edge0] == f0 and ref_state[edge1] == f1:
                break
        else:
            raise Exception("Could not find edge f0/f1 %s/%s\n%s" % (f0, f1, cube2str(ref_state)))

        ref_idx_ie = self.idx_ie
        ref_idx_ne = self.idx_ne
        ref_idx_idx = self.idx_idx
        ref_idx = self.idx
        r = range(ref_idx_ne)

        for i in r:
            if ie > ref_idx_idx[i]:
                ie -= 2

        self.idx = (ref_idx * ref_idx_ie) + ie
        self.idx_idx[ref_idx_ne] = ie
        self.idx_ne += 1
        self.idx_ie -= 2

    # @timed_function
    def verify_solution(self, original_state, solution):
        """
        Put the cube back in the original state and apply `solution` to verify
        that the cube is indeed solved.  This should always be the case but this
        gives a nice way to catch weird bugs.
        """
        self.solution = []
        self.state = original_state

        for step in solution:
            self.rotate(step)

        kociemba_string = self.get_kociemba_string()

        if kociemba_string != "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB":
            print("ERROR: cube should be solved but it is not solved, %s" % kociemba_string)
            print(cube2strcolor(self.state))
            import sys
            sys.exit(0)

    # @timed_function
    def solve_phase(self, phase, desc, mtb, mtd, sz, mvm):
        """
        Solve a single phase per the `mtd` table
        `sz` is how many 'mtb' long move sequenes there are in the mtd file
        """
        self.idx = sz - self.idx
        idx = self.idx

        if idx > 0:
            ref_get_lines_in_file = get_lines_in_file
            ref_get_step_string_side2str = get_step_string_side2str
            # ref_RFIX = RFIX
            # ref_get_step_string = get_step_string
            #ref_rotate = self.rotate
            ref_rotate_map = rotate_map
            ref_state = self.state
            ref_state_scratchpad = self.state_scratchpad
            ref_solution = self.solution

            LINE_WIDTH = const(5)
            #mvm = (mtb * 2) - 1
            # print("\nphase %d %s: mtb %d, mtd %s, mvm %d, sz %d, idx %d" % (phase, desc, mtb, mtd, mvm, sz, self.idx))

            i = (idx - 1) * mtb
            orig_i = i

            # unrolled this to avoid a function call
            #steps = ref_get_lines_in_file(mtd, LINE_WIDTH, i, mvm)
            steps = [int(x, 16) for x in mtd[LINE_WIDTH * i : (LINE_WIDTH * i) + (LINE_WIDTH * mvm)].splitlines()]

            b = steps[0]
            i += 1

            if b != 0xFF:
                mv = 0
                f0 = int(b / 3)

                # unrolled this to avoid a function call
                # r0 = ref_RFIX(b - (f0 * 3) + 1)
                r0 = ((b - (f0 * 3) + 2) & 3) - 1

                # unrolled this to avoid a function call
                # step = ref_get_step_string(f0, r0)
                r0 &= 3

                # r is 1/4 forward, 1/4 backward or 1/2 turn
                if r0 == 1:
                    step = ref_get_step_string_side2str[f0]
                elif r0 == 2:
                    step = "{}2".format(ref_get_step_string_side2str[f0])
                elif r0 == 3:
                    step = "{}'".format(ref_get_step_string_side2str[f0])
                else:
                    raise Exception("rotate r0 '%s' is invalid" % r0)

                # unrolled this to avoid a function call
                #ref_rotate(step)
                rotate_function = ref_rotate_map.get(step)
                rotate_function(ref_state, ref_state_scratchpad)
                ref_solution.append(step)

                mv += 1

                while mv < mvm:
                    b >>= 4

                    if (mv & 1) != 0:
                        b = steps[i - orig_i]
                        i += 1

                    b0 = b & 0xF

                    if b0 == 0xF:
                        break

                    f1 = int(b0 / 3)

                    # unrolled this to avoid a function call
                    # r0 = ref_RFIX(b0 - (f1 * 3) + 1)
                    r0 = ((b0 - (f1 * 3) + 2) & 3) - 1

                    if f1 >= f0:
                        f1 += 1

                    f0 = f1

                    # unrolled this to avoid a function call
                    #step = ref_get_step_string(f0, r0)
                    r0 &= 3

                    # r is 1/4 forward, 1/4 backward or 1/2 turn
                    if r0 == 1:
                        step = ref_get_step_string_side2str[f0]
                    elif r0 == 2:
                        step = "{}2".format(ref_get_step_string_side2str[f0])
                    elif r0 == 3:
                        step = "{}'".format(ref_get_step_string_side2str[f0])
                    else:
                        raise Exception("rotate r0 '%s' is invalid" % r0)

                    # unrolled this to avoid a function call
                    #ref_rotate(step)
                    rotate_function = ref_rotate_map.get(step)
                    rotate_function(ref_state, ref_state_scratchpad)
                    ref_solution.append(step)
                    mv += 1

    def _solve(self, original_state, original_solution, rotations_to_try, phases_to_solve):
        ref_rotate = self.rotate
        ref_recolor = self.recolor
        ref_phases = self.phases
        ref_index_init_all = self.index_init_all
        ref_index_corner = self.index_corner
        ref_index_edge = self.index_edge
        ref_index_last = self.index_last
        ref_solve_phase = self.solve_phase
        ref_rotations_24 = rotations_24

        min_solution = None
        min_solution_len = 999
        min_rotations = None
        min_rotation_count = None

        last_phase = const(8)

        # Try all 'rotations_to_try', find the one with the shortest solution
        for (rotation_count, rotations) in rotations_to_try:
            self.state = original_state[:]
            self.solution = original_solution[:]

            for step in rotations:
                ref_rotate(step)

            solution_len = len(self.solution)
            prev_solution_len = solution_len
            ref_state = self.state

            recolor_map = {
                ref_state[4] : U,
                ref_state[13] : L,
                ref_state[22] : F,
                ref_state[31] : R,
                ref_state[40] : B,
                ref_state[49] : D,
            }

            ref_recolor(recolor_map)
            ref_index_init_all()

            for (phase, desc, corners, edges, mtb, mtd, sz, mvm) in ref_phases[0:phases_to_solve]:

                # unrolled this to avoid a function call
                # ref_index_init()
                self.idx_nc = 0
                self.idx_ne = 0
                self.idx = 0

                for corner in corners:
                    ref_index_corner(*corner)

                for edge in edges:
                    ref_index_edge(*edge)

                if phase == last_phase:
                    ref_index_last()

                ref_solve_phase(phase, desc, mtb, mtd, sz, mvm)
                solution_len = len(self.solution)
                self.solution.append("COMMENT phase %s: %s (%d steps)" % (
                    phase, desc, (solution_len - prev_solution_len)))
                prev_solution_len = solution_len

            # There will be one COMMENT per phase
            solution_len = len(self.solution)
            solution_len -= rotation_count + phases_to_solve

            if solution_len < min_solution_len:
                min_solution_len = solution_len
                min_solution = self.solution[:]
                min_rotations = rotations
                min_rotation_count = rotation_count
                print("(NEW MIN) rotations %s, solution len %d" % (" ".join(rotations), solution_len))
            else:
                print("rotations %s, solution len %d" % (" ".join(rotations), solution_len))

        return ((min_rotation_count, min_rotations), min_solution)

    # @timed_function
    def solve(self):
        """
        Solve the cube and return the solution
        """
        print("INIT CUBE:\n%s" % (cube2strcolor(self.state)))
        self.rotate_U_to_U()
        self.rotate_F_to_F()

        original_state = self.state[:]
        original_solution = self.solution [:]

        # Find the rotation that has the lowest move count for the first 3 phases
        (best_rotation, min_solution) = self._solve(original_state, original_solution, rotations_24, 3)

        # Use that rotation to solve the entire cube
        (_, min_solution) = self._solve(original_state, original_solution, (best_rotation, ), 9)

        self.solution = compress_solution(min_solution)

        print("FINAL CUBE:\n%s" % (cube2strcolor(self.state)))
        print(get_alg_cubing_net_url(self.solution))

        # Remove the comments from the solution
        self.solution = [x for x in self.solution if not x.startswith("COMMENT")]

        self.verify_solution(original_state, self.solution)

        return self.solution

    def print_profile_data(self):
        print("                     function      calls  time(ms)")
        print("==============================  ========  ========")
        for function in profile_stats_calls.keys():
            print("{:>30}  {:>8}  {:>8.2f}".format(function, profile_stats_calls[function], profile_stats_time[function] / 1000))
