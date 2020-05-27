import numpy as np

import codebase.toolkit.struct
from codebase.toolkit.struct import Struct, XS


def repad(struct, pad):
    X = codebase.toolkit.struct.XS[['X', 'Y', 'Z']]
    S = codebase.toolkit.struct.XS.S

    X -= np.amin(X, axis=0)
    box = np.amax(X, axis=0)

    A = np.diag(box + 2 * pad)
    X += pad
    return Struct(A=A, XS=XS(X, S))