#!/usr/bin/env micropython

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

with open("mtd0.txt", "w") as fh:
    for x in mtd0:
        fh.write("0x%02X\n" % x)

with open("mtd1.txt", "w") as fh:
    for x in mtd1:
        fh.write("0x%02X\n" % x)

with open("mtd2.txt", "w") as fh:
    for x in mtd2:
        fh.write("0x%02X\n" % x)

with open("mtd3.txt", "w") as fh:
    for x in mtd3:
        fh.write("0x%02X\n" % x)

with open("mtd4.txt", "w") as fh:
    for x in mtd4:
        fh.write("0x%02X\n" % x)

with open("mtd5.txt", "w") as fh:
    for x in mtd5:
        fh.write("0x%02X\n" % x)

with open("mtd6.txt", "w") as fh:
    for x in mtd6:
        fh.write("0x%02X\n" % x)

with open("mtd7.txt", "w") as fh:
    for x in mtd7:
        fh.write("0x%02X\n" % x)

with open("mtd8.txt", "w") as fh:
    for x in mtd8:
        fh.write("0x%02X\n" % x)
