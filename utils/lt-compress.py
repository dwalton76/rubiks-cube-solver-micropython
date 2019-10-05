#!/usr/bin/env python3

"""
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
table to 2.7M and the phase4 table to 649K.
"""

import argparse
import os
import logging
import subprocess
import sys

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


def get_edge_corner_index(edges, corners, state):
    state_edges = []
    state_corners = []

    for (index, square_state) in enumerate(state):
        if index + 1 in CORNERS:
            state_corners.append(square_state)
        elif index + 1 in EDGES:
            state_edges.append(square_state)

    state_edges = "".join(state_edges)
    state_corners = "".join(state_corners)
    edges_index = edges[state_edges]
    corners_index = corners[state_corners]

    '''
    log.info(f"state: {state}")
    log.info(f"state_edges: {state_edges}")
    log.info(f"state_corners: {state_corners}")
    log.info(f"edges_index: {edges_index}")
    log.info(f"corners_index: {corners_index}")
    sys.exit(0)
    '''
    return (edges_index, corners_index)


def lookup_table_compress(filename_main, filename_edges, filename_corners):
    edges = {}
    corners = {}

    with open(filename_edges, "r") as fh:
        for line in fh:
            (state, index) = line.strip().split(":")
            edges[state] = int(index)

    with open(filename_corners, "r") as fh:
        for line in fh:
            (state, index) = line.strip().split(":")
            corners[state] = int(index)

    edges_count = len(edges.keys())
    corners_count = len(corners.keys())
    to_write = [None] * (edges_count * corners_count)
    print(f"edges_count {edges_count}, corners_count {corners_count}, to_write {len(to_write)}")

    step_to_char = {
        ""   : '0',
        "U"  : '1',
        "U'" : '2',
        "U2" : '3',
        "L"  : '4',
        "L'" : '5',
        "L2" : '6',
        "F"  : '7',
        "F'" : '8',
        "F2" : '9',
        "R"  : 'a',
        "R'" : 'b',
        "R2" : 'c',
        "B"  : 'd',
        "B'" : 'e',
        "B2" : 'f',
        "D"  : 'g',
        "D'" : 'h',
        "D2" : 'i',
    }

    with open(filename_main, "r") as fh:
        for line in fh:
            (state, steps) = line.strip().split(":")
            (edge_index, corner_index) = get_edge_corner_index(edges, corners, state)
            main_index = (edge_index * corners_count) + corner_index

            try:
                if steps:
                    step = steps.split()[0]
                else:
                    step = ""
            except IndexError:
                log.info(f"steps {steps}")
                log.info(f"edge_index {edge_index}, corner_index {corner_index}, main_index {main_index}")
                raise

            # Store the step via a single character to save space
            to_write[main_index] = step_to_char[step]

    assert None not in to_write

    filename_main_new = filename_main + ".new"
    with open(filename_main_new, "w") as fh:
        fh.write("".join(to_write))

    subprocess.call(["./utils/pad-lines.py", filename_main_new])
    os.rename(filename_main_new, filename_main)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(filename)22s %(levelname)8s: %(message)s")
    log = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("--main", type=str, help="main lookup table filename")
    parser.add_argument("--edges", type=str, help="edges lookup table filename")
    parser.add_argument("--corners", type=str, help="corners lookup table filename")
    args = parser.parse_args()

    lookup_table_compress(args.main, args.edges, args.corners)
