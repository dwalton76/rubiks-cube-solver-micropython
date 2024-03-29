
"""
The phase1 table for this solver is pretty straightforward. The phase2,
phase3, and phase4 tables are encoded a little differenlty to save space...

This solver was written primarily to run on the lego SPIKE platform
which only has 30M of free disk space. Initially the phase2 table
was 88M, the phase3 table 254M and the phase4 table 64M. Each of these
tables consisted of the full cube state and the steps needed to solve
that state.

- We did not need to store the entire move sequence, we only needed to
know the next move (because that takes us to a new state where we can
just do another lookup).  That alone chopped about 25% off of each table.

- Store the moves as a single character instead of "U'", "U2", etc. See
step_to_char for the mapping.

- The bigger change needed was a more effecient way of storing the cube state.
    - assign each edge state in the table a unique index
    - assign each corner state in the table a unique index
    - main table index is then:
        main_index = (edge_index * corners_count) + corner_index

Now the main table can be a single line of "edges_count * corners_count"
step_to_char characters. This cut the phase2 table down to 1.1M, the phase3
table to 2.7M and the phase4 table to 649K!!!
"""

from rubikscubesolvermicropython.LookupTable import LookupTable

# Get the directory where cube.py was installed...example:
# /usr/lib/micropython/rubikscubesolvermicropython/cube.py
directory = "/".join(__file__.split("/")[:-1]) + "/"

kociemba_sequence = (
    1, 2, 3, 4, 5, 6, 7, 8, 9,  # U
    28, 29, 30, 31, 32, 33, 34, 35, 36,  # R
    19, 20, 21, 22, 23, 24, 25, 26, 27,  # F
    46, 47, 48, 49, 50, 51, 52, 53, 54,  # D
    10, 11, 12, 13, 14, 15, 16, 17, 18,  # L
    37, 38, 39, 40, 41, 42, 43, 44, 45,  # B
)

EDGES = (
    2, 4, 6, 8,  # U
    11, 13, 15, 17,  # L
    20, 22, 24, 26,  # F
    29, 31, 33, 35,  # R
    38, 40, 42, 44,  # B
    47, 49, 51, 53,  # D
)

CORNERS = (
    1, 3, 7, 9,
    10, 12, 16, 18,
    19, 21, 25, 27,
    28, 30, 34, 36,
    37, 39, 43, 45,
    46, 48, 52, 54,
)

FULL_CUBE_ROTATES = set(("x", "x'", "x2", "y", "y'", "y2", "z", "z'", "z2"))

char_to_step = {
    '0' : "",
    '1' : "U",
    '2' : "U'",
    '3' : "U2",
    '4' : "L",
    '5' : "L'",
    '6' : "L2",
    '7' : "F",
    '8' : "F'",
    '9' : "F2",
    'a' : "R",
    'b' : "R'",
    'c' : "R2",
    'd' : "B",
    'e' : "B'",
    'f' : "B2",
    'g' : "D",
    'h' : "D'",
    'i' : "D2",
}


# facelet swaps for 3x3x3 moves
swaps_333 = {
    "B": (0, 30, 33, 36, 4, 5, 6, 7, 8, 9, 3, 11, 12, 2, 14, 15, 1, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 54, 31, 32, 53, 34, 35, 52, 43, 40, 37, 44, 41, 38, 45, 42, 39, 46, 47, 48, 49, 50, 51, 10, 13, 16),
    "B'": (0, 16, 13, 10, 4, 5, 6, 7, 8, 9, 52, 11, 12, 53, 14, 15, 54, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 1, 31, 32, 2, 34, 35, 3, 39, 42, 45, 38, 41, 44, 37, 40, 43, 46, 47, 48, 49, 50, 51, 36, 33, 30),
    "B2": (0, 54, 53, 52, 4, 5, 6, 7, 8, 9, 36, 11, 12, 33, 14, 15, 30, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 16, 31, 32, 13, 34, 35, 10, 45, 44, 43, 42, 41, 40, 39, 38, 37, 46, 47, 48, 49, 50, 51, 3, 2, 1),
    "D": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 43, 44, 45, 19, 20, 21, 22, 23, 24, 16, 17, 18, 28, 29, 30, 31, 32, 33, 25, 26, 27, 37, 38, 39, 40, 41, 42, 34, 35, 36, 52, 49, 46, 53, 50, 47, 54, 51, 48),
    "D'": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 25, 26, 27, 19, 20, 21, 22, 23, 24, 34, 35, 36, 28, 29, 30, 31, 32, 33, 43, 44, 45, 37, 38, 39, 40, 41, 42, 16, 17, 18, 48, 51, 54, 47, 50, 53, 46, 49, 52),
    "D2": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 34, 35, 36, 19, 20, 21, 22, 23, 24, 43, 44, 45, 28, 29, 30, 31, 32, 33, 16, 17, 18, 37, 38, 39, 40, 41, 42, 25, 26, 27, 54, 53, 52, 51, 50, 49, 48, 47, 46),
    "F": (0, 1, 2, 3, 4, 5, 6, 18, 15, 12, 10, 11, 46, 13, 14, 47, 16, 17, 48, 25, 22, 19, 26, 23, 20, 27, 24, 21, 7, 29, 30, 8, 32, 33, 9, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 34, 31, 28, 49, 50, 51, 52, 53, 54),
    "F'": (0, 1, 2, 3, 4, 5, 6, 28, 31, 34, 10, 11, 9, 13, 14, 8, 16, 17, 7, 21, 24, 27, 20, 23, 26, 19, 22, 25, 48, 29, 30, 47, 32, 33, 46, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 12, 15, 18, 49, 50, 51, 52, 53, 54),
    "F2": (0, 1, 2, 3, 4, 5, 6, 48, 47, 46, 10, 11, 34, 13, 14, 31, 16, 17, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 29, 30, 15, 32, 33, 12, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 9, 8, 7, 49, 50, 51, 52, 53, 54),
    "L": (0, 45, 2, 3, 42, 5, 6, 39, 8, 9, 16, 13, 10, 17, 14, 11, 18, 15, 12, 1, 20, 21, 4, 23, 24, 7, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 52, 40, 41, 49, 43, 44, 46, 19, 47, 48, 22, 50, 51, 25, 53, 54),
    "L'": (0, 19, 2, 3, 22, 5, 6, 25, 8, 9, 12, 15, 18, 11, 14, 17, 10, 13, 16, 46, 20, 21, 49, 23, 24, 52, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 7, 40, 41, 4, 43, 44, 1, 45, 47, 48, 42, 50, 51, 39, 53, 54),
    "L2": (0, 46, 2, 3, 49, 5, 6, 52, 8, 9, 18, 17, 16, 15, 14, 13, 12, 11, 10, 45, 20, 21, 42, 23, 24, 39, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 25, 40, 41, 22, 43, 44, 19, 1, 47, 48, 4, 50, 51, 7, 53, 54),
    "R": (0, 1, 2, 21, 4, 5, 24, 7, 8, 27, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 48, 22, 23, 51, 25, 26, 54, 34, 31, 28, 35, 32, 29, 36, 33, 30, 9, 38, 39, 6, 41, 42, 3, 44, 45, 46, 47, 43, 49, 50, 40, 52, 53, 37),
    "R'": (0, 1, 2, 43, 4, 5, 40, 7, 8, 37, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 3, 22, 23, 6, 25, 26, 9, 30, 33, 36, 29, 32, 35, 28, 31, 34, 54, 38, 39, 51, 41, 42, 48, 44, 45, 46, 47, 21, 49, 50, 24, 52, 53, 27),
    "R2": (0, 1, 2, 48, 4, 5, 51, 7, 8, 54, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 43, 22, 23, 40, 25, 26, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 38, 39, 24, 41, 42, 21, 44, 45, 46, 47, 3, 49, 50, 6, 52, 53, 9),
    "U": (0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 19, 20, 21, 13, 14, 15, 16, 17, 18, 28, 29, 30, 22, 23, 24, 25, 26, 27, 37, 38, 39, 31, 32, 33, 34, 35, 36, 10, 11, 12, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54),
    "U'": (0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 37, 38, 39, 13, 14, 15, 16, 17, 18, 10, 11, 12, 22, 23, 24, 25, 26, 27, 19, 20, 21, 31, 32, 33, 34, 35, 36, 28, 29, 30, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54),
    "U2": (0, 9, 8, 7, 6, 5, 4, 3, 2, 1, 28, 29, 30, 13, 14, 15, 16, 17, 18, 37, 38, 39, 22, 23, 24, 25, 26, 27, 10, 11, 12, 31, 32, 33, 34, 35, 36, 19, 20, 21, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54),
    "x": (0, 19, 20, 21, 22, 23, 24, 25, 26, 27, 12, 15, 18, 11, 14, 17, 10, 13, 16, 46, 47, 48, 49, 50, 51, 52, 53, 54, 34, 31, 28, 35, 32, 29, 36, 33, 30, 9, 8, 7, 6, 5, 4, 3, 2, 1, 45, 44, 43, 42, 41, 40, 39, 38, 37),
    "x'": (0, 45, 44, 43, 42, 41, 40, 39, 38, 37, 16, 13, 10, 17, 14, 11, 18, 15, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 30, 33, 36, 29, 32, 35, 28, 31, 34, 54, 53, 52, 51, 50, 49, 48, 47, 46, 19, 20, 21, 22, 23, 24, 25, 26, 27),
    "x2": (0, 46, 47, 48, 49, 50, 51, 52, 53, 54, 18, 17, 16, 15, 14, 13, 12, 11, 10, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    "y": (0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 10, 11, 12, 13, 14, 15, 16, 17, 18, 48, 51, 54, 47, 50, 53, 46, 49, 52),
    "y'": (0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 37, 38, 39, 40, 41, 42, 43, 44, 45, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 52, 49, 46, 53, 50, 47, 54, 51, 48),
    "y2": (0, 9, 8, 7, 6, 5, 4, 3, 2, 1, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 54, 53, 52, 51, 50, 49, 48, 47, 46),
    "z": (0, 16, 13, 10, 17, 14, 11, 18, 15, 12, 52, 49, 46, 53, 50, 47, 54, 51, 48, 25, 22, 19, 26, 23, 20, 27, 24, 21, 7, 4, 1, 8, 5, 2, 9, 6, 3, 39, 42, 45, 38, 41, 44, 37, 40, 43, 34, 31, 28, 35, 32, 29, 36, 33, 30),
    "z'": (0, 30, 33, 36, 29, 32, 35, 28, 31, 34, 3, 6, 9, 2, 5, 8, 1, 4, 7, 21, 24, 27, 20, 23, 26, 19, 22, 25, 48, 51, 54, 47, 50, 53, 46, 49, 52, 43, 40, 37, 44, 41, 38, 45, 42, 39, 12, 15, 18, 11, 14, 17, 10, 13, 16),
    "z2": (0, 54, 53, 52, 51, 50, 49, 48, 47, 46, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 45, 44, 43, 42, 41, 40, 39, 38, 37, 9, 8, 7, 6, 5, 4, 3, 2, 1),
}


def print_mem_stats(desc):
    import gc
    print('{} free: {} allocated: {}'.format(desc, gc.mem_free(), gc.mem_alloc()))


# @timed_function
def cube2str(cube):
    """
    Return a human readable string for `cube`
    """
    return """
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
    cube[1], cube[2], cube[3], # U row 1
    cube[4], cube[5], cube[6], # U row 2
    cube[7], cube[8], cube[9], # U row 3

    cube[10], cube[11], cube[12], # L row 1
    cube[19], cube[20], cube[21], # F row 1
    cube[28], cube[29], cube[30], # R row 1
    cube[37], cube[38], cube[39], # B row 1

    cube[13], cube[14], cube[15], # L row 2
    cube[22], cube[23], cube[24], # F row 2
    cube[31], cube[32], cube[33], # R row 2
    cube[40], cube[41], cube[42], # B row 2

    cube[16], cube[17], cube[18], # L row 3
    cube[25], cube[26], cube[27], # F row 3
    cube[34], cube[35], cube[36], # R row 3
    cube[43], cube[44], cube[45], # B row 3

    cube[46], cube[47], cube[48], # D row 1
    cube[49], cube[50], cube[51], # D row 2
    cube[52], cube[53], cube[54]  # D row 3
    )


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


# @timed_function
def get_solution_len(solution):
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


EDGE_TUPLES = (
    ((2, 38), (38, 2)),
    ((4, 11), (11, 4)),
    ((6, 29), (29, 6)),
    ((8, 20), (20, 8)),
    ((13, 42), (42, 13)),
    ((15, 22), (22, 15)),
    ((31, 24), (24, 31)),
    ((33, 40), (40, 33)),
    ((47, 26), (26, 47)),
    ((49, 17), (17, 49)),
    ((51, 35), (35, 51)),
    ((53, 44), (44, 53)),
)


CORNER_TUPLES = (
    ((1, 10, 39), (39, 1, 10), (10, 39, 1)),
    ((3, 37, 30), (30, 3, 37), (37, 30, 3)),
    ((7, 19, 12), (12, 7, 19), (19, 12, 7)),
    ((9, 28, 21), (21, 9, 28), (28, 21, 9)),
    ((46, 18, 25), (25, 46, 18), (18, 25, 46)),
    ((48, 27, 34), (34, 48, 27), (27, 34, 48)),
    ((52, 45, 16), (16, 52, 45), (45, 16, 52)),
    ((54, 36, 43), (43, 54, 36), (36, 43, 54)),
)

'''
This should average 31 moves

phase 1 - EO the edges
    - make the edges solveable without L L' R R'
    - (2^12)/2 or 2048 states
    - averages 4.61 moves

phase 2 - Remove F F' B B'
    - LB LF RB RF edges must be staged to x-plane
        12!/(8!*4!) is 495
    - Stage the UD corners (color all of the U or D corner squares as U)
        - (3^8)/3 or 2187 states
    - 495 * 2187 is 1,082,565 states
    - averages 7.80 moves

phase 3 - Remove U U' D D'
    move 4 edges to y-plane, this in turn moves the other 4-edges to z-plane
    There must also be some corner manipulation done here
    - 8!/(4!*4!) is 70 for the edges
    - 40,320 for the corners
    - 70 * 40,320 is 2,822,400
    - averages 8.70 moves

phase 4 - solve cube
    - all quarter turns have been removed by this point
    - (4!^3)/2 is 6912 for the edges
    - 4!^2 is 576 for the corners
        it is actually 96 though (I got 96 by building the corners table)
        576/6 is 96...not sure if that means anything

    - 6912 * 96 is 663,552
    - averages 10.13 moves
'''

class LookupTable333Phase1(LookupTable):
    """
    lookup-table-3x3x3-step110.txt
    ==============================
    0 steps has 1 entries (0 percent, 0.00x previous step)
    1 steps has 2 entries (0 percent, 2.00x previous step)
    2 steps has 25 entries (1 percent, 12.50x previous step)
    3 steps has 202 entries (9 percent, 8.08x previous step)
    4 steps has 620 entries (30 percent, 3.07x previous step)
    5 steps has 900 entries (43 percent, 1.45x previous step)
    6 steps has 285 entries (13 percent, 0.32x previous step)
    7 steps has 13 entries (0 percent, 0.05x previous step)

    Total: 2,048 entries
    Average: 4.61 moves
    """

    edge_states = {
        (2, 38): ['UB', 'UL', 'UR', 'UF', 'LB', 'LF', 'RB', 'RF', 'DB', 'DL', 'DR', 'DF'],
        (4, 11): ['UB', 'UL', 'UR', 'UF', 'LB', 'LF', 'RB', 'RF', 'DB', 'DL', 'DR', 'DF'],
        (8, 20): ['UB', 'UL', 'UR', 'UF', 'LB', 'LF', 'RB', 'RF', 'DB', 'DL', 'DR', 'DF'],
        (6, 29): ['UB', 'UL', 'UR', 'UF', 'LB', 'LF', 'RB', 'RF', 'DB', 'DL', 'DR', 'DF'],

        (13, 42): ['UB', 'UL', 'UR', 'UF', 'LB', 'LF', 'RB', 'RF', 'DB', 'DL', 'DR', 'DF'],
        (15, 22): ['UB', 'UL', 'UR', 'UF', 'LB', 'LF', 'RB', 'RF', 'DB', 'DL', 'DR', 'DF'],
        (31, 24): ['UB', 'UL', 'UR', 'UF', 'LB', 'LF', 'RB', 'RF', 'DB', 'DL', 'DR', 'DF'],
        (33, 40): ['UB', 'UL', 'UR', 'UF', 'LB', 'LF', 'RB', 'RF', 'DB', 'DL', 'DR', 'DF'],

        (47, 26): ['UB', 'UL', 'UR', 'UF', 'LB', 'LF', 'RB', 'RF', 'DB', 'DL', 'DR', 'DF'],
        (49, 17): ['UB', 'UL', 'UR', 'UF', 'LB', 'LF', 'RB', 'RF', 'DB', 'DL', 'DR', 'DF'],
        (51, 35): ['UB', 'UL', 'UR', 'UF', 'LB', 'LF', 'RB', 'RF', 'DB', 'DL', 'DR', 'DF'],
        (53, 44): ['UB', 'UL', 'UR', 'UF', 'LB', 'LF', 'RB', 'RF', 'DB', 'DL', 'DR', 'DF'],
    }

    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            directory + "lookup-table-3x3x3-step110.txt",
            "x1x1U1x1xx1x1L1x1xx1x1F1x1xx1x1R1x1xx1x1B1x1xx1x1D1x1x",
            linecount=2048,
        )

    def state(self):
        state = self.parent.state[:]

        for edge_position in EDGE_TUPLES:
            for (e0, e1) in edge_position:
                edge_str = state[e0] + state[e1]

                if edge_str in self.edge_states.get((e0, e1), ()):
                    state[e0] = "1"
                    state[e1] = "1"
                    break
            else:
                state[e0] = "0"
                state[e1] = "0"

        for x in CORNERS:
            state[x] = "x"

        r = range(1, 55)
        result = "".join([state[x] for x in r])
        return result


phase2_edge_states = {
    (2, 38): ['UB', 'UL', 'UR', 'UF', 'DB', 'DL', 'DR', 'DF'],
    (4, 11): ['UB', 'UL', 'UR', 'UF', 'DB', 'DL', 'DR', 'DF'],
    (6, 29): ['UB', 'UL', 'UR', 'UF', 'DB', 'DL', 'DR', 'DF'],
    (8, 20): ['UB', 'UL', 'UR', 'UF', 'DB', 'DL', 'DR', 'DF'],

    (13, 42): ['LB', 'LF', 'RB', 'RF'],
    (15, 22): ['LB', 'LF', 'RB', 'RF'],
    (31, 24): ['LB', 'LF', 'RB', 'RF'],
    (33, 40): ['LB', 'LF', 'RB', 'RF'],

    (47, 26): ['UB', 'UL', 'UR', 'UF', 'DB', 'DL', 'DR', 'DF'],
    (49, 17): ['UB', 'UL', 'UR', 'UF', 'DB', 'DL', 'DR', 'DF'],
    (51, 35): ['UB', 'UL', 'UR', 'UF', 'DB', 'DL', 'DR', 'DF'],
    (53, 44): ['UB', 'UL', 'UR', 'UF', 'DB', 'DL', 'DR', 'DF'],
}

class LookupTable333Phase2Edges(LookupTable):
    """
    lookup-table-3x3x3-step121-edges.txt
    ====================================
    0 steps has 1 entries (0 percent, 0.00x previous step)
    1 steps has 2 entries (0 percent, 2.00x previous step)
    2 steps has 17 entries (3 percent, 8.50x previous step)
    3 steps has 104 entries (21 percent, 6.12x previous step)
    4 steps has 221 entries (44 percent, 2.12x previous step)
    5 steps has 150 entries (30 percent, 0.68x previous step)

    Total: 495 entries
    Average: 4.00 moves
    """

    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            directory + "lookup-table-3x3x3-step121-edges.txt",
            "xxxxx11xx11xx11xx11xxxxx",
            linecount=495,
        )

    def state(self):
        state = self.parent.state[:]
        X_PLANE_EDGES = ("LB", "BL", "LF", "FL", "RB", "BR", "RF", "FR")
        ref_phase2_edge_states = phase2_edge_states

        for edge_position in EDGE_TUPLES:
            for (e0, e1) in edge_position:
                edge_str = state[e0] + state[e1]

                if edge_str in X_PLANE_EDGES:
                    if edge_str in phase2_edge_states.get((e0, e1), ()):
                        state[e0] = "1"
                        state[e1] = "1"
                        break
                else:
                    state[e0] = "x"
                    state[e1] = "x"
                    break

            else:
                state[e0] = "0"
                state[e1] = "0"

        return "".join([state[x] for x in EDGES])


class LookupTable333Phase2Corners(LookupTable):
    """
    lookup-table-3x3x3-step122-corners.txt
    ======================================
    0 steps has 1 entries (0 percent, 0.00x previous step)
    1 steps has 2 entries (0 percent, 2.00x previous step)
    2 steps has 13 entries (0 percent, 6.50x previous step)
    3 steps has 70 entries (3 percent, 5.38x previous step)
    4 steps has 335 entries (15 percent, 4.79x previous step)
    5 steps has 1,008 entries (46 percent, 3.01x previous step)
    6 steps has 726 entries (33 percent, 0.72x previous step)
    7 steps has 32 entries (1 percent, 0.04x previous step)

    Total: 2,187 entries
    Average: 5.12 moves
    """
    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            directory + "lookup-table-3x3x3-step122-corners.txt",
            "UUUUxxxxxxxxxxxxxxxxUUUU",
            linecount=2187,
        )

    def state(self):
        state = self.parent.state[:]

        for x in CORNERS:
            if state[x] == "U" or state[x] == "D":
                state[x] = "U"
            else:
                state[x] = "x"

        return "".join([state[x] for x in CORNERS])


class LookupTable333Phase2(LookupTable):
    """
    lookup-table-3x3x3-step120.txt
    ==============================
    0 steps has 1 entries (0 percent, 0.00x previous step)
    1 steps has 2 entries (0 percent, 2.00x previous step)
    2 steps has 17 entries (0 percent, 8.50x previous step)
    3 steps has 134 entries (0 percent, 7.88x previous step)
    4 steps has 1,065 entries (0 percent, 7.95x previous step)
    5 steps has 8,190 entries (0 percent, 7.69x previous step)
    6 steps has 54,694 entries (5 percent, 6.68x previous step)
    7 steps has 267,576 entries (24 percent, 4.89x previous step)
    8 steps has 560,568 entries (51 percent, 2.09x previous step)
    9 steps has 187,204 entries (17 percent, 0.33x previous step)
    10 steps has 3,114 entries (0 percent, 0.02x previous step)

    Total: 1,082,565 entries
    Average: 7.80 moves
    """

    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            directory + "lookup-table-3x3x3-step120.txt",
            "UxUxUxUxUxxx1L1xxxxxx1F1xxxxxx1R1xxxxxx1B1xxxUxUxDxUxU",
            linecount=1082565,
            init_width=False,
        )

    def state(self):
        state = self.parent.state[:]
        X_PLANE_EDGES = ("LB", "BL", "LF", "FL", "RB", "BR", "RF", "FR")
        ref_phase2_edge_states = phase2_edge_states

        for edge_position in EDGE_TUPLES:
            for (e0, e1) in edge_position:
                edge_str = state[e0] + state[e1]

                if edge_str in X_PLANE_EDGES:
                    if edge_str in ref_phase2_edge_states.get((e0, e1), ()):
                        state[e0] = "1"
                        state[e1] = "1"
                        break
                else:
                    state[e0] = "x"
                    state[e1] = "x"
                    break

            else:
                state[e0] = "0"
                state[e1] = "0"

        for x in CORNERS:
            if state[x] == "U" or state[x] == "D":
                state[x] = "U"
            else:
                state[x] = "x"

        r = range(1, 55)
        return "".join([state[x] for x in r])

    def steps(self, state_to_find):
        """
        Return a list of the steps found in the lookup table for the current cube state
        """
        edges_state = self.parent.lt_phase2_edges.state()
        edges_index = int(self.parent.lt_phase2_edges.steps(edges_state)[0])

        corners_state = self.parent.lt_phase2_corners.state()
        corners_index = int(self.parent.lt_phase2_corners.steps(corners_state)[0])

        corners_count = 2187
        line_number = (edges_index * corners_count) + corners_index

        step_as_char = self.get_character(line_number)
        step = char_to_step[step_as_char]
        return [step,]


class LookupTable333Phase3Edges(LookupTable):
    """
    lookup-table-3x3x3-step131-edges.txt
    ====================================
    0 steps has 1 entries (1 percent, 0.00x previous step)
    1 steps has 2 entries (2 percent, 2.00x previous step)
    2 steps has 9 entries (12 percent, 4.50x previous step)
    3 steps has 30 entries (42 percent, 3.33x previous step)
    4 steps has 28 entries (40 percent, 0.93x previous step)

    Total: 70 entries
    Average: 3.17 moves
    """

    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            directory + "lookup-table-3x3x3-step131-edges.txt",
            "TBD",
            linecount=70,
        )

    def state(self):
        state = self.parent.state[:]
        Y_PLANE_EDGES = ("UF", "UB", "DF", "DB")

        for edge_position in EDGE_TUPLES:
            for (e0, e1) in edge_position:
                edge_str = state[e0] + state[e1]

                if edge_str in Y_PLANE_EDGES:
                    state[e0] = "F"
                    state[e1] = "F"
                else:
                    state[e0] = "x"
                    state[e1] = "x"
                break

        return "".join([state[x] for x in EDGES])


class LookupTable333Phase3Corners(LookupTable):
    """
    lookup-table-3x3x3-step132-corners.txt
    ======================================
    0 steps has 13 entries (0 percent, 0.00x previous step)
    1 steps has 275 entries (0 percent, 21.15x previous step)
    2 steps has 480 entries (1 percent, 1.75x previous step)
    3 steps has 1,152 entries (2 percent, 2.40x previous step)
    4 steps has 1,728 entries (4 percent, 1.50x previous step)
    5 steps has 4,800 entries (11 percent, 2.78x previous step)
    6 steps has 4,224 entries (10 percent, 0.88x previous step)
    7 steps has 4,992 entries (12 percent, 1.18x previous step)
    8 steps has 6,528 entries (16 percent, 1.31x previous step)
    9 steps has 9,216 entries (22 percent, 1.41x previous step)
    10 steps has 4,992 entries (12 percent, 0.54x previous step)
    11 steps has 1,920 entries (4 percent, 0.38x previous step)

    Total: 40,320 entries
    Average: 7.49 moves
    """

    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            directory + "lookup-table-3x3x3-step132-corners.txt",
            "TBD",
            linecount=40320,
        )

    def state(self):
        state = self.parent.state[:]
        return "".join([state[x] for x in CORNERS])


class LookupTable333Phase3(LookupTable):
    """
    lookup-table-3x3x3-step130.txt
    ==============================
    0 steps has 13 entries (0 percent, 0.00x previous step)
    1 steps has 275 entries (0 percent, 21.15x previous step)
    2 steps has 864 entries (0 percent, 3.14x previous step)
    3 steps has 3,456 entries (0 percent, 4.00x previous step)
    4 steps has 11,904 entries (0 percent, 3.44x previous step)
    5 steps has 50,880 entries (1 percent, 4.27x previous step)
    6 steps has 173,376 entries (6 percent, 3.41x previous step)
    7 steps has 358,272 entries (12 percent, 2.07x previous step)
    8 steps has 495,168 entries (17 percent, 1.38x previous step)
    9 steps has 678,720 entries (24 percent, 1.37x previous step)
    10 steps has 692,928 entries (24 percent, 1.02x previous step)
    11 steps has 307,392 entries (10 percent, 0.44x previous step)
    12 steps has 46,848 entries (1 percent, 0.15x previous step)
    13 steps has 2,304 entries (0 percent, 0.05x previous step)

    Total: 2,822,400 entries
    Average: 8.80 moves
    """

    state_targets = (
        'DFDxUxDFDLxLxLxLxLBFBxFxBFBRxRxRxRxRFFFxBxFFFUFUxDxUFU',
        'DFDxUxDFDLxLxLxRxRBFBxFxFFFRxRxRxLxLFFFxBxBFBUFUxDxUFU',
        'DFDxUxDFDLxRxLxLxRFFBxFxFFBRxLxRxRxLBFFxBxBFFUFUxDxUFU',
        'DFDxUxDFDLxRxLxRxLFFBxFxBFFRxLxRxLxRBFFxBxFFBUFUxDxUFU',
        'DFDxUxDFDRxLxLxLxRBFFxFxFFBLxRxRxRxLFFBxBxBFFUFUxDxUFU',
        'DFDxUxDFDRxLxLxRxLBFFxFxBFFLxRxRxLxRFFBxBxFFBUFUxDxUFU',
        'DFDxUxDFDRxRxLxLxLFFFxFxBFBLxLxRxRxRBFBxBxFFFUFUxDxUFU',
        'DFDxUxDFDRxRxLxRxRFFFxFxFFFLxLxRxLxLBFBxBxBFBUFUxDxUFU',
        'DFDxUxUFULxLxLxLxLFFFxFxBFBRxRxRxRxRFFFxBxBFBUFUxDxDFD',
        'DFDxUxUFULxLxLxRxRFFBxFxBFFLxLxRxRxRBFFxBxFFBDFDxDxUFU',
        'DFDxUxUFULxLxLxRxRFFBxFxFFBLxLxRxRxRBFFxBxBFFUFUxDxDFD',
        'DFDxUxUFULxLxLxRxRFFFxFxBFBRxRxRxLxLFFFxBxBFBDFDxDxUFU',
        'DFDxUxUFULxRxLxLxRBFBxFxBFBLxRxRxLxRFFFxBxFFFDFDxDxUFU',
        'DFDxUxUFULxRxLxLxRBFBxFxFFFLxRxRxLxRFFFxBxBFBUFUxDxDFD',
        'DFDxUxUFULxRxLxLxRBFFxFxBFFRxLxRxRxLBFFxBxBFFDFDxDxUFU',
        'DFDxUxUFULxRxLxRxLBFFxFxBFFRxLxRxLxRBFFxBxBFFUFUxDxDFD',
        'DFDxUxUFURxLxLxLxRFFBxFxFFBLxRxRxRxLFFBxBxFFBUFUxDxDFD',
        'DFDxUxUFURxLxLxRxLFFBxFxFFBLxRxRxLxRFFBxBxFFBDFDxDxUFU',
        'DFDxUxUFURxLxLxRxLFFFxFxBFBRxLxRxRxLBFBxBxFFFUFUxDxDFD',
        'DFDxUxUFURxLxLxRxLFFFxFxFFFRxLxRxRxLBFBxBxBFBDFDxDxUFU',
        'DFDxUxUFURxRxLxLxLBFBxFxFFFLxLxRxRxRBFBxBxFFFDFDxDxUFU',
        'DFDxUxUFURxRxLxLxLBFFxFxBFFRxRxRxLxLFFBxBxFFBUFUxDxDFD',
        'DFDxUxUFURxRxLxLxLBFFxFxFFBRxRxRxLxLFFBxBxBFFDFDxDxUFU',
        'DFDxUxUFURxRxLxRxRBFBxFxFFFLxLxRxLxLBFBxBxFFFUFUxDxDFD',
        'DFUxUxDFULxLxLxLxLBFFxFxBFFRxRxRxRxRBFFxBxBFFUFDxDxUFD',
        'DFUxUxDFULxLxLxRxRBFBxFxBFBLxLxRxRxRFFFxBxFFFDFUxDxDFU',
        'DFUxUxDFULxLxLxRxRBFBxFxFFFLxLxRxRxRFFFxBxBFBUFDxDxUFD',
        'DFUxUxDFULxLxLxRxRBFFxFxBFFRxRxRxLxLBFFxBxBFFDFUxDxDFU',
        'DFUxUxDFULxRxLxLxRFFBxFxBFFLxRxRxLxRBFFxBxFFBDFUxDxDFU',
        'DFUxUxDFULxRxLxLxRFFBxFxFFBLxRxRxLxRBFFxBxBFFUFDxDxUFD',
        'DFUxUxDFULxRxLxLxRFFFxFxBFBRxLxRxRxLFFFxBxBFBDFUxDxDFU',
        'DFUxUxDFULxRxLxRxLFFFxFxBFBRxLxRxLxRFFFxBxBFBUFDxDxUFD',
        'DFUxUxDFURxLxLxLxRBFBxFxFFFLxRxRxRxLBFBxBxFFFUFDxDxUFD',
        'DFUxUxDFURxLxLxRxLBFBxFxFFFLxRxRxLxRBFBxBxFFFDFUxDxDFU',
        'DFUxUxDFURxLxLxRxLBFFxFxBFFRxLxRxRxLFFBxBxFFBUFDxDxUFD',
        'DFUxUxDFURxLxLxRxLBFFxFxFFBRxLxRxRxLFFBxBxBFFDFUxDxDFU',
        'DFUxUxDFURxRxLxLxLFFBxFxFFBLxLxRxRxRFFBxBxFFBDFUxDxDFU',
        'DFUxUxDFURxRxLxLxLFFFxFxBFBRxRxRxLxLBFBxBxFFFUFDxDxUFD',
        'DFUxUxDFURxRxLxLxLFFFxFxFFFRxRxRxLxLBFBxBxBFBDFUxDxDFU',
        'DFUxUxDFURxRxLxRxRFFBxFxFFBLxLxRxLxLFFBxBxFFBUFDxDxUFD',
        'DFUxUxUFDLxLxLxLxLFFBxFxBFFRxRxRxRxRBFFxBxFFBUFDxDxDFU',
        'DFUxUxUFDLxLxLxRxRFFBxFxFFBRxRxRxLxLBFFxBxBFFUFDxDxDFU',
        'DFUxUxUFDLxRxLxLxRBFBxFxFFFRxLxRxRxLFFFxBxBFBUFDxDxDFU',
        'DFUxUxUFDLxRxLxRxLBFBxFxBFBRxLxRxLxRFFFxBxFFFUFDxDxDFU',
        'DFUxUxUFDRxLxLxLxRFFFxFxFFFLxRxRxRxLBFBxBxBFBUFDxDxDFU',
        'DFUxUxUFDRxLxLxRxLFFFxFxBFBLxRxRxLxRBFBxBxFFFUFDxDxDFU',
        'DFUxUxUFDRxRxLxLxLBFFxFxBFFLxLxRxRxRFFBxBxFFBUFDxDxDFU',
        'DFUxUxUFDRxRxLxRxRBFFxFxFFBLxLxRxLxLFFBxBxBFFUFDxDxDFU',
        'UFDxUxDFULxLxLxLxLBFFxFxFFBRxRxRxRxRFFBxBxBFFDFUxDxUFD',
        'UFDxUxDFULxLxLxRxRBFFxFxBFFRxRxRxLxLFFBxBxFFBDFUxDxUFD',
        'UFDxUxDFULxRxLxLxRFFFxFxBFBRxLxRxRxLBFBxBxFFFDFUxDxUFD',
        'UFDxUxDFULxRxLxRxLFFFxFxFFFRxLxRxLxRBFBxBxBFBDFUxDxUFD',
        'UFDxUxDFURxLxLxLxRBFBxFxBFBLxRxRxRxLFFFxBxFFFDFUxDxUFD',
        'UFDxUxDFURxLxLxRxLBFBxFxFFFLxRxRxLxRFFFxBxBFBDFUxDxUFD',
        'UFDxUxDFURxRxLxLxLFFBxFxFFBLxLxRxRxRBFFxBxBFFDFUxDxUFD',
        'UFDxUxDFURxRxLxRxRFFBxFxBFFLxLxRxLxLBFFxBxFFBDFUxDxUFD',
        'UFDxUxUFDLxLxLxLxLFFBxFxFFBRxRxRxRxRFFBxBxFFBDFUxDxDFU',
        'UFDxUxUFDLxLxLxRxRFFBxFxFFBRxRxRxLxLFFBxBxFFBUFDxDxUFD',
        'UFDxUxUFDLxLxLxRxRFFFxFxBFBLxLxRxRxRBFBxBxFFFDFUxDxDFU',
        'UFDxUxUFDLxLxLxRxRFFFxFxFFFLxLxRxRxRBFBxBxBFBUFDxDxUFD',
        'UFDxUxUFDLxRxLxLxRBFBxFxFFFRxLxRxRxLBFBxBxFFFUFDxDxUFD',
        'UFDxUxUFDLxRxLxLxRBFFxFxBFFLxRxRxLxRFFBxBxFFBDFUxDxDFU',
        'UFDxUxUFDLxRxLxLxRBFFxFxFFBLxRxRxLxRFFBxBxBFFUFDxDxUFD',
        'UFDxUxUFDLxRxLxRxLBFBxFxFFFRxLxRxLxRBFBxBxFFFDFUxDxDFU',
        'UFDxUxUFDRxLxLxLxRFFFxFxBFBLxRxRxRxLFFFxBxBFBDFUxDxDFU',
        'UFDxUxUFDRxLxLxRxLFFBxFxBFFRxLxRxRxLBFFxBxFFBUFDxDxUFD',
        'UFDxUxUFDRxLxLxRxLFFBxFxFFBRxLxRxRxLBFFxBxBFFDFUxDxDFU',
        'UFDxUxUFDRxLxLxRxLFFFxFxBFBLxRxRxLxRFFFxBxBFBUFDxDxUFD',
        'UFDxUxUFDRxRxLxLxLBFBxFxBFBRxRxRxLxLFFFxBxFFFUFDxDxUFD',
        'UFDxUxUFDRxRxLxLxLBFBxFxFFFRxRxRxLxLFFFxBxBFBDFUxDxDFU',
        'UFDxUxUFDRxRxLxLxLBFFxFxBFFLxLxRxRxRBFFxBxBFFUFDxDxUFD',
        'UFDxUxUFDRxRxLxRxRBFFxFxBFFLxLxRxLxLBFFxBxBFFDFUxDxDFU',
        'UFUxUxDFDLxLxLxLxLBFBxFxFFFRxRxRxRxRBFBxBxFFFDFDxDxUFU',
        'UFUxUxDFDLxLxLxRxRBFBxFxFFFRxRxRxLxLBFBxBxFFFUFUxDxDFD',
        'UFUxUxDFDLxLxLxRxRBFFxFxBFFLxLxRxRxRFFBxBxFFBDFDxDxUFU',
        'UFUxUxDFDLxLxLxRxRBFFxFxFFBLxLxRxRxRFFBxBxBFFUFUxDxDFD',
        'UFUxUxDFDLxRxLxLxRFFBxFxFFBRxLxRxRxLFFBxBxFFBUFUxDxDFD',
        'UFUxUxDFDLxRxLxLxRFFFxFxBFBLxRxRxLxRBFBxBxFFFDFDxDxUFU',
        'UFUxUxDFDLxRxLxLxRFFFxFxFFFLxRxRxLxRBFBxBxBFBUFUxDxDFD',
        'UFUxUxDFDLxRxLxRxLFFBxFxFFBRxLxRxLxRFFBxBxFFBDFDxDxUFU',
        'UFUxUxDFDRxLxLxLxRBFFxFxBFFLxRxRxRxLBFFxBxBFFDFDxDxUFU',
        'UFUxUxDFDRxLxLxRxLBFBxFxBFBRxLxRxRxLFFFxBxFFFUFUxDxDFD',
        'UFUxUxDFDRxLxLxRxLBFBxFxFFFRxLxRxRxLFFFxBxBFBDFDxDxUFU',
        'UFUxUxDFDRxLxLxRxLBFFxFxBFFLxRxRxLxRBFFxBxBFFUFUxDxDFD',
        'UFUxUxDFDRxRxLxLxLFFBxFxBFFRxRxRxLxLBFFxBxFFBUFUxDxDFD',
        'UFUxUxDFDRxRxLxLxLFFBxFxFFBRxRxRxLxLBFFxBxBFFDFDxDxUFU',
        'UFUxUxDFDRxRxLxLxLFFFxFxBFBLxLxRxRxRFFFxBxBFBUFUxDxDFD',
        'UFUxUxDFDRxRxLxRxRFFFxFxBFBLxLxRxLxLFFFxBxBFBDFDxDxUFU',
        'UFUxUxUFULxLxLxLxLFFFxFxFFFRxRxRxRxRBFBxBxBFBDFDxDxDFD',
        'UFUxUxUFULxLxLxRxRFFFxFxBFBRxRxRxLxLBFBxBxFFFDFDxDxDFD',
        'UFUxUxUFULxRxLxLxRBFFxFxBFFRxLxRxRxLFFBxBxFFBDFDxDxDFD',
        'UFUxUxUFULxRxLxRxLBFFxFxFFBRxLxRxLxRFFBxBxBFFDFDxDxDFD',
        'UFUxUxUFURxLxLxLxRFFBxFxBFFLxRxRxRxLBFFxBxFFBDFDxDxDFD',
        'UFUxUxUFURxLxLxRxLFFBxFxFFBLxRxRxLxRBFFxBxBFFDFDxDxDFD',
        'UFUxUxUFURxRxLxLxLBFBxFxFFFLxLxRxRxRFFFxBxBFBDFDxDxDFD',
        'UFUxUxUFURxRxLxRxRBFBxFxBFBLxLxRxLxLFFFxBxFFFDFDxDxDFD',
    )

    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            directory + "lookup-table-3x3x3-step130.txt",
            self.state_targets,
            linecount=2822400,
            init_width=False,
        )

    def state(self):
        state = self.parent.state[:]
        Y_PLANE_EDGES = ("UF", "UB", "DF", "DB")

        for edge_position in EDGE_TUPLES:
            for (e0, e1) in edge_position:
                edge_str = state[e0] + state[e1]

                if edge_str in Y_PLANE_EDGES:
                    state[e0] = "F"
                    state[e1] = "F"
                else:
                    state[e0] = "x"
                    state[e1] = "x"
                break

        r = range(1, 55)
        return "".join([state[x] for x in r])

    def steps(self, state_to_find):
        """
        Return a list of the steps found in the lookup table for the current cube state
        """
        edges_state = self.parent.lt_phase3_edges.state()
        edges_index = int(self.parent.lt_phase3_edges.steps(edges_state)[0])

        corners_state = self.parent.lt_phase3_corners.state()
        corners_index = int(self.parent.lt_phase3_corners.steps(corners_state)[0])

        corners_count = 40320
        line_number = (edges_index * corners_count) + corners_index

        step_as_char = self.get_character(line_number)
        step = char_to_step[step_as_char]
        return [step,]



class LookupTable333Phase4Edges(LookupTable):
    """
    lookup-table-3x3x3-step141-edges.txt
    ====================================
    0 steps has 1 entries (0 percent, 0.00x previous step)
    1 steps has 6 entries (0 percent, 6.00x previous step)
    2 steps has 27 entries (0 percent, 4.50x previous step)
    3 steps has 120 entries (1 percent, 4.44x previous step)
    4 steps has 519 entries (7 percent, 4.33x previous step)
    5 steps has 1,582 entries (22 percent, 3.05x previous step)
    6 steps has 2,911 entries (42 percent, 1.84x previous step)
    7 steps has 1,588 entries (22 percent, 0.55x previous step)
    8 steps has 158 entries (2 percent, 0.10x previous step)

    Total: 6,912 entries
    Average: 5.82 moves
    """
    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            directory + "lookup-table-3x3x3-step141-edges.txt",
            "UUUULLLLFFFFRRRRBBBBDDDD",
            linecount=6912,
        )

    def state(self):
        parent_state = self.parent.state
        return "".join([parent_state[x] for x in EDGES])


class LookupTable333Phase4Corners(LookupTable):
    """
    lookup-table-3x3x3-step142-corners.txt
    ======================================
    0 steps has 1 entries (1 percent, 0.00x previous step)
    1 steps has 6 entries (6 percent, 6.00x previous step)
    2 steps has 27 entries (28 percent, 4.50x previous step)
    3 steps has 42 entries (43 percent, 1.56x previous step)
    4 steps has 20 entries (20 percent, 0.48x previous step)

    Total: 96 entries
    Average: 2.77 moves
    """
    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            directory + "lookup-table-3x3x3-step142-corners.txt",
            "UUUULLLLFFFFRRRRBBBBDDDD",
            linecount=96,
        )

    def state(self):
        parent_state = self.parent.state
        return "".join([parent_state[x] for x in CORNERS])


class LookupTable333Phase4(LookupTable):
    """
    lookup-table-3x3x3-step140.txt
    ==============================
    0 steps has 1 entries (0 percent, 0.00x previous step)
    1 steps has 6 entries (0 percent, 6.00x previous step)
    2 steps has 27 entries (0 percent, 4.50x previous step)
    3 steps has 120 entries (0 percent, 4.44x previous step)
    4 steps has 519 entries (0 percent, 4.33x previous step)
    5 steps has 1,932 entries (0 percent, 3.72x previous step)
    6 steps has 6,484 entries (0 percent, 3.36x previous step)
    7 steps has 20,310 entries (3 percent, 3.13x previous step)
    8 steps has 55,034 entries (8 percent, 2.71x previous step)
    9 steps has 113,892 entries (17 percent, 2.07x previous step)
    10 steps has 178,495 entries (26 percent, 1.57x previous step)
    11 steps has 179,196 entries (27 percent, 1.00x previous step)
    12 steps has 89,728 entries (13 percent, 0.50x previous step)
    13 steps has 16,176 entries (2 percent, 0.18x previous step)
    14 steps has 1,488 entries (0 percent, 0.09x previous step)
    15 steps has 144 entries (0 percent, 0.10x previous step)

    Total: 663,552 entries
    Average: 10.13 moves
    """

    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            directory + "lookup-table-3x3x3-step140.txt",
            "UUUUUUUUULLLLLLLLLFFFFFFFFFRRRRRRRRRBBBBBBBBBDDDDDDDDD",
            linecount=663552,
            init_width=False,
        )

    def state(self):
        parent_state = self.parent.state
        r = range(1, 55)
        return "".join([parent_state[x] for x in r])

    def steps(self, state_to_find):
        """
        Return a list of the steps found in the lookup table for the current cube state
        """
        edges_state = self.parent.lt_phase4_edges.state()
        edges_index = int(self.parent.lt_phase4_edges.steps(edges_state)[0])

        corners_state = self.parent.lt_phase4_corners.state()
        corners_index = int(self.parent.lt_phase4_corners.steps(corners_state)[0])

        corners_count = 96
        line_number = (edges_index * corners_count) + corners_index

        step_as_char = self.get_character(line_number)
        step = char_to_step[step_as_char]
        return [step,]


class RubiksCube333(object):
    """
    A class for solving a 3x3x3 Rubiks Cube
    """

    def __init__(self, state, order):
        SQUARES_PER_SIDE = 9
        foo = []
        init_state = ["dummy"]
        init_state.extend(list(state))

        if order == "URFDLB":
            foo.extend(init_state[1 : SQUARES_PER_SIDE + 1])  # U
            foo.extend(init_state[(SQUARES_PER_SIDE * 4) + 1 : (SQUARES_PER_SIDE * 5) + 1])  # L
            foo.extend(init_state[(SQUARES_PER_SIDE * 2) + 1 : (SQUARES_PER_SIDE * 3) + 1])  # F
            foo.extend(init_state[(SQUARES_PER_SIDE * 1) + 1 : (SQUARES_PER_SIDE * 2) + 1])  # R
            foo.extend(init_state[(SQUARES_PER_SIDE * 5) + 1 : (SQUARES_PER_SIDE * 6) + 1])  # B
            foo.extend(init_state[(SQUARES_PER_SIDE * 3) + 1 : (SQUARES_PER_SIDE * 4) + 1])  # D
        elif order == "ULFRBD":
            foo.extend(init_state[1 : SQUARES_PER_SIDE + 1])  # U
            foo.extend(init_state[(SQUARES_PER_SIDE * 1) + 1 : (SQUARES_PER_SIDE * 2) + 1])  # L
            foo.extend(init_state[(SQUARES_PER_SIDE * 2) + 1 : (SQUARES_PER_SIDE * 3) + 1])  # F
            foo.extend(init_state[(SQUARES_PER_SIDE * 3) + 1 : (SQUARES_PER_SIDE * 4) + 1])  # R
            foo.extend(init_state[(SQUARES_PER_SIDE * 4) + 1 : (SQUARES_PER_SIDE * 5) + 1])  # B
            foo.extend(init_state[(SQUARES_PER_SIDE * 5) + 1 : (SQUARES_PER_SIDE * 6) + 1])  # D
        else:
            raise Exception("Add support for order %s" % order)

        self.solution = []
        self.state = ["x"]
        for side_name in foo:
            self.state.append(side_name)

        self.state_scratchpad = self.state[:]
        self.state_backup = self.state[:]

        self.lt_phase1 = LookupTable333Phase1(self)

        self.lt_phase2 = LookupTable333Phase2(self)
        self.lt_phase2_edges = LookupTable333Phase2Edges(self)
        self.lt_phase2_corners = LookupTable333Phase2Corners(self)

        self.lt_phase3 = LookupTable333Phase3(self)
        self.lt_phase3_edges = LookupTable333Phase3Edges(self)
        self.lt_phase3_corners = LookupTable333Phase3Corners(self)

        self.lt_phase4_edges = LookupTable333Phase4Edges(self)
        self.lt_phase4_corners = LookupTable333Phase4Corners(self)
        self.lt_phase4 = LookupTable333Phase4(self)

    # @timed_function
    def re_init(self):
        self.solution = []
        self.state = self.state_backup[:]

    # @timed_function
    def get_kociemba_string(self):
        """
        Return the cube state as a kociemba string
        """
        return "".join([self.state[x] for x in kociemba_sequence])

    # @timed_function
    def rotate(self, step):
        """
        Apply `step` to the cube and append `step` to our solution list
        """
        ref_swaps_333 = swaps_333
        ref_state = self.state
        ref_state_scratchpad = self.state_scratchpad

        # On a laptop the following list comp is the fastest way to do the rotate. This involves
        # allocating memory for the new list everytime though.  That malloc is about 600x slower
        # on Spike than it is on my laptop.
        #
        # self.state = [ref_state[x] for x in ref_swaps_333[step]]

        # So what we do instead is use a scratchpad bytearray to do the rotate without
        # any mallocs
        for (i, x) in enumerate(ref_swaps_333[step]):
            ref_state_scratchpad[i] = ref_state[x]

        for i in range(55):
            ref_state[i] = ref_state_scratchpad[i]

        self.solution.append(step)

    # @timed_function
    def rotate_side_X_to_Y(self, x, y):
        """
        Rotate the entire cube so that side `x` is on side `y`
        """

        if y == "U":
            pos_to_check = 5
        elif y == "L":
            pos_to_check = 14
        elif y == "F":
            pos_to_check = 23
        elif y == "R":
            pos_to_check = 32
        elif y == "B":
            pos_to_check = 41
        elif y == "D":
            pos_to_check = 50

        F_pos_to_check = 23
        D_pos_to_check = 50

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
        self.rotate_side_X_to_Y("U", "U")

    # @timed_function
    def rotate_F_to_F(self):
        """
        Rotate side F to the front
        """
        self.rotate_side_X_to_Y("F", "F")

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
    def solve(self):
        """
        Solve the cube and return the solution
        """
        print("INIT CUBE:\n%s" % (cube2strcolor(self.state)))
        self.rotate_U_to_U()
        self.rotate_F_to_F()

        original_state = self.state[:]
        original_solution= self.solution[:]

        self.lt_phase1.solve()
        solution_len = get_solution_len(self.solution)
        self.solution.append("COMMENT phase 1: EO edges ({} steps)".format(solution_len))
        prev_solution_len = solution_len
        print(cube2strcolor(self.state))
        print("phase1 complete, {} steps in".format(solution_len))

        self.lt_phase2.solve()
        solution_len = get_solution_len(self.solution)
        self.solution.append("COMMENT phase 2: ({} steps)".format(solution_len - prev_solution_len))
        prev_solution_len = solution_len
        print(cube2strcolor(self.state))
        print("phase2 complete, {} steps in".format(solution_len))

        self.lt_phase3.solve()
        solution_len = get_solution_len(self.solution)
        self.solution.append("COMMENT phase 3: ({} steps)".format(solution_len - prev_solution_len))
        prev_solution_len = solution_len
        print(cube2strcolor(self.state))
        print("phase3 complete, {} steps in".format(solution_len))

        self.lt_phase4.solve()
        solution_len = get_solution_len(self.solution)
        self.solution.append("COMMENT phase 4: ({} steps)".format(solution_len - prev_solution_len))
        prev_solution_len = solution_len
        print(cube2strcolor(self.state))
        print("phase4 complete, {} steps in".format(solution_len))

        #print("FINAL CUBE:\n%s" % (cube2strcolor(self.state)))
        self.solution = compress_solution(self.solution)
        print(get_alg_cubing_net_url(self.solution))

        # Remove the comments from the solution
        self.solution = [x for x in self.solution if not x.startswith("COMMENT")]

        # Put the cube back in the original state and apply the solution to
        # make sure it solves the cube.
        self.verify_solution(original_state, self.solution)

        return self.solution
