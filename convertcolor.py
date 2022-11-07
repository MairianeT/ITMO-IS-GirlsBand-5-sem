import numpy as np
def RGB_YCoCg(R, G, B):
    matrix = np.array([[1/4, 1/2, 1/4], [1/2, 0, -1/2], [-1/4, 1/2, -1/4]])
    rgb = np.array([R, G, B])
    res = matrix.dot(rgb)
    return res[0], res[1], res[2]

def YCoCg_RGB(Y, Co, Cg):
    tmp = Y - Cg
    R = tmp + Co
    G = Y + Cg
    B = tmp - Co
    return R, G, B

def RGB_CMY(R, G, B):
    C = 1.0 - (R / 255.0)
    M = 1.0 - (G / 255.0)
    Y = 1.0 - (B / 255.0)
    return C, M, Y

def CMY_RGB(C, M, Y):
    R = 255.0 * (1.0 - C)
    G = 255.0 * (1.0 - M)
    B = 255.0 * (1.0 - Y)
    return R, G, B