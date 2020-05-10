import pandas as pd

from codebase.toolkit.objects import Struct

def axs_to_struct(A, X, S):
    XS = pd.DataFrame(X, columns=('X','Y','Z')).join(
        pd.Series(S, name='S')
    )
    return Struct(A=A, XS=XS)