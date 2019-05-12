

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

#-----------------------------------------------------------------------------
# Face indices
#-----------------------------------------------------------------------------
U = 0
F = 1
D = 2
B = 3
R = 4
L = 5


idx_nc = 0
idx_ne = 0
idx = 0

def index_init():
    global idx_nc, idx_ne, idx
    idx_nc = 0
    idx_ne = 0
    idx = 0


def POS(FF, OO):
    return (FF * 8) + OO


def FIND_CORNER(cube, f0, f1, f2, F0, O0, F1, O1, F2, O2, I0, I1, I2):
    c0 = cube[POS(F0, O0)]

    if c0 == f0:
        if cube[POS(F1, O1)] == f1 and cube[POS(F2, O2)] == f2:
            return I2

    elif c0 == f2:
        if cube[POS(F1, O1)] == f0 and cube[POS(F2, O2)] == f1:
            return I1

    elif c0 == f1:
        if cube[POS(F1, O1)] == f2 and cube[POS(F2, O2)] == f0:
            return I0

    return None


def find_corner(cube, f0, f1, f2):

    corner = FIND_CORNER(f0, f1, f2, U, 2, B, 4, R, 2, 0,  1,  2)

    if corner is not None:
        return corner

    corner = FIND_CORNER(f0, f1, f2, U, 0, L, 0, B, 6, 3,  4,  5)

    if corner is not None:
        return corner

    corner = FIND_CORNER(f0, f1, f2, U, 6, F, 0, L, 2, 6,  7,  8)

    if corner is not None:
        return corner

    corner = FIND_CORNER(f0, f1, f2, U, 4, R, 0, F, 2, 9,  10, 11)

    if corner is not None:
        return corner

    corner = FIND_CORNER(f0, f1, f2, D, 0, L, 4, F, 6, 12, 13, 14)

    if corner is not None:
        return corner

    corner = FIND_CORNER(f0, f1, f2, D, 6, B, 0, L, 6, 15, 16, 17)

    if corner is not None:
        return corner

    corner = FIND_CORNER(f0, f1, f2, D, 4, R, 4, B, 2, 18, 19, 20)

    if corner is not None:
        return corner

    corner = FIND_CORNER(f0, f1, f2, D, 2, F, 4, R, 6, 21, 22, 23)
    return corner


def index_corner(cube, f0, f1, f2):
    ic = find_corner(cube, f0, f1, f2)

    for i in range(idx_nc):
        if ic > idx_idx[i]:
            ic -= 3;

    idx = (idx * idx_ic) + ic
    idx_idx[idx_nc] = ic
    idx_nc += 1
    idx_ic -= 3


'''
int index_corner(byte &cube[], byte f0, byte f1, byte f2) {
  int ic = find_corner(cube, f0, f1, f2);
  for (int i = 0; i < idx_nc; i++) {
    if (ic > idx_idx[i])
      ic -= 3;
  }
  idx = (idx*idx_ic) + ic;
  idx_idx[idx_nc++] = ic;
  idx_ic -= 3;
}


#define FIND_EDGE(F0, O0, F1, O1, I0, I1) \
  e0 = cube[POS(F0, O0)]; \
  if (e0 == f0) { \
    if (cube[POS(F1, O1)] == f1) return I1; \
  } else if (e0 == f1) { \
    if (cube[POS(F1, O1)] == f0) return I0; \
  }

int find_edge(byte &cube[], byte f0, byte f1) {
  byte e0;
  FIND_EDGE(U, 1, B, 5, 0,  1);
  FIND_EDGE(U, 7, L, 1, 2,  3);
  FIND_EDGE(U, 5, F, 1, 4,  5);
  FIND_EDGE(U, 3, R, 1, 6,  7);
  FIND_EDGE(L, 3, F, 7, 8,  9);
  FIND_EDGE(B, 7, L, 7, 10, 11);
  FIND_EDGE(D, 7, L, 5, 12, 13);
  FIND_EDGE(R, 3, B, 3, 14, 15);
  FIND_EDGE(D, 5, B, 1, 16, 17);
  FIND_EDGE(F, 3, R, 7, 18, 19);
  FIND_EDGE(D, 3, R, 5, 20, 21);
  FIND_EDGE(D, 1, F, 5, 22, 23);
  return -1;
}

void index_edge(byte &cube[], byte f0, byte f1) {
  int ie = find_edge(cube, f0, f1);
  for (int i = 0; i < idx_ne; i++) {
    if (ie > idx_idx[i])
      ie -= 2;
  }
  idx = (idx*idx_ie) + ie;
  idx_idx[idx_ne++] = ie;
  idx_ie -= 2;
}



void solve_phase(byte &cube[], int mtb, const byte &mtd[], bool dorot = true) {
  int sz = ArrayLen(mtd)/mtb;
  idx = sz-idx;

  if (idx > 0) {
    int i = (idx-1)*mtb;
    byte b = mtd[i++];

    if (b != 0xFF) {
      const int mvm = mtb*2-1;
      int mv = 0;
      int f0 = b / 3;
      int r0 = RFIX(b-(f0*3)+1);
      add_mv(f0, r0);

      if (dorot)
        rotate(cube, f0, r0);

      mv ++;
      while (mv < mvm) {
        b >>= 4;

        if ((mv & 1) != 0)
          b = mtd[i++];

        byte b0 = b & 0xF;

        if (b0 == 0xF)
          break;

        int f1 = b0 / 3;
        r0 = RFIX(b0-(f1*3)+1);

        if (f1 >= f0)
          f1 ++;

        f0 = f1;
        add_mv(f0, r0);

        if (dorot)
          rotate(cube, f0, r0);

        mv ++;
      }
    }
  }
}


void solve_one(byte &cube[], bool dorot) {
  mv_n = 0;
  idx_ic = 24;
  idx_ie = 24;

  index_init();
  index_edge(cube, D, F);
  index_edge(cube, D, R);
  solve_phase(cube, mtb0, mtd0);

  index_init();
  index_corner(cube, D, F, R);
  index_edge(cube, F, R);
  solve_phase(cube, mtb1, mtd1);

  index_init();
  index_edge(cube, D, B);
  solve_phase(cube, mtb2, mtd2);

  index_init();
  index_corner(cube, D, R, B);
  index_edge(cube, R, B);
  solve_phase(cube, mtb3, mtd3);

  index_init();
  index_edge(cube, D, L);
  solve_phase(cube, mtb4, mtd4);

  index_init();
  index_corner(cube, D, B, L);
  index_edge(cube, B, L);
  solve_phase(cube, mtb5, mtd5);

  index_init();
  index_corner(cube, D, L, F);
  index_edge(cube, L, F);
  solve_phase(cube, mtb6, mtd6);

  index_init();
  index_corner(cube, U, R, F);
  index_corner(cube, U, F, L);
  index_corner(cube, U, L, B);
  solve_phase(cube, mtb7, mtd7);

  index_init();
  index_edge(cube, U, R);
  index_edge(cube, U, F);
  index_edge(cube, U, L);
  index_last();
  solve_phase(cube, mtb8, mtd8, dorot);
}
'''


class RubiksCube333(object):

    def __init__(self, state):
        self.state = list(state)
        self.solution = []

    def solve(self):
        pass

