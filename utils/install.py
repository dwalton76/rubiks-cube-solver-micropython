#!/usr/bin/env python3

import argparse
import logging
import os
import subprocess
import sys

files = (
    "__init__.py",
    "cube.py",
    "LookupTable.py",
    "profile.py",
    "lookup-table-3x3x3-step110.txt",
    "lookup-table-3x3x3-step120.txt",
    "lookup-table-3x3x3-step121-edges.txt",
    "lookup-table-3x3x3-step122-corners.txt",
    "lookup-table-3x3x3-step130.txt",
    "lookup-table-3x3x3-step131-edges.txt",
    "lookup-table-3x3x3-step132-corners.txt",
    "lookup-table-3x3x3-step140.txt",
    "lookup-table-3x3x3-step141-edges.txt",
    "lookup-table-3x3x3-step142-corners.txt",
)


def sizeof_human_readable(num: int, suffix: str ='') -> str:
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def install_rubiks_cube_solver(dev: str) -> bool:

    # ampy requires root perms
    if os.geteuid() != 0:
        log.error("You must run this program using 'sudo'")
        return False

    if not os.path.exists(dev):
        log.error(f"device '{dev}' is not connected")
        return False

    dirname = "rubikscubesolvermicropython"

    '''
    try:
        with open(os.devnull, 'w'):
            subprocess.call(f"ampy --port /dev/ttyACM0 mkdir {dirname}", shell=True)
    except Exception:
        pass
    '''

    current_files = sorted(subprocess.check_output(f"ampy --port {dev} ls {dirname}", shell=True).decode("utf-8").splitlines())

    if current_files:
        log.info("current files\n\n    {}\n".format("\n    ".join(current_files)))

    for filename in files:
        local_filename = f"{dirname}/{filename}"
        dest_filename = f"/{dirname}/{filename}"
        filesize = sizeof_human_readable(os.path.getsize(local_filename))
        
        if dest_filename not in current_files:
            log.info(f"TX {filesize} {filename}")
            subprocess.call(f"ampy --port /dev/ttyACM0 put {local_filename} {dest_filename}", shell=True)
        else:
            log.info(f"{filesize} {filename} already on device")

    return True


if __name__ == "__main__":

    # configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(filename)16s %(levelname)8s: %(message)s"
    )
    log = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", type=str, default="/dev/ttyACM0", help="/dev/ttyXXXXX of SPIKE")
    args = parser.parse_args()

    if not install_rubiks_cube_solver(args.dev):
        sys.exit(1)
