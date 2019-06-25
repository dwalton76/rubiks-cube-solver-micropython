
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

#-----------------------------------------------------------------------------
# Face indices
#-----------------------------------------------------------------------------
U = 0
F = 1
D = 2
B = 3
R = 4
L = 5

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


def cube2str(cube):
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



def index_init():
    global idx_nc, idx_ne, idx
    idx_nc = 0
    idx_ne = 0
    idx = 0


def index_last():
    global idx
    idx = ((idx>>2)<<1)|(idx&1);


def RFIX(RR):
    return ((int(RR) + 1) & 3) - 1  # Normalise to range -1 to 2


def find_corner(cube, f0, f1, f2):
    """
    Return a number from 0-23 that indicates where corner f0/f1/f2 is located
    """
    for (index, (corner0, corner1, corner2)) in enumerate((
            # UBR (2, 36, 29)
            (29, 2, 36),
            (36, 29, 2),
            (2, 36, 29),

            # ULB (0, 9, 38)
            (38, 0, 9),
            (9, 38, 0),
            (0, 9, 38),

            # UFL (6, 18, 11)
            (11, 6, 18),
            (18, 11, 6),
            (6, 18, 11),

            # URF (8, 27, 20)
            (20, 8, 27),
            (27, 20, 8),
            (8, 27, 20),

            # DLF (45, 17, 24)
            (24, 45, 17),
            (17, 24, 45),
            (45, 17, 24),

            # DBL (51, 44, 15)
            (15, 51, 44),
            (44, 15, 51),
            (51, 44, 15),

            # DRB (53, 35, 42)
            (42, 53, 35),
            (35, 42, 53),
            (53, 35, 42),

            # DFR (47, 26, 33)
            (33, 47, 26),
            (26, 33, 47),
            (47, 26, 33),
        )):

        if cube[corner0] == f0 and cube[corner1] == f1 and cube[corner2] == f2:
            return index

    raise Exception("Could not find corner f0/f1/f2 %s/%s/%s in\n%s\n" % (f0, f1, f2, cube2str(cube)))


def index_corner(cube, f0, f1, f2):
    assert isinstance(f0, int), "f0 is a %s, it must be an int" % type(f0)
    assert isinstance(f1, int), "f1 is a %s, it must be an int" % type(f1)
    assert isinstance(f2, int), "f2 is a %s, it must be an int" % type(f2)

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
    assert isinstance(f0, int), "f0 is a %s, it must be an int" % type(f0)
    assert isinstance(f1, int), "f1 is a %s, it must be an int" % type(f1)

    for (index, (edge0, edge1)) in enumerate((
            # UB
            (37, 1),
            (1, 37),

            # UL
            (10, 3),
            (3, 10),

            # UF
            (19, 7),
            (7, 19),

            # UR
            (28, 5),
            (5, 28),

            # LF
            (21, 14),
            (14, 21),

            # BL
            (12, 41),
            (41, 12),

            # DL
            (16, 48),
            (48, 16),

            # RB
            (39, 32),
            (32, 39),

            # DB
            (43, 52),
            (52, 43),

            # FR
            (30, 23),
            (23, 30),

            # DR
            (34, 50),
            (50, 34),

            # DF
            (25, 46),
            (46, 25),
        )):

        if cube[edge0] == f0 and cube[edge1] == f1:
            return index

    raise Exception("Could not find edge f0/f1 %s/%s\n%s" % (f0, f1, cube2str(cube)))


def index_edge(cube, f0, f1):
    assert isinstance(f0, int), "f0 is a %s, it must be an int" % type(f0)
    assert isinstance(f1, int), "f1 is a %s, it must be an int" % type(f1)
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


opposite = [D, B, U, F, L, R]

def add_mv(f, r):
    assert isinstance(f, int), "f is a %s, it must be an int" % type(f)
    assert isinstance(r, int), "r is a %s, it must be an int" % type(r)
    global mv_n
    i   = mv_n
    mrg = False

    while i > 0:
        i -= 1

        fi = mv_f[i]

        if f == fi:
            r += mv_r[i]
            r = RFIX(r)

            if r != 0:
                mv_r[i] = r
            else:
                mv_n -= 1

                while i < mv_n:
                    mv_f[i] = mv_f[i+1]
                    mv_r[i] = mv_r[i+1]
                    i += 1

            mrg = True
            break

        if opposite[f] != fi:
            break

    if not mrg:
        mv_f[mv_n] = f
        mv_r[mv_n] = RFIX(r)
        mv_n += 1


swaps_333 = {
 'B': (0, 30, 33, 36, 4, 5, 6, 7, 8, 9, 3, 11, 12, 2, 14, 15, 1, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 54, 31, 32, 53, 34, 35, 52, 43, 40, 37, 44, 41, 38, 45, 42, 39, 46, 47, 48, 49, 50, 51, 10, 13, 16),
 "B'": (0, 16, 13, 10, 4, 5, 6, 7, 8, 9, 52, 11, 12, 53, 14, 15, 54, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 1, 31, 32, 2, 34, 35, 3, 39, 42, 45, 38, 41, 44, 37, 40, 43, 46, 47, 48, 49, 50, 51, 36, 33, 30),
 'B2': (0, 54, 53, 52, 4, 5, 6, 7, 8, 9, 36, 11, 12, 33, 14, 15, 30, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 16, 31, 32, 13, 34, 35, 10, 45, 44, 43, 42, 41, 40, 39, 38, 37, 46, 47, 48, 49, 50, 51, 3, 2, 1),
 'D': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 43, 44, 45, 19, 20, 21, 22, 23, 24, 16, 17, 18, 28, 29, 30, 31, 32, 33, 25, 26, 27, 37, 38, 39, 40, 41, 42, 34, 35, 36, 52, 49, 46, 53, 50, 47, 54, 51, 48),
 "D'": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 25, 26, 27, 19, 20, 21, 22, 23, 24, 34, 35, 36, 28, 29, 30, 31, 32, 33, 43, 44, 45, 37, 38, 39, 40, 41, 42, 16, 17, 18, 48, 51, 54, 47, 50, 53, 46, 49, 52),
 'D2': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 34, 35, 36, 19, 20, 21, 22, 23, 24, 43, 44, 45, 28, 29, 30, 31, 32, 33, 16, 17, 18, 37, 38, 39, 40, 41, 42, 25, 26, 27, 54, 53, 52, 51, 50, 49, 48, 47, 46),
 'F': (0, 1, 2, 3, 4, 5, 6, 18, 15, 12, 10, 11, 46, 13, 14, 47, 16, 17, 48, 25, 22, 19, 26, 23, 20, 27, 24, 21, 7, 29, 30, 8, 32, 33, 9, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 34, 31, 28, 49, 50, 51, 52, 53, 54),
 "F'": (0, 1, 2, 3, 4, 5, 6, 28, 31, 34, 10, 11, 9, 13, 14, 8, 16, 17, 7, 21, 24, 27, 20, 23, 26, 19, 22, 25, 48, 29, 30, 47, 32, 33, 46, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 12, 15, 18, 49, 50, 51, 52, 53, 54),
 'F2': (0, 1, 2, 3, 4, 5, 6, 48, 47, 46, 10, 11, 34, 13, 14, 31, 16, 17, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 29, 30, 15, 32, 33, 12, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 9, 8, 7, 49, 50, 51, 52, 53, 54),
 'L': (0, 45, 2, 3, 42, 5, 6, 39, 8, 9, 16, 13, 10, 17, 14, 11, 18, 15, 12, 1, 20, 21, 4, 23, 24, 7, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 52, 40, 41, 49, 43, 44, 46, 19, 47, 48, 22, 50, 51, 25, 53, 54),
 "L'": (0, 19, 2, 3, 22, 5, 6, 25, 8, 9, 12, 15, 18, 11, 14, 17, 10, 13, 16, 46, 20, 21, 49, 23, 24, 52, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 7, 40, 41, 4, 43, 44, 1, 45, 47, 48, 42, 50, 51, 39, 53, 54),
 'L2': (0, 46, 2, 3, 49, 5, 6, 52, 8, 9, 18, 17, 16, 15, 14, 13, 12, 11, 10, 45, 20, 21, 42, 23, 24, 39, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 25, 40, 41, 22, 43, 44, 19, 1, 47, 48, 4, 50, 51, 7, 53, 54),
 'R': (0, 1, 2, 21, 4, 5, 24, 7, 8, 27, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 48, 22, 23, 51, 25, 26, 54, 34, 31, 28, 35, 32, 29, 36, 33, 30, 9, 38, 39, 6, 41, 42, 3, 44, 45, 46, 47, 43, 49, 50, 40, 52, 53, 37),
 "R'": (0, 1, 2, 43, 4, 5, 40, 7, 8, 37, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 3, 22, 23, 6, 25, 26, 9, 30, 33, 36, 29, 32, 35, 28, 31, 34, 54, 38, 39, 51, 41, 42, 48, 44, 45, 46, 47, 21, 49, 50, 24, 52, 53, 27),
 'R2': (0, 1, 2, 48, 4, 5, 51, 7, 8, 54, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 43, 22, 23, 40, 25, 26, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 38, 39, 24, 41, 42, 21, 44, 45, 46, 47, 3, 49, 50, 6, 52, 53, 9),
 'U': (0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 19, 20, 21, 13, 14, 15, 16, 17, 18, 28, 29, 30, 22, 23, 24, 25, 26, 27, 37, 38, 39, 31, 32, 33, 34, 35, 36, 10, 11, 12, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54),
 "U'": (0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 37, 38, 39, 13, 14, 15, 16, 17, 18, 10, 11, 12, 22, 23, 24, 25, 26, 27, 19, 20, 21, 31, 32, 33, 34, 35, 36, 28, 29, 30, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54),
 'U2': (0, 9, 8, 7, 6, 5, 4, 3, 2, 1, 28, 29, 30, 13, 14, 15, 16, 17, 18, 37, 38, 39, 22, 23, 24, 25, 26, 27, 10, 11, 12, 31, 32, 33, 34, 35, 36, 19, 20, 21, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54),
 'x': (0, 19, 20, 21, 22, 23, 24, 25, 26, 27, 12, 15, 18, 11, 14, 17, 10, 13, 16, 46, 47, 48, 49, 50, 51, 52, 53, 54, 34, 31, 28, 35, 32, 29, 36, 33, 30, 9, 8, 7, 6, 5, 4, 3, 2, 1, 45, 44, 43, 42, 41, 40, 39, 38, 37),
 "x'": (0, 45, 44, 43, 42, 41, 40, 39, 38, 37, 16, 13, 10, 17, 14, 11, 18, 15, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 30, 33, 36, 29, 32, 35, 28, 31, 34, 54, 53, 52, 51, 50, 49, 48, 47, 46, 19, 20, 21, 22, 23, 24, 25, 26, 27),
 'x2': (0, 46, 47, 48, 49, 50, 51, 52, 53, 54, 18, 17, 16, 15, 14, 13, 12, 11, 10, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 1, 2, 3, 4, 5, 6, 7, 8, 9),
 'y': (0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 10, 11, 12, 13, 14, 15, 16, 17, 18, 48, 51, 54, 47, 50, 53, 46, 49, 52),
 "y'": (0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 37, 38, 39, 40, 41, 42, 43, 44, 45, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 52, 49, 46, 53, 50, 47, 54, 51, 48),
 'y2': (0, 9, 8, 7, 6, 5, 4, 3, 2, 1, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 54, 53, 52, 51, 50, 49, 48, 47, 46),
 'z': (0, 16, 13, 10, 17, 14, 11, 18, 15, 12, 52, 49, 46, 53, 50, 47, 54, 51, 48, 25, 22, 19, 26, 23, 20, 27, 24, 21, 7, 4, 1, 8, 5, 2, 9, 6, 3, 39, 42, 45, 38, 41, 44, 37, 40, 43, 34, 31, 28, 35, 32, 29, 36, 33, 30),
 "z'": (0, 30, 33, 36, 29, 32, 35, 28, 31, 34, 3, 6, 9, 2, 5, 8, 1, 4, 7, 21, 24, 27, 20, 23, 26, 19, 22, 25, 48, 51, 54, 47, 50, 53, 46, 49, 52, 43, 40, 37, 44, 41, 38, 45, 42, 39, 12, 15, 18, 11, 14, 17, 10, 13, 16),
 'z2': (0, 54, 53, 52, 51, 50, 49, 48, 47, 46, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 45, 44, 43, 42, 41, 40, 39, 38, 37, 9, 8, 7, 6, 5, 4, 3, 2, 1)}

def rotate_333(cube, step):
    return [cube[x] for x in swaps_333[step]]


def rotate(cube, f, r):
    assert isinstance(f, int), "f is a %s, it must be an int" % type(f)
    assert isinstance(r, int), "r is a %s, it must be an int" % type(r)
    r &= 3

    # f is the face
    # r has to be 1/4 forward, 1/4 backward or 1/2 turn
    # log.info("rotate: f %s (%s), r %s" % (f, side2str[f], r))

    # f will be an int in 0..5, convert that to side name (U, L, etc)
    step = side2str[f]

    # r has to be 1/4 forward, 1/4 backward or 1/2 turn
    # FAIL: pass ' 2
    # BETTER (edges solved): pass 2 '
    # FAIL: ' pass 2
    # FAIL: ' 2 pass
    # FAIL: 2 ' pass
    # FAIL: 2 pass '

    if r == 1:
        #step += "'"
        #step += "2"
        pass
    elif r == 2:
        #step += "'"
        step += "2"
        #pass
    elif r == 3:
        step += "'"
        #step += "2"
        #pass
    else:
        raise Exception("rotate r '%s' is invalid" % r)

    solution.append(step)
    tmp_cube = [0] + cube
    cube = rotate_333(tmp_cube, step)
    cube = cube[1:]
    return cube


    '''
    if f == U:
        rot_edges(cube, r, B, 4, R, 0, F, 0, L, 0)
    elif f == F:
        rot_edges(cube, r, U, 4, R, 6, D, 0, L, 2)
    elif f == D:
        rot_edges(cube, r, F, 4, R, 4, B, 0, L, 4)
    elif f == B:
        rot_edges(cube, r, D, 4, R, 2, U, 0, L, 6)
    elif f == R:
        rot_edges(cube, r, U, 2, B, 2, D, 2, F, 2)
    elif f == L:
        rot_edges(cube, r, U, 6, F, 6, D, 6, B, 6)
    else:
        raise Exception("rotate() invalid f %s" % f)

    f *= 8

    if r == 1:
        p         = cube[f+7]
        cube[f+7] = cube[f+5]
        cube[f+5] = cube[f+3]
        cube[f+3] = cube[f+1]
        cube[f+1] = p
        p         = cube[f+6]
        cube[f+6] = cube[f+4]
        cube[f+4] = cube[f+2]
        cube[f+2] = cube[f]
        cube[f]   = p

    elif r == 2:
        p         = cube[f+1]
        cube[f+1] = cube[f+5]
        cube[f+5] = p
        p         = cube[f+3]
        cube[f+3] = cube[f+7]
        cube[f+7] = p
        p         = cube[f]
        cube[f]   = cube[f+4]
        cube[f+4] = p
        p         = cube[f+2]
        cube[f+2] = cube[f+6]
        cube[f+6] = p

    elif r == 3:
        p         = cube[f+1]
        cube[f+1] = cube[f+3]
        cube[f+3] = cube[f+5]
        cube[f+5] = cube[f+7]
        cube[f+7] = p
        p         = cube[f]
        cube[f]   = cube[f+2]
        cube[f+2] = cube[f+4]
        cube[f+4] = cube[f+6]
        cube[f+6] = p

    else:
        raise Exception("rotate r %s is invalid" % r)
    '''


def solve_phase(cube, mtb, mtd, dorot=True):
    global idx
    sz = len(mtd) / mtb
    idx = sz - idx

    #print(cube2str(cube))
    #sys.exit(0)
    expected = """
        0 0 0
        0 0 0
        0 0 0

 5 5 5  1 1 1  4 4 4  3 3 3
 5 5 5  1 1 1  4 4 4  3 3 3
 5 5 5  1 1 1  4 4 4  3 3 3

        2 2 2
        2 2 2
        2 2 2
"""

    # assert cube2str(cube) == expected, "'%s' != '%s'" % (cube2str(cube), expected)
    log.info("solve_phase: mtb %s, len(mtd) %s, dorot %s, sz %s, idx %s" % (mtb, len(mtd), dorot, sz, idx))

    if idx > 0:
        i = int((idx - 1) * mtb)
        b = mtd[i]
        i += 1

        if b != 0xFF:
            mvm = mtb * 2 - 1
            mv = 0
            f0 = int(b / 3)
            r0 = RFIX(b - (f0 * 3) + 1)
            add_mv(f0, r0)

            if dorot:
                cube = rotate(cube, f0, r0)

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
                add_mv(f0, r0)

                if dorot:
                    cube = rotate(cube, f0, r0)

                mv += 1
    return cube


def solve_one(cube, dorot):
    print("INIT CUBE:\n%s" % (cube2str(cube)))

    # phase 1 - solve edges DF DR
    index_init()
    index_edge(cube, D, F)
    index_edge(cube, D, R)
    cube = solve_phase(cube, mtb0, mtd0)

    # phase 2 - solve corner DFR and edge FR
    index_init()
    index_corner(cube, D, F, R)
    index_edge(cube, F, R)
    cube = solve_phase(cube, mtb1, mtd1)

    # phase 3 - solve edge DB
    index_init()
    index_edge(cube, D, B)
    cube = solve_phase(cube, mtb2, mtd2)

    # phase 4 - solve corner DRB and edge RB
    index_init()
    index_corner(cube, D, R, B)
    index_edge(cube, R, B)
    cube = solve_phase(cube, mtb3, mtd3)

    # phase 5 - solve edge DL
    index_init()
    index_edge(cube, D, L)
    cube = solve_phase(cube, mtb4, mtd4)

    # phase 6 - solve corner DBL and edge BL
    index_init()
    index_corner(cube, D, B, L)
    index_edge(cube, B, L)
    cube = solve_phase(cube, mtb5, mtd5)

    # phase 7 - solve corner DLF and edge LF
    index_init()
    index_corner(cube, D, L, F)
    index_edge(cube, L, F)
    cube = solve_phase(cube, mtb6, mtd6)

    # phase 8 - solve corners URF, UFL, and ULB
    index_init()
    index_corner(cube, U, R, F)
    index_corner(cube, U, F, L)
    index_corner(cube, U, L, B)
    cube = solve_phase(cube, mtb7, mtd7)

    # phase 9 - solve edges UR, UF and UL
    index_init()
    index_edge(cube, U, R)
    index_edge(cube, U, F)
    index_edge(cube, U, L)
    index_last()
    cube = solve_phase(cube, mtb8, mtd8, dorot)

    print("FINAL CUBE:\n%s" % (cube2str(cube)))


class RubiksCube333(object):

    def __init__(self, state, order):
        self.solution = []
        foo = []
        state = list(state)
        squares_per_side = 9

        if order == 'URFDLB':
            foo.extend(state[0:squares_per_side])                            # U
            foo.extend(state[(squares_per_side * 4):(squares_per_side * 5)]) # L
            foo.extend(state[(squares_per_side * 2):(squares_per_side * 3)]) # F
            foo.extend(state[(squares_per_side * 1):(squares_per_side * 2)]) # R
            foo.extend(state[(squares_per_side * 5):(squares_per_side * 6)]) # B
            foo.extend(state[(squares_per_side * 3):(squares_per_side * 4)]) # D
        elif order == 'ULFRBD':
            foo.extend(state[0:squares_per_side])                            # U
            foo.extend(state[(squares_per_side * 1):(squares_per_side * 2)]) # L
            foo.extend(state[(squares_per_side * 2):(squares_per_side * 3)]) # F
            foo.extend(state[(squares_per_side * 3):(squares_per_side * 4)]) # R
            foo.extend(state[(squares_per_side * 4):(squares_per_side * 5)]) # B
            foo.extend(state[(squares_per_side * 5):(squares_per_side * 6)]) # D
        else:
            raise Exception("Add support for order %s" % order)

        self.state = []

        for x in foo:
            if x == "U":
                self.state.append(U)
            elif x == "L":
                self.state.append(L)
            elif x == "F":
                self.state.append(F)
            elif x == "R":
                self.state.append(R)
            elif x == "B":
                self.state.append(B)
            elif x == "D":
                self.state.append(D)

    def solve(self):
        solve_one(self.state, True)
        self.solution = solution
