import numpy as np
from toolkit.functions import XS
from toolkit.struct import Struct


def repad(struct, pad):
    X = struct.XS[['X', 'Y', 'Z']]
    S = struct.XS.S

    X -= np.amin(X, axis=0)
    box = np.amax(X, axis=0)

    A = np.diag(box + 2 * pad)
    X += pad
    return Struct(A=A, XS=XS(X, S))