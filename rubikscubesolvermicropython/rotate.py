# n is new
# o is old
def rotate_B(o, n):
    n[0] = o[29]
    n[1] = o[32]
    n[2] = o[35]
    n[9] = o[2]
    n[12] = o[1]
    n[15] = o[0]
    n[29] = o[53]
    n[32] = o[52]
    n[35] = o[51]
    n[36] = o[42]
    n[37] = o[39]
    n[38] = o[36]
    n[39] = o[43]
    n[41] = o[37]
    n[42] = o[44]
    n[43] = o[41]
    n[44] = o[38]
    n[51] = o[9]
    n[52] = o[12]
    n[53] = o[15]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[9] = n[9]
    o[12] = n[12]
    o[15] = n[15]
    o[29] = n[29]
    o[32] = n[32]
    o[35] = n[35]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]
    o[39] = n[39]
    o[41] = n[41]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_B_prime(o, n):
    n[0] = o[15]
    n[1] = o[12]
    n[2] = o[9]
    n[9] = o[51]
    n[12] = o[52]
    n[15] = o[53]
    n[29] = o[0]
    n[32] = o[1]
    n[35] = o[2]
    n[36] = o[38]
    n[37] = o[41]
    n[38] = o[44]
    n[39] = o[37]
    n[41] = o[43]
    n[42] = o[36]
    n[43] = o[39]
    n[44] = o[42]
    n[51] = o[35]
    n[52] = o[32]
    n[53] = o[29]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[9] = n[9]
    o[12] = n[12]
    o[15] = n[15]
    o[29] = n[29]
    o[32] = n[32]
    o[35] = n[35]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]
    o[39] = n[39]
    o[41] = n[41]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_B2(o, n):
    n[0] = o[53]
    n[1] = o[52]
    n[2] = o[51]
    n[9] = o[35]
    n[12] = o[32]
    n[15] = o[29]
    n[29] = o[15]
    n[32] = o[12]
    n[35] = o[9]
    n[36] = o[44]
    n[37] = o[43]
    n[38] = o[42]
    n[39] = o[41]
    n[41] = o[39]
    n[42] = o[38]
    n[43] = o[37]
    n[44] = o[36]
    n[51] = o[2]
    n[52] = o[1]
    n[53] = o[0]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[9] = n[9]
    o[12] = n[12]
    o[15] = n[15]
    o[29] = n[29]
    o[32] = n[32]
    o[35] = n[35]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]
    o[39] = n[39]
    o[41] = n[41]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_D(o, n):
    n[15] = o[42]
    n[16] = o[43]
    n[17] = o[44]
    n[24] = o[15]
    n[25] = o[16]
    n[26] = o[17]
    n[33] = o[24]
    n[34] = o[25]
    n[35] = o[26]
    n[42] = o[33]
    n[43] = o[34]
    n[44] = o[35]
    n[45] = o[51]
    n[46] = o[48]
    n[47] = o[45]
    n[48] = o[52]
    n[50] = o[46]
    n[51] = o[53]
    n[52] = o[50]
    n[53] = o[47]

    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]
    o[48] = n[48]
    o[50] = n[50]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_D_prime(o, n):
    n[15] = o[24]
    n[16] = o[25]
    n[17] = o[26]
    n[24] = o[33]
    n[25] = o[34]
    n[26] = o[35]
    n[33] = o[42]
    n[34] = o[43]
    n[35] = o[44]
    n[42] = o[15]
    n[43] = o[16]
    n[44] = o[17]
    n[45] = o[47]
    n[46] = o[50]
    n[47] = o[53]
    n[48] = o[46]
    n[50] = o[52]
    n[51] = o[45]
    n[52] = o[48]
    n[53] = o[51]

    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]
    o[48] = n[48]
    o[50] = n[50]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_D2(o, n):
    n[15] = o[33]
    n[16] = o[34]
    n[17] = o[35]
    n[24] = o[42]
    n[25] = o[43]
    n[26] = o[44]
    n[33] = o[15]
    n[34] = o[16]
    n[35] = o[17]
    n[42] = o[24]
    n[43] = o[25]
    n[44] = o[26]
    n[45] = o[53]
    n[46] = o[52]
    n[47] = o[51]
    n[48] = o[50]
    n[50] = o[48]
    n[51] = o[47]
    n[52] = o[46]
    n[53] = o[45]

    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]
    o[48] = n[48]
    o[50] = n[50]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_F(o, n):
    n[6] = o[17]
    n[7] = o[14]
    n[8] = o[11]
    n[11] = o[45]
    n[14] = o[46]
    n[17] = o[47]
    n[18] = o[24]
    n[19] = o[21]
    n[20] = o[18]
    n[21] = o[25]
    n[23] = o[19]
    n[24] = o[26]
    n[25] = o[23]
    n[26] = o[20]
    n[27] = o[6]
    n[30] = o[7]
    n[33] = o[8]
    n[45] = o[33]
    n[46] = o[30]
    n[47] = o[27]

    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[11] = n[11]
    o[14] = n[14]
    o[17] = n[17]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[21] = n[21]
    o[23] = n[23]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[27] = n[27]
    o[30] = n[30]
    o[33] = n[33]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]


def rotate_F_prime(o, n):
    n[6] = o[27]
    n[7] = o[30]
    n[8] = o[33]
    n[11] = o[8]
    n[14] = o[7]
    n[17] = o[6]
    n[18] = o[20]
    n[19] = o[23]
    n[20] = o[26]
    n[21] = o[19]
    n[23] = o[25]
    n[24] = o[18]
    n[25] = o[21]
    n[26] = o[24]
    n[27] = o[47]
    n[30] = o[46]
    n[33] = o[45]
    n[45] = o[11]
    n[46] = o[14]
    n[47] = o[17]

    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[11] = n[11]
    o[14] = n[14]
    o[17] = n[17]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[21] = n[21]
    o[23] = n[23]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[27] = n[27]
    o[30] = n[30]
    o[33] = n[33]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]


def rotate_F2(o, n):
    n[6] = o[47]
    n[7] = o[46]
    n[8] = o[45]
    n[11] = o[33]
    n[14] = o[30]
    n[17] = o[27]
    n[18] = o[26]
    n[19] = o[25]
    n[20] = o[24]
    n[21] = o[23]
    n[23] = o[21]
    n[24] = o[20]
    n[25] = o[19]
    n[26] = o[18]
    n[27] = o[17]
    n[30] = o[14]
    n[33] = o[11]
    n[45] = o[8]
    n[46] = o[7]
    n[47] = o[6]

    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[11] = n[11]
    o[14] = n[14]
    o[17] = n[17]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[21] = n[21]
    o[23] = n[23]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[27] = n[27]
    o[30] = n[30]
    o[33] = n[33]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]


def rotate_L(o, n):
    n[0] = o[44]
    n[3] = o[41]
    n[6] = o[38]
    n[9] = o[15]
    n[10] = o[12]
    n[11] = o[9]
    n[12] = o[16]
    n[14] = o[10]
    n[15] = o[17]
    n[16] = o[14]
    n[17] = o[11]
    n[18] = o[0]
    n[21] = o[3]
    n[24] = o[6]
    n[38] = o[51]
    n[41] = o[48]
    n[44] = o[45]
    n[45] = o[18]
    n[48] = o[21]
    n[51] = o[24]

    o[0] = n[0]
    o[3] = n[3]
    o[6] = n[6]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[12] = n[12]
    o[14] = n[14]
    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[18] = n[18]
    o[21] = n[21]
    o[24] = n[24]
    o[38] = n[38]
    o[41] = n[41]
    o[44] = n[44]
    o[45] = n[45]
    o[48] = n[48]
    o[51] = n[51]


def rotate_L_prime(o, n):
    n[0] = o[18]
    n[3] = o[21]
    n[6] = o[24]
    n[9] = o[11]
    n[10] = o[14]
    n[11] = o[17]
    n[12] = o[10]
    n[14] = o[16]
    n[15] = o[9]
    n[16] = o[12]
    n[17] = o[15]
    n[18] = o[45]
    n[21] = o[48]
    n[24] = o[51]
    n[38] = o[6]
    n[41] = o[3]
    n[44] = o[0]
    n[45] = o[44]
    n[48] = o[41]
    n[51] = o[38]

    o[0] = n[0]
    o[3] = n[3]
    o[6] = n[6]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[12] = n[12]
    o[14] = n[14]
    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[18] = n[18]
    o[21] = n[21]
    o[24] = n[24]
    o[38] = n[38]
    o[41] = n[41]
    o[44] = n[44]
    o[45] = n[45]
    o[48] = n[48]
    o[51] = n[51]


def rotate_L2(o, n):
    n[0] = o[45]
    n[3] = o[48]
    n[6] = o[51]
    n[9] = o[17]
    n[10] = o[16]
    n[11] = o[15]
    n[12] = o[14]
    n[14] = o[12]
    n[15] = o[11]
    n[16] = o[10]
    n[17] = o[9]
    n[18] = o[44]
    n[21] = o[41]
    n[24] = o[38]
    n[38] = o[24]
    n[41] = o[21]
    n[44] = o[18]
    n[45] = o[0]
    n[48] = o[3]
    n[51] = o[6]

    o[0] = n[0]
    o[3] = n[3]
    o[6] = n[6]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[12] = n[12]
    o[14] = n[14]
    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[18] = n[18]
    o[21] = n[21]
    o[24] = n[24]
    o[38] = n[38]
    o[41] = n[41]
    o[44] = n[44]
    o[45] = n[45]
    o[48] = n[48]
    o[51] = n[51]


def rotate_R(o, n):
    n[2] = o[20]
    n[5] = o[23]
    n[8] = o[26]
    n[20] = o[47]
    n[23] = o[50]
    n[26] = o[53]
    n[27] = o[33]
    n[28] = o[30]
    n[29] = o[27]
    n[30] = o[34]
    n[32] = o[28]
    n[33] = o[35]
    n[34] = o[32]
    n[35] = o[29]
    n[36] = o[8]
    n[39] = o[5]
    n[42] = o[2]
    n[47] = o[42]
    n[50] = o[39]
    n[53] = o[36]

    o[2] = n[2]
    o[5] = n[5]
    o[8] = n[8]
    o[20] = n[20]
    o[23] = n[23]
    o[26] = n[26]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[30] = n[30]
    o[32] = n[32]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[36] = n[36]
    o[39] = n[39]
    o[42] = n[42]
    o[47] = n[47]
    o[50] = n[50]
    o[53] = n[53]


def rotate_R_prime(o, n):
    n[2] = o[42]
    n[5] = o[39]
    n[8] = o[36]
    n[20] = o[2]
    n[23] = o[5]
    n[26] = o[8]
    n[27] = o[29]
    n[28] = o[32]
    n[29] = o[35]
    n[30] = o[28]
    n[32] = o[34]
    n[33] = o[27]
    n[34] = o[30]
    n[35] = o[33]
    n[36] = o[53]
    n[39] = o[50]
    n[42] = o[47]
    n[47] = o[20]
    n[50] = o[23]
    n[53] = o[26]

    o[2] = n[2]
    o[5] = n[5]
    o[8] = n[8]
    o[20] = n[20]
    o[23] = n[23]
    o[26] = n[26]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[30] = n[30]
    o[32] = n[32]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[36] = n[36]
    o[39] = n[39]
    o[42] = n[42]
    o[47] = n[47]
    o[50] = n[50]
    o[53] = n[53]


def rotate_R2(o, n):
    n[2] = o[47]
    n[5] = o[50]
    n[8] = o[53]
    n[20] = o[42]
    n[23] = o[39]
    n[26] = o[36]
    n[27] = o[35]
    n[28] = o[34]
    n[29] = o[33]
    n[30] = o[32]
    n[32] = o[30]
    n[33] = o[29]
    n[34] = o[28]
    n[35] = o[27]
    n[36] = o[26]
    n[39] = o[23]
    n[42] = o[20]
    n[47] = o[2]
    n[50] = o[5]
    n[53] = o[8]

    o[2] = n[2]
    o[5] = n[5]
    o[8] = n[8]
    o[20] = n[20]
    o[23] = n[23]
    o[26] = n[26]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[30] = n[30]
    o[32] = n[32]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[36] = n[36]
    o[39] = n[39]
    o[42] = n[42]
    o[47] = n[47]
    o[50] = n[50]
    o[53] = n[53]


def rotate_U(o, n):
    n[0] = o[6]
    n[1] = o[3]
    n[2] = o[0]
    n[3] = o[7]
    n[5] = o[1]
    n[6] = o[8]
    n[7] = o[5]
    n[8] = o[2]
    n[9] = o[18]
    n[10] = o[19]
    n[11] = o[20]
    n[18] = o[27]
    n[19] = o[28]
    n[20] = o[29]
    n[27] = o[36]
    n[28] = o[37]
    n[29] = o[38]
    n[36] = o[9]
    n[37] = o[10]
    n[38] = o[11]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[3] = n[3]
    o[5] = n[5]
    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]


def rotate_U_prime(o, n):
    n[0] = o[2]
    n[1] = o[5]
    n[2] = o[8]
    n[3] = o[1]
    n[5] = o[7]
    n[6] = o[0]
    n[7] = o[3]
    n[8] = o[6]
    n[9] = o[36]
    n[10] = o[37]
    n[11] = o[38]
    n[18] = o[9]
    n[19] = o[10]
    n[20] = o[11]
    n[27] = o[18]
    n[28] = o[19]
    n[29] = o[20]
    n[36] = o[27]
    n[37] = o[28]
    n[38] = o[29]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[3] = n[3]
    o[5] = n[5]
    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]


def rotate_U2(o, n):
    n[0] = o[8]
    n[1] = o[7]
    n[2] = o[6]
    n[3] = o[5]
    n[5] = o[3]
    n[6] = o[2]
    n[7] = o[1]
    n[8] = o[0]
    n[9] = o[27]
    n[10] = o[28]
    n[11] = o[29]
    n[18] = o[36]
    n[19] = o[37]
    n[20] = o[38]
    n[27] = o[9]
    n[28] = o[10]
    n[29] = o[11]
    n[36] = o[18]
    n[37] = o[19]
    n[38] = o[20]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[3] = n[3]
    o[5] = n[5]
    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]


def rotate_x(o, n):
    n[0] = o[18]
    n[1] = o[19]
    n[2] = o[20]
    n[3] = o[21]
    n[4] = o[22]
    n[5] = o[23]
    n[6] = o[24]
    n[7] = o[25]
    n[8] = o[26]
    n[9] = o[11]
    n[10] = o[14]
    n[11] = o[17]
    n[12] = o[10]
    n[14] = o[16]
    n[15] = o[9]
    n[16] = o[12]
    n[17] = o[15]
    n[18] = o[45]
    n[19] = o[46]
    n[20] = o[47]
    n[21] = o[48]
    n[22] = o[49]
    n[23] = o[50]
    n[24] = o[51]
    n[25] = o[52]
    n[26] = o[53]
    n[27] = o[33]
    n[28] = o[30]
    n[29] = o[27]
    n[30] = o[34]
    n[32] = o[28]
    n[33] = o[35]
    n[34] = o[32]
    n[35] = o[29]
    n[36] = o[8]
    n[37] = o[7]
    n[38] = o[6]
    n[39] = o[5]
    n[40] = o[4]
    n[41] = o[3]
    n[42] = o[2]
    n[43] = o[1]
    n[44] = o[0]
    n[45] = o[44]
    n[46] = o[43]
    n[47] = o[42]
    n[48] = o[41]
    n[49] = o[40]
    n[50] = o[39]
    n[51] = o[38]
    n[52] = o[37]
    n[53] = o[36]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[3] = n[3]
    o[4] = n[4]
    o[5] = n[5]
    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[12] = n[12]
    o[14] = n[14]
    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[21] = n[21]
    o[22] = n[22]
    o[23] = n[23]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[30] = n[30]
    o[32] = n[32]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]
    o[39] = n[39]
    o[40] = n[40]
    o[41] = n[41]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]
    o[48] = n[48]
    o[49] = n[49]
    o[50] = n[50]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_x_prime(o, n):
    n[0] = o[44]
    n[1] = o[43]
    n[2] = o[42]
    n[3] = o[41]
    n[4] = o[40]
    n[5] = o[39]
    n[6] = o[38]
    n[7] = o[37]
    n[8] = o[36]
    n[9] = o[15]
    n[10] = o[12]
    n[11] = o[9]
    n[12] = o[16]
    n[14] = o[10]
    n[15] = o[17]
    n[16] = o[14]
    n[17] = o[11]
    n[18] = o[0]
    n[19] = o[1]
    n[20] = o[2]
    n[21] = o[3]
    n[22] = o[4]
    n[23] = o[5]
    n[24] = o[6]
    n[25] = o[7]
    n[26] = o[8]
    n[27] = o[29]
    n[28] = o[32]
    n[29] = o[35]
    n[30] = o[28]
    n[32] = o[34]
    n[33] = o[27]
    n[34] = o[30]
    n[35] = o[33]
    n[36] = o[53]
    n[37] = o[52]
    n[38] = o[51]
    n[39] = o[50]
    n[40] = o[49]
    n[41] = o[48]
    n[42] = o[47]
    n[43] = o[46]
    n[44] = o[45]
    n[45] = o[18]
    n[46] = o[19]
    n[47] = o[20]
    n[48] = o[21]
    n[49] = o[22]
    n[50] = o[23]
    n[51] = o[24]
    n[52] = o[25]
    n[53] = o[26]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[3] = n[3]
    o[4] = n[4]
    o[5] = n[5]
    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[12] = n[12]
    o[14] = n[14]
    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[21] = n[21]
    o[22] = n[22]
    o[23] = n[23]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[30] = n[30]
    o[32] = n[32]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]
    o[39] = n[39]
    o[40] = n[40]
    o[41] = n[41]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]
    o[48] = n[48]
    o[49] = n[49]
    o[50] = n[50]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_x2(o, n):
    n[0] = o[45]
    n[1] = o[46]
    n[2] = o[47]
    n[3] = o[48]
    n[4] = o[49]
    n[5] = o[50]
    n[6] = o[51]
    n[7] = o[52]
    n[8] = o[53]
    n[9] = o[17]
    n[10] = o[16]
    n[11] = o[15]
    n[12] = o[14]
    n[14] = o[12]
    n[15] = o[11]
    n[16] = o[10]
    n[17] = o[9]
    n[18] = o[44]
    n[19] = o[43]
    n[20] = o[42]
    n[21] = o[41]
    n[22] = o[40]
    n[23] = o[39]
    n[24] = o[38]
    n[25] = o[37]
    n[26] = o[36]
    n[27] = o[35]
    n[28] = o[34]
    n[29] = o[33]
    n[30] = o[32]
    n[32] = o[30]
    n[33] = o[29]
    n[34] = o[28]
    n[35] = o[27]
    n[36] = o[26]
    n[37] = o[25]
    n[38] = o[24]
    n[39] = o[23]
    n[40] = o[22]
    n[41] = o[21]
    n[42] = o[20]
    n[43] = o[19]
    n[44] = o[18]
    n[45] = o[0]
    n[46] = o[1]
    n[47] = o[2]
    n[48] = o[3]
    n[49] = o[4]
    n[50] = o[5]
    n[51] = o[6]
    n[52] = o[7]
    n[53] = o[8]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[3] = n[3]
    o[4] = n[4]
    o[5] = n[5]
    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[12] = n[12]
    o[14] = n[14]
    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[21] = n[21]
    o[22] = n[22]
    o[23] = n[23]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[30] = n[30]
    o[32] = n[32]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]
    o[39] = n[39]
    o[40] = n[40]
    o[41] = n[41]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]
    o[48] = n[48]
    o[49] = n[49]
    o[50] = n[50]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_y(o, n):
    n[0] = o[6]
    n[1] = o[3]
    n[2] = o[0]
    n[3] = o[7]
    n[5] = o[1]
    n[6] = o[8]
    n[7] = o[5]
    n[8] = o[2]
    n[9] = o[18]
    n[10] = o[19]
    n[11] = o[20]
    n[12] = o[21]
    n[13] = o[22]
    n[14] = o[23]
    n[15] = o[24]
    n[16] = o[25]
    n[17] = o[26]
    n[18] = o[27]
    n[19] = o[28]
    n[20] = o[29]
    n[21] = o[30]
    n[22] = o[31]
    n[23] = o[32]
    n[24] = o[33]
    n[25] = o[34]
    n[26] = o[35]
    n[27] = o[36]
    n[28] = o[37]
    n[29] = o[38]
    n[30] = o[39]
    n[31] = o[40]
    n[32] = o[41]
    n[33] = o[42]
    n[34] = o[43]
    n[35] = o[44]
    n[36] = o[9]
    n[37] = o[10]
    n[38] = o[11]
    n[39] = o[12]
    n[40] = o[13]
    n[41] = o[14]
    n[42] = o[15]
    n[43] = o[16]
    n[44] = o[17]
    n[45] = o[47]
    n[46] = o[50]
    n[47] = o[53]
    n[48] = o[46]
    n[50] = o[52]
    n[51] = o[45]
    n[52] = o[48]
    n[53] = o[51]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[3] = n[3]
    o[5] = n[5]
    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[12] = n[12]
    o[13] = n[13]
    o[14] = n[14]
    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[21] = n[21]
    o[22] = n[22]
    o[23] = n[23]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[30] = n[30]
    o[31] = n[31]
    o[32] = n[32]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]
    o[39] = n[39]
    o[40] = n[40]
    o[41] = n[41]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]
    o[48] = n[48]
    o[50] = n[50]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_y_prime(o, n):
    n[0] = o[2]
    n[1] = o[5]
    n[2] = o[8]
    n[3] = o[1]
    n[5] = o[7]
    n[6] = o[0]
    n[7] = o[3]
    n[8] = o[6]
    n[9] = o[36]
    n[10] = o[37]
    n[11] = o[38]
    n[12] = o[39]
    n[13] = o[40]
    n[14] = o[41]
    n[15] = o[42]
    n[16] = o[43]
    n[17] = o[44]
    n[18] = o[9]
    n[19] = o[10]
    n[20] = o[11]
    n[21] = o[12]
    n[22] = o[13]
    n[23] = o[14]
    n[24] = o[15]
    n[25] = o[16]
    n[26] = o[17]
    n[27] = o[18]
    n[28] = o[19]
    n[29] = o[20]
    n[30] = o[21]
    n[31] = o[22]
    n[32] = o[23]
    n[33] = o[24]
    n[34] = o[25]
    n[35] = o[26]
    n[36] = o[27]
    n[37] = o[28]
    n[38] = o[29]
    n[39] = o[30]
    n[40] = o[31]
    n[41] = o[32]
    n[42] = o[33]
    n[43] = o[34]
    n[44] = o[35]
    n[45] = o[51]
    n[46] = o[48]
    n[47] = o[45]
    n[48] = o[52]
    n[50] = o[46]
    n[51] = o[53]
    n[52] = o[50]
    n[53] = o[47]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[3] = n[3]
    o[5] = n[5]
    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[12] = n[12]
    o[13] = n[13]
    o[14] = n[14]
    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[21] = n[21]
    o[22] = n[22]
    o[23] = n[23]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[30] = n[30]
    o[31] = n[31]
    o[32] = n[32]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]
    o[39] = n[39]
    o[40] = n[40]
    o[41] = n[41]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]
    o[48] = n[48]
    o[50] = n[50]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_y2(o, n):
    n[0] = o[8]
    n[1] = o[7]
    n[2] = o[6]
    n[3] = o[5]
    n[5] = o[3]
    n[6] = o[2]
    n[7] = o[1]
    n[8] = o[0]
    n[9] = o[27]
    n[10] = o[28]
    n[11] = o[29]
    n[12] = o[30]
    n[13] = o[31]
    n[14] = o[32]
    n[15] = o[33]
    n[16] = o[34]
    n[17] = o[35]
    n[18] = o[36]
    n[19] = o[37]
    n[20] = o[38]
    n[21] = o[39]
    n[22] = o[40]
    n[23] = o[41]
    n[24] = o[42]
    n[25] = o[43]
    n[26] = o[44]
    n[27] = o[9]
    n[28] = o[10]
    n[29] = o[11]
    n[30] = o[12]
    n[31] = o[13]
    n[32] = o[14]
    n[33] = o[15]
    n[34] = o[16]
    n[35] = o[17]
    n[36] = o[18]
    n[37] = o[19]
    n[38] = o[20]
    n[39] = o[21]
    n[40] = o[22]
    n[41] = o[23]
    n[42] = o[24]
    n[43] = o[25]
    n[44] = o[26]
    n[45] = o[53]
    n[46] = o[52]
    n[47] = o[51]
    n[48] = o[50]
    n[50] = o[48]
    n[51] = o[47]
    n[52] = o[46]
    n[53] = o[45]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[3] = n[3]
    o[5] = n[5]
    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[12] = n[12]
    o[13] = n[13]
    o[14] = n[14]
    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[21] = n[21]
    o[22] = n[22]
    o[23] = n[23]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[30] = n[30]
    o[31] = n[31]
    o[32] = n[32]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]
    o[39] = n[39]
    o[40] = n[40]
    o[41] = n[41]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]
    o[48] = n[48]
    o[50] = n[50]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_z(o, n):
    n[0] = o[15]
    n[1] = o[12]
    n[2] = o[9]
    n[3] = o[16]
    n[4] = o[13]
    n[5] = o[10]
    n[6] = o[17]
    n[7] = o[14]
    n[8] = o[11]
    n[9] = o[51]
    n[10] = o[48]
    n[11] = o[45]
    n[12] = o[52]
    n[13] = o[49]
    n[14] = o[46]
    n[15] = o[53]
    n[16] = o[50]
    n[17] = o[47]
    n[18] = o[24]
    n[19] = o[21]
    n[20] = o[18]
    n[21] = o[25]
    n[23] = o[19]
    n[24] = o[26]
    n[25] = o[23]
    n[26] = o[20]
    n[27] = o[6]
    n[28] = o[3]
    n[29] = o[0]
    n[30] = o[7]
    n[31] = o[4]
    n[32] = o[1]
    n[33] = o[8]
    n[34] = o[5]
    n[35] = o[2]
    n[36] = o[38]
    n[37] = o[41]
    n[38] = o[44]
    n[39] = o[37]
    n[41] = o[43]
    n[42] = o[36]
    n[43] = o[39]
    n[44] = o[42]
    n[45] = o[33]
    n[46] = o[30]
    n[47] = o[27]
    n[48] = o[34]
    n[49] = o[31]
    n[50] = o[28]
    n[51] = o[35]
    n[52] = o[32]
    n[53] = o[29]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[3] = n[3]
    o[4] = n[4]
    o[5] = n[5]
    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[12] = n[12]
    o[13] = n[13]
    o[14] = n[14]
    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[21] = n[21]
    o[23] = n[23]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[30] = n[30]
    o[31] = n[31]
    o[32] = n[32]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]
    o[39] = n[39]
    o[41] = n[41]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]
    o[48] = n[48]
    o[49] = n[49]
    o[50] = n[50]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_z_prime(o, n):
    n[0] = o[29]
    n[1] = o[32]
    n[2] = o[35]
    n[3] = o[28]
    n[4] = o[31]
    n[5] = o[34]
    n[6] = o[27]
    n[7] = o[30]
    n[8] = o[33]
    n[9] = o[2]
    n[10] = o[5]
    n[11] = o[8]
    n[12] = o[1]
    n[13] = o[4]
    n[14] = o[7]
    n[15] = o[0]
    n[16] = o[3]
    n[17] = o[6]
    n[18] = o[20]
    n[19] = o[23]
    n[20] = o[26]
    n[21] = o[19]
    n[23] = o[25]
    n[24] = o[18]
    n[25] = o[21]
    n[26] = o[24]
    n[27] = o[47]
    n[28] = o[50]
    n[29] = o[53]
    n[30] = o[46]
    n[31] = o[49]
    n[32] = o[52]
    n[33] = o[45]
    n[34] = o[48]
    n[35] = o[51]
    n[36] = o[42]
    n[37] = o[39]
    n[38] = o[36]
    n[39] = o[43]
    n[41] = o[37]
    n[42] = o[44]
    n[43] = o[41]
    n[44] = o[38]
    n[45] = o[11]
    n[46] = o[14]
    n[47] = o[17]
    n[48] = o[10]
    n[49] = o[13]
    n[50] = o[16]
    n[51] = o[9]
    n[52] = o[12]
    n[53] = o[15]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[3] = n[3]
    o[4] = n[4]
    o[5] = n[5]
    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[12] = n[12]
    o[13] = n[13]
    o[14] = n[14]
    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[21] = n[21]
    o[23] = n[23]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[30] = n[30]
    o[31] = n[31]
    o[32] = n[32]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]
    o[39] = n[39]
    o[41] = n[41]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]
    o[48] = n[48]
    o[49] = n[49]
    o[50] = n[50]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]


def rotate_z2(o, n):
    n[0] = o[53]
    n[1] = o[52]
    n[2] = o[51]
    n[3] = o[50]
    n[4] = o[49]
    n[5] = o[48]
    n[6] = o[47]
    n[7] = o[46]
    n[8] = o[45]
    n[9] = o[35]
    n[10] = o[34]
    n[11] = o[33]
    n[12] = o[32]
    n[13] = o[31]
    n[14] = o[30]
    n[15] = o[29]
    n[16] = o[28]
    n[17] = o[27]
    n[18] = o[26]
    n[19] = o[25]
    n[20] = o[24]
    n[21] = o[23]
    n[23] = o[21]
    n[24] = o[20]
    n[25] = o[19]
    n[26] = o[18]
    n[27] = o[17]
    n[28] = o[16]
    n[29] = o[15]
    n[30] = o[14]
    n[31] = o[13]
    n[32] = o[12]
    n[33] = o[11]
    n[34] = o[10]
    n[35] = o[9]
    n[36] = o[44]
    n[37] = o[43]
    n[38] = o[42]
    n[39] = o[41]
    n[41] = o[39]
    n[42] = o[38]
    n[43] = o[37]
    n[44] = o[36]
    n[45] = o[8]
    n[46] = o[7]
    n[47] = o[6]
    n[48] = o[5]
    n[49] = o[4]
    n[50] = o[3]
    n[51] = o[2]
    n[52] = o[1]
    n[53] = o[0]

    o[0] = n[0]
    o[1] = n[1]
    o[2] = n[2]
    o[3] = n[3]
    o[4] = n[4]
    o[5] = n[5]
    o[6] = n[6]
    o[7] = n[7]
    o[8] = n[8]
    o[9] = n[9]
    o[10] = n[10]
    o[11] = n[11]
    o[12] = n[12]
    o[13] = n[13]
    o[14] = n[14]
    o[15] = n[15]
    o[16] = n[16]
    o[17] = n[17]
    o[18] = n[18]
    o[19] = n[19]
    o[20] = n[20]
    o[21] = n[21]
    o[23] = n[23]
    o[24] = n[24]
    o[25] = n[25]
    o[26] = n[26]
    o[27] = n[27]
    o[28] = n[28]
    o[29] = n[29]
    o[30] = n[30]
    o[31] = n[31]
    o[32] = n[32]
    o[33] = n[33]
    o[34] = n[34]
    o[35] = n[35]
    o[36] = n[36]
    o[37] = n[37]
    o[38] = n[38]
    o[39] = n[39]
    o[41] = n[41]
    o[42] = n[42]
    o[43] = n[43]
    o[44] = n[44]
    o[45] = n[45]
    o[46] = n[46]
    o[47] = n[47]
    o[48] = n[48]
    o[49] = n[49]
    o[50] = n[50]
    o[51] = n[51]
    o[52] = n[52]
    o[53] = n[53]
