import numpy as np
from PyQt6.QtGui import QTransform

_board = np.array([[3.16260888e-02, -3.30701236e-01, 4.19977106e+02],
                   [-1.09647099e-01, -1.31679696e-01,  4.87941764e+02],
                   [-2.41137870e-04, -2.91447781e-04,  1.00000000e+00]])

_debug = np.array([[1.03106760e-01, -9.86045165e-03, 6.66978152e+02],
                   [ 4.10553857e-02,  3.41860141e-02, 5.60431240e+02],
                   [ 9.08682314e-05,  7.51824966e-05,  1.00000000e+00]])

BOARD_TRANSFORM = QTransform()
DEBUG_TRANSFORM = QTransform()
BOARD_TRANSFORM.setMatrix(_board[0][0], _board[1][0], _board[2][0],
                          _board[0][1], _board[1][1], _board[2][1],
                          _board[0][2], _board[1][2], _board[2][2])

DEBUG_TRANSFORM.setMatrix(_debug[0][0], _debug[1][0], _debug[2][0],
                          _debug[0][1], _debug[1][1], _debug[2][1],
                          _debug[0][2], _debug[1][2], _debug[2][2])