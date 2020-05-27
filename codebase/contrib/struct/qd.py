import numpy as np
from codebase.toolkit.struct import Struct, XS


def pad_to(struct, pad_to):
    X = struct.XS[['X', 'Y', 'Z']]
    S = struct.XS.S

    X = X - X.mean() + pad_to / 2.
    A = np.diag(pad_to)

    return Struct(A=A, XS=XS(X, S))