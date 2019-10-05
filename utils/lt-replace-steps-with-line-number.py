#!/usr/bin/env python3

"""
For a lookup-table of state:steps entries, replace the steps with the line number
for this state.  We will use this later to find the 'index' for a state.
"""

import os
import sys
import subprocess

filename = sys.argv[1]
filename_new = filename + ".new"

to_write = []

with open(filename, "r") as fh:
    for (line_number, line) in enumerate(fh):
        (state, steps) = line.strip().split(":")
        to_write.append(f"{state}:{line_number}")

with open(filename_new, "w") as fh:
    fh.write("\n".join(to_write) + "\n")

subprocess.call(["./utils/pad-lines.py", filename_new])
os.rename(filename_new, filename)
