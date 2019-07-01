
import logging
import sys
from rubikscubesolvermicropython.movetables import (
    mtb0, mtd0,
    mtb1, mtd1,
    mtb2, mtd2,
    mtb3, mtd3,
    mtb4, mtd4,
    mtb5, mtd5,
    mtb6, mtd6,
    mtb7, mtd7,
    mtb8, mtd8,
)

log = logging.getLogger(__name__)


FACELET_COUNT = 54

side2str = {
    0 : "U",
    1 : "F",
    2 : "D",
    3 : "B",
    4 : "R",
    5 : "L",
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

kociemba_sequence = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, # U
    27, 28, 29, 30, 31, 32, 33, 34, 35, # R
    18, 19, 20, 21, 22, 23, 24, 25, 26, # F
    45, 46, 47, 48, 49, 50, 51, 52, 53, # D
    9, 10, 11, 12, 13, 14, 15, 16, 17, # L
    36, 37, 38, 39, 40, 41, 42, 43, 44, # B
)

# There are 24 combinations to try in terms of which colors
# are on side U and side F
rotations_24 = (
    (),
    ("y",),
    ("y'",),
    ("y", "y"),
    ("x", "x"),
    ("x", "x", "y"),
    ("x", "x", "y'"),
    ("x", "x", "y", "y"),
    ("y'", "x"),
    ("y'", "x", "y"),
    ("y'", "x", "y'"),
    ("y'", "x", "y", "y"),
    ("x",),
    ("x", "y"),
    ("x", "y'"),
    ("x", "y", "y"),
    ("y", "x"),
    ("y", "x", "y"),
    ("y", "x", "y'"),
    ("y", "x", "y", "y"),
    ("x'",),
    ("x'", "y"),
    ("x'", "y'"),
    ("x'", "y", "y"),
)



# facelet swaps for 3x3x3 moves
swaps_333 = {
    "B" : [29, 32, 35, 3, 4, 5, 6, 7, 8, 2, 10, 11, 1, 13, 14, 0, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 53, 30, 31, 52, 33, 34, 51, 42, 39, 36, 43, 40, 37, 44, 41, 38, 45, 46, 47, 48, 49, 50, 9, 12, 15],
    "B'" : [15, 12, 9, 3, 4, 5, 6, 7, 8, 51, 10, 11, 52, 13, 14, 53, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 0, 30, 31, 1, 33, 34, 2, 38, 41, 44, 37, 40, 43, 36, 39, 42, 45, 46, 47, 48, 49, 50, 35, 32, 29],
    "B2" : [53, 52, 51, 3, 4, 5, 6, 7, 8, 35, 10, 11, 32, 13, 14, 29, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 15, 30, 31, 12, 33, 34, 9, 44, 43, 42, 41, 40, 39, 38, 37, 36, 45, 46, 47, 48, 49, 50, 2, 1, 0],
    "D" : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 42, 43, 44, 18, 19, 20, 21, 22, 23, 15, 16, 17, 27, 28, 29, 30, 31, 32, 24, 25, 26, 36, 37, 38, 39, 40, 41, 33, 34, 35, 51, 48, 45, 52, 49, 46, 53, 50, 47],
    "D'" : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 24, 25, 26, 18, 19, 20, 21, 22, 23, 33, 34, 35, 27, 28, 29, 30, 31, 32, 42, 43, 44, 36, 37, 38, 39, 40, 41, 15, 16, 17, 47, 50, 53, 46, 49, 52, 45, 48, 51],
    "D2" : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 33, 34, 35, 18, 19, 20, 21, 22, 23, 42, 43, 44, 27, 28, 29, 30, 31, 32, 15, 16, 17, 36, 37, 38, 39, 40, 41, 24, 25, 26, 53, 52, 51, 50, 49, 48, 47, 46, 45],
    "F" : [0, 1, 2, 3, 4, 5, 17, 14, 11, 9, 10, 45, 12, 13, 46, 15, 16, 47, 24, 21, 18, 25, 22, 19, 26, 23, 20, 6, 28, 29, 7, 31, 32, 8, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 33, 30, 27, 48, 49, 50, 51, 52, 53],
    "F'" : [0, 1, 2, 3, 4, 5, 27, 30, 33, 9, 10, 8, 12, 13, 7, 15, 16, 6, 20, 23, 26, 19, 22, 25, 18, 21, 24, 47, 28, 29, 46, 31, 32, 45, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 11, 14, 17, 48, 49, 50, 51, 52, 53],
    "F2" : [0, 1, 2, 3, 4, 5, 47, 46, 45, 9, 10, 33, 12, 13, 30, 15, 16, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 28, 29, 14, 31, 32, 11, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 8, 7, 6, 48, 49, 50, 51, 52, 53],
    "L" : [44, 1, 2, 41, 4, 5, 38, 7, 8, 15, 12, 9, 16, 13, 10, 17, 14, 11, 0, 19, 20, 3, 22, 23, 6, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 51, 39, 40, 48, 42, 43, 45, 18, 46, 47, 21, 49, 50, 24, 52, 53],
    "L'" : [18, 1, 2, 21, 4, 5, 24, 7, 8, 11, 14, 17, 10, 13, 16, 9, 12, 15, 45, 19, 20, 48, 22, 23, 51, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 6, 39, 40, 3, 42, 43, 0, 44, 46, 47, 41, 49, 50, 38, 52, 53],
    "L2" : [45, 1, 2, 48, 4, 5, 51, 7, 8, 17, 16, 15, 14, 13, 12, 11, 10, 9, 44, 19, 20, 41, 22, 23, 38, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 24, 39, 40, 21, 42, 43, 18, 0, 46, 47, 3, 49, 50, 6, 52, 53],
    "R" : [0, 1, 20, 3, 4, 23, 6, 7, 26, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 47, 21, 22, 50, 24, 25, 53, 33, 30, 27, 34, 31, 28, 35, 32, 29, 8, 37, 38, 5, 40, 41, 2, 43, 44, 45, 46, 42, 48, 49, 39, 51, 52, 36],
    "R'" : [0, 1, 42, 3, 4, 39, 6, 7, 36, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 21, 22, 5, 24, 25, 8, 29, 32, 35, 28, 31, 34, 27, 30, 33, 53, 37, 38, 50, 40, 41, 47, 43, 44, 45, 46, 20, 48, 49, 23, 51, 52, 26],
    "R2" : [0, 1, 47, 3, 4, 50, 6, 7, 53, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 42, 21, 22, 39, 24, 25, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 37, 38, 23, 40, 41, 20, 43, 44, 45, 46, 2, 48, 49, 5, 51, 52, 8],
    "U" : [6, 3, 0, 7, 4, 1, 8, 5, 2, 18, 19, 20, 12, 13, 14, 15, 16, 17, 27, 28, 29, 21, 22, 23, 24, 25, 26, 36, 37, 38, 30, 31, 32, 33, 34, 35, 9, 10, 11, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
    "U'" : [2, 5, 8, 1, 4, 7, 0, 3, 6, 36, 37, 38, 12, 13, 14, 15, 16, 17, 9, 10, 11, 21, 22, 23, 24, 25, 26, 18, 19, 20, 30, 31, 32, 33, 34, 35, 27, 28, 29, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
    "U2" : [8, 7, 6, 5, 4, 3, 2, 1, 0, 27, 28, 29, 12, 13, 14, 15, 16, 17, 36, 37, 38, 21, 22, 23, 24, 25, 26, 9, 10, 11, 30, 31, 32, 33, 34, 35, 18, 19, 20, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
    "x" : [18, 19, 20, 21, 22, 23, 24, 25, 26, 11, 14, 17, 10, 13, 16, 9, 12, 15, 45, 46, 47, 48, 49, 50, 51, 52, 53, 33, 30, 27, 34, 31, 28, 35, 32, 29, 8, 7, 6, 5, 4, 3, 2, 1, 0, 44, 43, 42, 41, 40, 39, 38, 37, 36],
    "x'" : [44, 43, 42, 41, 40, 39, 38, 37, 36, 15, 12, 9, 16, 13, 10, 17, 14, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 29, 32, 35, 28, 31, 34, 27, 30, 33, 53, 52, 51, 50, 49, 48, 47, 46, 45, 18, 19, 20, 21, 22, 23, 24, 25, 26],
    "x2" : [45, 46, 47, 48, 49, 50, 51, 52, 53, 17, 16, 15, 14, 13, 12, 11, 10, 9, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 0, 1, 2, 3, 4, 5, 6, 7, 8],
    "y" : [6, 3, 0, 7, 4, 1, 8, 5, 2, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 9, 10, 11, 12, 13, 14, 15, 16, 17, 47, 50, 53, 46, 49, 52, 45, 48, 51],
    "y'" : [2, 5, 8, 1, 4, 7, 0, 3, 6, 36, 37, 38, 39, 40, 41, 42, 43, 44, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 51, 48, 45, 52, 49, 46, 53, 50, 47],
    "y2" : [8, 7, 6, 5, 4, 3, 2, 1, 0, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 53, 52, 51, 50, 49, 48, 47, 46, 45],
    "z" : [15, 12, 9, 16, 13, 10, 17, 14, 11, 51, 48, 45, 52, 49, 46, 53, 50, 47, 24, 21, 18, 25, 22, 19, 26, 23, 20, 6, 3, 0, 7, 4, 1, 8, 5, 2, 38, 41, 44, 37, 40, 43, 36, 39, 42, 33, 30, 27, 34, 31, 28, 35, 32, 29],
    "z'" : [29, 32, 35, 28, 31, 34, 27, 30, 33, 2, 5, 8, 1, 4, 7, 0, 3, 6, 20, 23, 26, 19, 22, 25, 18, 21, 24, 47, 50, 53, 46, 49, 52, 45, 48, 51, 42, 39, 36, 43, 40, 37, 44, 41, 38, 11, 14, 17, 10, 13, 16, 9, 12, 15],
    "z2" : [53, 52, 51, 50, 49, 48, 47, 46, 45, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 44, 43, 42, 41, 40, 39, 38, 37, 36, 8, 7, 6, 5, 4, 3, 2, 1, 0],
}


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


def find_corner(cube, f0, f1, f2):
    """
    Return a number from 0-23 that indicates where corner `f0/f1/f2` is located
    """
    for (index, (corner0, corner1, corner2)) in enumerate((
            (29, 2, 36), (36, 29, 2), (2, 36, 29), # UBR
            (38, 0, 9), (9, 38, 0), (0, 9, 38), # ULB
            (11, 6, 18), (18, 11, 6), (6, 18, 11), # UFL
            (20, 8, 27), (27, 20, 8), (8, 27, 20), # URF
            (24, 45, 17), (17, 24, 45), (45, 17, 24), # DLF
            (15, 51, 44), (44, 15, 51), (51, 44, 15), # DBL
            (42, 53, 35), (35, 42, 53), (53, 35, 42), # DRB
            (33, 47, 26), (26, 33, 47), (47, 26, 33), # DFR
        )):

        if cube[corner0] == f0 and cube[corner1] == f1 and cube[corner2] == f2:
            return index

    raise Exception("Could not find corner f0/f1/f2 %s/%s/%s in\n%s\n" % (f0, f1, f2, cube2str(cube)))


def find_edge(cube, f0, f1):
    """
    Return a number from 0-23 that indicates where edge `f0/f1` is located
    """
    for (index, (edge0, edge1)) in enumerate((
            (37, 1), (1, 37), # UB
            (10, 3), (3, 10), # UL
            (19, 7), (7, 19), # UF
            (28, 5), (5, 28), # UR
            (21, 14), (14, 21), # LF
            (12, 41), (41, 12), # BL
            (16, 48), (48, 16), # DL
            (39, 32), (32, 39), # RB
            (43, 52), (52, 43), # DB
            (30, 23), (23, 30), # FR
            (34, 50), (50, 34), # DR
            (25, 46), (46, 25), # DF
        )):

        if cube[edge0] == f0 and cube[edge1] == f1:
            return index

    raise Exception("Could not find edge f0/f1 %s/%s\n%s" % (f0, f1, cube2str(cube)))


def RFIX(RR):
    """
    Normalize to range -1 to 2
    """
    return ((int(RR) + 1) & 3) - 1


def get_step_string(f, r):
    """
    Give the face `f` and rotation `r`, return the string equivalent such as U, U', U2, etc
    """
    r &= 3
    step = side2str[f]

    # r is 1/4 forward, 1/4 backward or 1/2 turn
    if r == 1:
        pass
    elif r == 2:
        step += "2"
    elif r == 3:
        step += "'"
    else:
        raise Exception("rotate r '%s' is invalid" % r)

    return step


def get_solution_len_minus_rotates(solution):
    """
    Return the length of `solution` ignoring comments and whole cube rotations
    """
    count = 0

    for step in solution:

        if step.startswith("COMMENT"):
            continue

        if step in ("x", "x'", "x2", "y", "y'", "y2", "z", "z'", "z2"):
            continue

        count += 1

    return count


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
        if step.startswith("3"):
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

        self.index_init_all()

    def get_kociemba_string(self):
        """
        Return the cube state as a kociemba string
        """
        return "".join([self.state[x] for x in kociemba_sequence])

    def rotate(self, step):
        """
        Apply `step` to the cube and append `step` to our solution list
        """
        new_state = [self.state[x] for x in swaps_333[step]]
        self.state = new_state
        self.solution.append(step)

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

    def rotate_U_to_U(self):
        """
        Rotate side U to the top
        """
        self.rotate_side_X_to_Y("U", "U")

    def rotate_F_to_F(self):
        """
        Rotate side F to the front
        """
        self.rotate_side_X_to_Y("F", "F")

    def recolor(self, recolor_map):
        """
        Recolor the squares of the cube per `recolor_map`
        """
        for x in range(FACELET_COUNT):
            x_color = self.state[x]
            x_new_color = recolor_map[x_color]
            self.state[x] = x_new_color

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

    def index_init(self):
        """
        Initialize indexes. This is called at the start of each phase for solving a cube.
        """
        self.idx_nc = 0
        self.idx_ne = 0
        self.idx = 0

    def index_last(self):
        """
        Initialize indexes for the last phase
        """
        self.idx = ((self.idx >> 2) <<1 ) | (self.idx & 1);

    def index_corner(self, f0, f1, f2):
        """
        Set idx, idx_ic and idx_nc for corner `f0/f1/f2`
        """
        ic = find_corner(self.state, f0, f1, f2)

        for i in range(self.idx_nc):
            if ic > self.idx_idx[i]:
                ic -= 3

        self.idx = (self.idx * self.idx_ic) + ic
        self.idx_idx[self.idx_nc] = ic
        self.idx_nc += 1
        self.idx_ic -= 3

    def index_edge(self, f0, f1):
        """
        Set idx, idx_ie and idx_ne for edge `f0/f1`
        """
        ie = find_edge(self.state, f0, f1)

        for i in range(self.idx_ne):
            if ie > self.idx_idx[i]:
                ie -= 2

        self.idx = (self.idx * self.idx_ie) + ie
        self.idx_idx[self.idx_ne] = ie
        self.idx_ne += 1
        self.idx_ie -= 2

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
            print("ERROR: cube should be solved but it is not solved")
            print(cube2strcolor(self.state))
            sys.exit(0)

    def solve_phase(self, phase, mtb, mtd):
        """
        Solve a single phase per the `mtb`/`mtd` tables
        """
        # print("phase %d has %s entries" % (phase, len(mtd)))
        sz = len(mtd) / mtb
        self.idx = sz - self.idx

        if self.idx > 0:
            i = int((self.idx - 1) * mtb)
            b = mtd[i]
            i += 1

            if b != 0xFF:
                mvm = mtb * 2 - 1
                mv = 0
                f0 = int(b / 3)
                r0 = RFIX(b - (f0 * 3) + 1)
                step = get_step_string(f0, r0)
                self.rotate(step)

                mv += 1
                while mv < mvm:
                    b >>= 4

                    if (mv & 1) != 0:
                        b = mtd[i]
                        i += 1

                    b0 = b & 0xF

                    if b0 == 0xF:
                        break

                    f1 = int(b0 / 3)
                    r0 = RFIX(b0 - (f1 * 3) + 1)

                    if f1 >= f0:
                        f1 += 1

                    f0 = f1
                    step = get_step_string(f0, r0)
                    self.rotate(step)

                    mv += 1

    def solve(self):
        """
        Solve the cube and return the solution
        """

        print("INIT CUBE:\n%s" % (cube2strcolor(self.state)))
        solution_len = len(self.solution)
        prev_solution_len = solution_len
        self.rotate_U_to_U()
        self.rotate_F_to_F()

        # We should be able to drop in different phases/tables in the future
        phases = (
            (1, "two edges", (), (("D", "F"), ("D", "R")), mtb0, mtd0),
            (2, "one corner, one edge", (("D", "F", "R"),), (("F", "R"),), mtb1, mtd1),
            (3, "one edge", (), (("D", "B"),), mtb2, mtd2),
            (4, "one corner, one edge", (("D", "R", "B"),), (("R", "B"),), mtb3, mtd3),
            (5, "one edge", (), (("D", "L"),), mtb4, mtd4),
            (6, "one corner, one edge", (("D", "B", "L"),), (("B", "L"),), mtb5, mtd5),
            (7, "one corner, one edge", (("D", "L", "F"),), (("L", "F"),), mtb6, mtd6),
            (8, "last three corners", (("U", "R", "F"), ("U", "F", "L"), ("U", "L", "B")), (), mtb7, mtd7),
            (9, "last three edges", (), (("U", "R"), ("U", "F"), ("U", "L")), mtb8, mtd8),
        )

        # Try all 24 rotations, keep the one with the shortest solution
        min_solution = None
        min_solution_len = 999
        min_solution_recolor_map = None

        original_state = self.state[:]
        original_solution = self.solution [:]

        for rotations in rotations_24:
            self.state = original_state[:]
            self.solution = original_solution[:]

            for step in rotations:
                self.rotate(step)

            solution_len = len(self.solution)
            prev_solution_len = solution_len

            recolor_map = {
                self.state[4] : "U",
                self.state[13] : "L",
                self.state[22] : "F",
                self.state[31] : "R",
                self.state[40] : "B",
                self.state[49] : "D",
            }

            self.recolor(recolor_map)
            self.index_init_all()

            for (phase, desc, corners, edges, mtb, mtd) in phases:
                self.index_init()

                for corner in corners:
                    self.index_corner(*corner)

                for edge in edges:
                    self.index_edge(*edge)

                if phase == len(phases):
                    self.index_last()

                self.solve_phase(phase, mtb, mtd)
                solution_len = len(self.solution)
                self.solution.append("COMMENT phase %s: %s (%d steps)" % (
                    phase, desc, (solution_len - prev_solution_len)))
                prev_solution_len = solution_len

            solution_len = get_solution_len_minus_rotates(self.solution)

            if solution_len < min_solution_len:
                min_solution_len = solution_len
                min_solution_recolor_map = recolor_map
                min_solution = self.solution[:]
                log.info("(NEW MIN) rotations %s, solution len %d" % (" ".join(rotations), solution_len))
            else:
                log.info("rotations %s, solution len %d" % (" ".join(rotations), solution_len))

        self.solution = compress_solution(min_solution)

        print("FINAL CUBE:\n%s" % (cube2strcolor(self.state)))
        print(get_alg_cubing_net_url(self.solution))

        # Remove the comments from the solution
        self.solution = [x for x in self.solution if not x.startswith("COMMENT")]

        self.verify_solution(original_state, self.solution)

        return self.solution
