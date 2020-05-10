import numpy as np
import pandas as pd
from collections import OrderedDict
import textwrap     # PEP257: multiline string indentation sucks
from codebase.toolkit.functions.struct import ordered_stoichiometry, axs_to_struct

def array2string(arr):
    """
    Parameters
    ----------
    arr : 2D np.array

    Returns
    -------
    str
        1.0000  2.0000  3.0000
        4.0000  5.0000  6.0000
    """
    return pd.DataFrame(arr).to_string(header=False, index=False)


def dict2string(d):
    """
    Parameters
    ----------
    d : OrderedDict or dict

    Returns
    -------
    str
        Pb55S38
    """
    return ''.join(k+str(v) for k,v in d.items())


def struct2str(struct):
    """
    Returns
    -------
    str
        POSCAR5 string. This is very caveman: no selective dynamics, no cartesian. But ase writes POSCAR4, so uh...
    """
    label = dict2string(ordered_stoichiometry(struct))
    A = array2string(struct.A)
    _ = ordered_stoichiometry(struct)
    stoichiometry = ' '.join(_.keys()) + '\n' + ' '.join(map(str, _.values()))
    X = array2string(struct.XS[['X','Y','Z']])
    return textwrap.dedent(f"""
        {label}
        1.0
        {A}
        {stoichiometry}
        Direct
        {X}
    """)


def write_poscar(filename, struct):
    with open(filename, 'w') as f:
        f.write(struct2str(struct))


def read_poscar(filename):
    """
    Parameters
    ----------
    filename
        POSCAR5. This is very caveman: no selective dynamics, no cartesian. But it preserves X order.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()                                   # PbS
    scaling = float(lines[1].strip())                           # 1.0
    A = np.float_([line.split() for line in lines[2:5]])        # 3 0 0         # yes, np.float_([]) is necessary
    A *= scaling                                                # 0 3 0
    stoichiometry = OrderedDict(zip(                            # 0 0 3
        lines[5].split(),                                       # Pb S
        [int(x) for x in lines[6].split()]                      # 4  4
    ))                                                          # Direct
    FX = np.float32([line.split()[:3] for line in lines[8:8 + sum(stoichiometry.values())]])
    X = np.dot(FX, A)
    S = [k for k,v in stoichiometry.items() for _ in range(v)]
    return axs_to_struct(A, X, S)

