import pandas as pd

from codebase.toolkit.objects import Struct

def axs_to_struct(A, X, S):
    """No such thing as pd.DataFrame(data1, columns1, data2, columns2) """
    XS = pd.concat([
        pd.DataFrame(X, columns=('X', 'Y', 'Z')),
        pd.Series(S, name='S')
    ], axis=1)
    return Struct(A=A, XS=XS)