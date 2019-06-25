
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

#-----------------------
# Face indices to string
#-----------------------
side2str = {
    0 : "U",
    1 : "F",
    2 : "D",
    3 : "B",
    4 : "R",
    5 : "L",
}


NPIECE = 3
MV_MAX = 100
idx_idx = [None] * NPIECE
mv_f = [None] * MV_MAX
mv_r = [None] * MV_MAX

idx_nc = 0
idx_ne = 0
idx = 0
mv_n = 0
idx_ic = 24
idx_ie = 24
solution = []


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
    Return a readable string of the cube
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
    Add color to the cube string
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
    Return an alg.cubing.net URL for 'solution'
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


def index_init():
    """
    Initialize indexes
    """
    global idx_nc, idx_ne, idx
    idx_nc = 0
    idx_ne = 0
    idx = 0


def index_last():
    """
    Initialize indexes for the last time
    """
    global idx
    idx = ((idx>>2)<<1)|(idx&1);


def RFIX(RR):
    """
    Normalise to range -1 to 2
    """
    return ((int(RR) + 1) & 3) - 1


def find_corner(cube, f0, f1, f2):
    """
    Return a number from 0-23 that indicates where corner f0/f1/f2 is located
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


def index_corner(cube, f0, f1, f2):
    """
    Set idx, idx_ic and idx_nc for a corner
    """
    global idx_ic
    global idx_nc
    global idx
    ic = find_corner(cube, f0, f1, f2)

    for i in range(idx_nc):
        if ic > idx_idx[i]:
            ic -= 3

    idx = (idx * idx_ic) + ic
    idx_idx[idx_nc] = ic
    idx_nc += 1
    idx_ic -= 3


def find_edge(cube, f0, f1):
    """
    Return a number from 0-23 that indicates where edge f0/f1 is located
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


def index_edge(cube, f0, f1):
    """
    Set idx, idx_ie and idx_ne for an edge
    """
    global idx_ie
    global idx_ne
    global idx
    ie = find_edge(cube, f0, f1)

    for i in range(idx_ne):
        if ie > idx_idx[i]:
            ie -= 2

    idx = (idx * idx_ie) + ie
    idx_idx[idx_ne] = ie
    idx_ne += 1
    idx_ie -= 2


def rotate(cube, side, r):
    r &= 3

    # r is 1/4 forward, 1/4 backward or 1/2 turn
    step = side

    if r == 1:
        pass
    elif r == 2:
        step += "2"
    elif r == 3:
        step += "'"
    else:
        raise Exception("rotate r '%s' is invalid" % r)

    solution.append(step)
    cube = [cube[x] for x in swaps_333[step]]
    return cube


def solve_phase(cube, mtb, mtd):
    global idx
    sz = len(mtd) / mtb
    idx = sz - idx

    log.info("solve_phase: mtb %s, len(mtd) %s, sz %s, idx %s" % (mtb, len(mtd), sz, idx))

    if idx > 0:
        i = int((idx - 1) * mtb)
        b = mtd[i]
        i += 1

        if b != 0xFF:
            mvm = mtb * 2 - 1
            mv = 0
            f0 = int(b / 3)
            r0 = RFIX(b - (f0 * 3) + 1)
            cube = rotate(cube, side2str[f0], r0)

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
                cube = rotate(cube, side2str[f0], r0)

                mv += 1
    return cube


def solve_one(cube):
    global solution
    log.info("INIT CUBE:\n%s" % (cube2strcolor(cube)))
    solution_len = len(solution)
    prev_solution_len = solution_len

    # phase 1 - solve edges DF DR
    index_init()
    index_edge(cube, "D", "F")
    index_edge(cube, "D", "R")
    cube = solve_phase(cube, mtb0, mtd0)
    solution_len = len(solution)
    solution.append("COMMENT phase 1: solve edges DF DR (%d steps)" % (solution_len - prev_solution_len))
    prev_solution_len = solution_len

    # phase 2 - solve corner DFR and edge FR
    index_init()
    index_corner(cube, "D", "F", "R")
    index_edge(cube, "F", "R")
    cube = solve_phase(cube, mtb1, mtd1)
    solution_len = len(solution)
    solution.append("COMMENT phase 2: solve corner DFR and edge FR (%d steps)" % (solution_len - prev_solution_len))
    prev_solution_len = solution_len

    # phase 3 - solve edge DB
    index_init()
    index_edge(cube, "D", "B")
    cube = solve_phase(cube, mtb2, mtd2)
    solution_len = len(solution)
    solution.append("COMMENT phase 3: solve edge DB (%d steps)" % (solution_len - prev_solution_len))
    prev_solution_len = solution_len

    # phase 4 - solve corner DRB and edge RB
    index_init()
    index_corner(cube, "D", "R", "B")
    index_edge(cube, "R", "B")
    cube = solve_phase(cube, mtb3, mtd3)
    solution_len = len(solution)
    solution.append("COMMENT phase 4: solve corner DRB and edge RB (%d steps)" % (solution_len - prev_solution_len))
    prev_solution_len = solution_len

    # phase 5 - solve edge DL
    index_init()
    index_edge(cube, "D", "L")
    cube = solve_phase(cube, mtb4, mtd4)
    solution_len = len(solution)
    solution.append("COMMENT phase 5: solve edge DL (%d steps)" % (solution_len - prev_solution_len))
    prev_solution_len = solution_len

    # phase 6 - solve corner DBL and edge BL
    index_init()
    index_corner(cube, "D", "B", "L")
    index_edge(cube, "B", "L")
    cube = solve_phase(cube, mtb5, mtd5)
    solution_len = len(solution)
    solution.append("COMMENT phase 6: solve corner DBL and edge BL (%d steps)" % (solution_len - prev_solution_len))
    prev_solution_len = solution_len

    # phase 7 - solve corner DLF and edge LF
    index_init()
    index_corner(cube, "D", "L", "F")
    index_edge(cube, "L", "F")
    cube = solve_phase(cube, mtb6, mtd6)
    solution_len = len(solution)
    solution.append("COMMENT phase 7: solve corner DLF and edge LF (%d steps)" % (solution_len - prev_solution_len))
    prev_solution_len = solution_len

    # phase 8 - solve corners URF, UFL, and ULB
    index_init()
    index_corner(cube, "U", "R", "F")
    index_corner(cube, "U", "F", "L")
    index_corner(cube, "U", "L", "B")
    cube = solve_phase(cube, mtb7, mtd7)
    solution_len = len(solution)
    solution.append("COMMENT phase 8: solve corners URF, UFL, and ULB (%d steps)" % (solution_len - prev_solution_len))
    prev_solution_len = solution_len

    # phase 9 - solve edges UR, UF and UL
    index_init()
    index_edge(cube, "U", "R")
    index_edge(cube, "U", "F")
    index_edge(cube, "U", "L")
    index_last()
    cube = solve_phase(cube, mtb8, mtd8)
    solution_len = len(solution)
    solution.append("COMMENT phase 9: solve edges UR, UF and UL (%d steps)" % (solution_len - prev_solution_len))
    prev_solution_len = solution_len

    log.info("FINAL CUBE:\n%s" % (cube2strcolor(cube)))
    log.info(get_alg_cubing_net_url(solution))

    # Remove the comments from the solution
    solution = [x for x in solution if not x.startswith("COMMENT")]


class RubiksCube333(object):

    def __init__(self, state, order):
        self.solution = []
        self.state = []
        state = list(state)
        squares_per_side = 9

        if order == 'URFDLB':
            self.state.extend(state[0:squares_per_side])                            # U
            self.state.extend(state[(squares_per_side * 4):(squares_per_side * 5)]) # L
            self.state.extend(state[(squares_per_side * 2):(squares_per_side * 3)]) # F
            self.state.extend(state[(squares_per_side * 1):(squares_per_side * 2)]) # R
            self.state.extend(state[(squares_per_side * 5):(squares_per_side * 6)]) # B
            self.state.extend(state[(squares_per_side * 3):(squares_per_side * 4)]) # D
        elif order == 'ULFRBD':
            self.state.extend(state[0:squares_per_side])                            # U
            self.state.extend(state[(squares_per_side * 1):(squares_per_side * 2)]) # L
            self.state.extend(state[(squares_per_side * 2):(squares_per_side * 3)]) # F
            self.state.extend(state[(squares_per_side * 3):(squares_per_side * 4)]) # R
            self.state.extend(state[(squares_per_side * 4):(squares_per_side * 5)]) # B
            self.state.extend(state[(squares_per_side * 5):(squares_per_side * 6)]) # D
        else:
            raise Exception("Add support for order %s" % order)

    def solve(self):
        solve_one(self.state)
        self.solution = solution
