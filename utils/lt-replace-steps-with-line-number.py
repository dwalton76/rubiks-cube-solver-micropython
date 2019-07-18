#!/usr/bin/env python3

import sys

filename = sys.argv[1]
filename_new = filename + ".new"

to_write = []

with open(filename, "r") as fh:
    for (line_number, line) in enumerate(fh):
        (state, steps) = line.strip().split(":")
        to_write.append(f"{state}:{line_number}")

with open(filename_new, "w") as fh:
    fh.write("\n".join(to_write) + "\n")
