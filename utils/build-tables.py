#!/usr/bin/env micropython

"""
Used this to build some data structures needed for the 3x3x3 4-phase solver
"""

from rubikscubesolvermicropython.cube import RubiksCube333, cube2strcolor, cube2str
import logging
import urandom
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)22s %(levelname)8s: %(message)s')
log = logging.getLogger(__name__)

EDGE_TUPLES = (
    (2, 38), (38, 2),
    (4, 11), (11, 4),
    (6, 29), (29, 6),
    (8, 20), (20, 8),
    (13, 42), (42, 13),
    (15, 22), (22, 15),
    (31, 24), (24, 31),
    (33, 40), (40, 33),
    (47, 26), (26, 47),
    (49, 17), (17, 49),
    (51, 35), (35, 51),
    (53, 44), (44, 53),
)

CORNER_TUPLES = (
    (1, 10, 39), (39, 1, 10), (10, 39, 1),
    (3, 37, 30), (30, 3, 37), (37, 30, 3),
    (7, 19, 12), (12, 7, 19), (19, 12, 7),
    (9, 28, 21), (21, 9, 28), (28, 21, 9),
    (46, 18, 25), (25, 46, 18), (18, 25, 46),
    (48, 27, 34), (34, 48, 27), (27, 34, 48),
    (52, 45, 16), (16, 52, 45), (45, 16, 52),
    (54, 36, 43), (43, 54, 36), (36, 43, 54),
)

EDGE_COLORS = (
    "UB", "UL", "UR", "UF",
    "LB", "LF", "RB", "RF",
    "DB", "DL", "DR", "DF",
)

CORNER_COLORS = (
    "ULB", "UBR", "UFL", "URF",
    "DLF", "DFR", "DBL", "DRB",
)

moves_333 = (
    "U", "U'", "U2",
    "L", "L'", "L2",
    "F", "F'", "F2",
    "R", "R'", "R2",
    "B", "B'", "B2",
    "D", "D'", "D2",
)


def nuke_corners(cube, corner_to_keep=None):
    for (c0, c1, c2) in CORNER_TUPLES:
        corner_str0 = cube.state[c0] + cube.state[c1] + cube.state[c2]
        corner_str1 = cube.state[c2] + cube.state[c0] + cube.state[c1]
        corner_str2 = cube.state[c1] + cube.state[c2] + cube.state[c0]

        if corner_to_keep is None or corner_to_keep not in (corner_str0, corner_str1, corner_str2):
            cube.state[c0] = "x"
            cube.state[c1] = "x"
            cube.state[c2] = "x"


def nuke_edges(cube, edge_to_keep=None):
    for (e0, e1) in EDGE_TUPLES:
        edge_str = cube.state[e0] + cube.state[e1]
        edge_str_rev = cube.state[e1] + cube.state[e0]

        if edge_to_keep is None or (edge_str != edge_to_keep and edge_str_rev != edge_to_keep):
            cube.state[e0] = "x"
            cube.state[e1] = "x"


def get_edge_location(cube, target_edge):
    for (e0, e1) in EDGE_TUPLES:
        edge_str = cube.state[e0] + cube.state[e1]

        if edge_str == target_edge:
            return (e0, e1)

    print(cube2strcolor(cube.state))
    raise Exception("Could not find {}".format(edge_color))


def get_corner_location(cube, target_corner):
    for (c0, c1, c2) in CORNER_TUPLES:
        corner_str = cube.state[c0] + cube.state[c1] + cube.state[c2]

        if corner_str == target_corner:
            return (c0, c1, c2)

    print(cube2strcolor(cube.state))
    raise Exception("Could not find {}".format(corner_color))


def get_all_positions(illegal_moves, target_edge=None, target_corner=None):
    assert target_edge is not None or target_corner is not None

    legal_moves = []
    for move in moves_333:
        if move not in illegal_moves:
            legal_moves.append(move)

    legal_moves = tuple(legal_moves)
    legal_move_count = len(legal_moves)
    # print("legal moves {}".format(legal_moves))
    # print("get_all_positions target_edge {}, target_corner {}".format(target_edge, target_corner))

    result = set()

    for x in range(3000):
        index = urandom.getrandbits(8) % legal_move_count
        step = legal_moves[index]
        cube.rotate(step)

        if target_edge:
            location = get_edge_location(cube, target_edge)
        else:
            location = get_corner_location(cube, target_corner)

        result.add(location)
        #print(step)
        #print(cube2strcolor(cube.state))

    result = tuple(sorted(list(result)))

    '''
    if target_edge:
        print("edge {} found {} entries\n{}".format(target_edge, len(result), result))
    elif target_corner:
        print("corner {} found {} entries\n{}".format(target_corner, len(result), result))
    '''

    return result



def get_states_for_illegal_moves(illegal_moves):
    edge_states = {}
    corner_states = {}

    for edge_color in EDGE_COLORS:
        nuke_corners(cube)
        nuke_edges(cube, edge_color)

        for (e0, e1) in get_all_positions(illegal_moves, edge_color, None):
            if (e0, e1) not in edge_states:
                edge_states[(e0, e1)] = []
            edge_states[(e0, e1)].append(edge_color)

        cube.re_init()
    edge_color = None

    for corner_color in CORNER_COLORS:
        nuke_corners(cube, corner_color)
        nuke_edges(cube)

        for (c0, c1, c2) in get_all_positions(illegal_moves, None, corner_color):
            if (c0, c1, c2) not in corner_states:
                corner_states[(c0, c1, c2)] = []
            corner_states[(c0, c1, c2)].append(corner_color)

        cube.re_init()
    corner_color = None

    return (edge_states, corner_states)


if __name__ == "__main__":
    cube = RubiksCube333("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB", "URFDLB")
    #nuke_corners(cube)
    #nuke_edges(cube)
    #print(cube2str(cube.state))

    illegal_moves = ("L", "L'", "R", "R'")
    (phase1_edge_states, phase1_corner_states) = get_states_for_illegal_moves(illegal_moves)
    print("phase1_edge_states = \n{}\n".format(phase1_edge_states))
    print("phase1_corner_states = \n{}\n".format(phase1_corner_states))

    illegal_moves = ("L", "L'", "R", "R'", "F", "F'", "B", "B'")
    (phase2_edge_states, phase2_corner_states) = get_states_for_illegal_moves(illegal_moves)
    print("phase2_edge_states = \n{}\n".format(phase2_edge_states))
    print("phase2_corner_states = \n{}\n".format(phase2_corner_states))

    illegal_moves = ("L", "L'", "R", "R'", "F", "F'", "B", "B'", "U", "U'", "D", "D'")
    (phase3_edge_states, phase3_corner_states) = get_states_for_illegal_moves(illegal_moves)
    print("phase3_edge_states = \n{}\n".format(phase3_edge_states))
    print("phase3_corner_states = \n{}\n".format(phase3_corner_states))
