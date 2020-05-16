import pandas as pd


def XS(X, S):
    XS = pd.DataFrame(X, columns=('X', 'Y', 'Z'))
    XS['S'] = S
    return XS


def exec_file(fname, d):
    with open(fname) as f:
        exec(f.read(), globals(), d)


