# rubiks-cube-solver-micropython
A 3x3x3 solver in micropython designed for devices with minimal memory.

Install
```
sudo mkdir /usr/lib/micropython/rubikscubesolvermicropython/
sudo cp rubikscubesolvermicropython/*.py /usr/lib/micropython/rubikscubesolvermicropython/
sudo cp rubikscubesolvermicropython/*.txt /usr/lib/micropython/rubikscubesolvermicropython/
```

Example:
```
micropython ./usr/bin/solver.py UFRUUDRLFLBUFRUDLBDFUFFDBBBRRRDDBFLDLBFDLRLRUFUBRBLLUD
```

The `UFRUUDR...` string is a representation of the state of each of
the 54 squares of a 3x3x3 cube. The U at the beginning means that square #1 is
the same color as the middle square of the Up side (the top), the F means that
square #2 is the same color as the middle square of the Front side, etc. The
solver takes cube state and returns a sequence of moves that can be used to
solve the cube.
