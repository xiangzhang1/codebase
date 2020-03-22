import pandas as pd
from ..utils import slugify
from ..atomics import Struct

def exec_shorthand(d, text):
    # exec_shorthand(d, "insulator, qd, spin=fm")
    for _ in text.split(','):
        _ = slugify(_)
        if '=' not in _:        # insulator
            d[_] = None
        else:                   # kpoints=[1,1] or spin=fm
            l, r = _.split('=')
            l, r = slugify(l), slugify(r)
            try:                # kpoints=[1,1]
                d[l] = eval(r)
            except NameError:   # spin=fm
                d[l] = r

def exec_file(d, path):
    # 文件用 # 分块
    for i in range(3):
        with open(path, "r") as file:
            for block in file.read().split('#'):
                try:
                    d.exec('#' + block)
                except:
                    if i == 2:
                        raise

def AXsymbol_to_struct(A, X, symbol):
    struct = Struct()
    struct.A = A
    struct.X = pd.DataFrame(X, columns=['x', 'y', 'z'])
    struct.X['symbol'] = symbol
    return struct