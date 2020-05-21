import pandas as pd
import numpy as np
from toolkit.struct import Struct


def XS(X, S):
    XS = pd.DataFrame(X, columns=('X', 'Y', 'Z'))
    XS['S'] = S
    return XS


def exec_file(fname, d):
    with open(fname) as f:
        exec(f.read(), globals(), d)


def pad(struct, pad):
    X = struct.XS[['X', 'Y', 'Z']]
    S = struct.XS.S

    X -= np.amin(X, axis=0)
    box = np.amax(X, axis=0)

    A = np.diag(box + 2 * pad)
    X += pad
    return Struct(A=A, XS=XS(X, S))