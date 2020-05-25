import numpy as np

import toolkit.__init__
import toolkit.function
from toolkit.__init__ import Struct
from toolkit.function import XS


def repad(struct, pad):
    X = toolkit.function.XS[['X', 'Y', 'Z']]
    S = toolkit.function.XS.S

    X -= np.amin(X, axis=0)
    box = np.amax(X, axis=0)

    A = np.diag(box + 2 * pad)
    X += pad
    return Struct(A=A, XS=XS(X, S))