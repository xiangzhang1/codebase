import numpy as np

import toolkit.struct
import toolkit.functions
from toolkit.struct import Struct, XS


def repad(struct, pad):
    X = toolkit.struct.XS[['X', 'Y', 'Z']]
    S = toolkit.struct.XS.S

    X -= np.amin(X, axis=0)
    box = np.amax(X, axis=0)

    A = np.diag(box + 2 * pad)
    X += pad
    return Struct(A=A, XS=XS(X, S))