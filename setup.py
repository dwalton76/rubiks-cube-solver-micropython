
import sys
from distutils.core import setup, Extension

setup(
    name='rubikscubesolvermicropython',
    version='1.0.0',
    description='3x3x3 rubiks cube solver',
    keywords='rubiks cube solver micropython',
    url='https://github.com/dwalton76/rubiks-cube-solver-micropython',
    author='Daniel Walton',
    author_email='dwalton76@gmail.com',
    license='GPLv3',
    scripts=['usr/bin/solver.py'],
    packages=['rubikscubesolvermicropython'],
)

