import pandas as pd


def XS(X, S):
    XS = pd.DataFrame(X, columns=('X', 'Y', 'Z'))
    XS['S'] = S
    return XS
