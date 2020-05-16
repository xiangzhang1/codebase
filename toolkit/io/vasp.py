import numpy as np
from collections import OrderedDict
from toolkit.utils import array2str, dict2str
from toolkit.struct import Struct
from toolkit.functions import XS


def struct2str(struct):
    """
    Returns
    -------
    str
        POSCAR5 string

    Note
    ----
    Limited functionality. Does not support no selective dynamics, no cartesian.
    """
    label = dict2str(struct.stoichiometry)
    A = array2str(struct.A)
    _ = struct.stoichiometry
    stoichiometry = ' '.join(_.keys()) + '\n' + ' '.join(map(str, _.values()))
    FX = array2str(struct.FX)
    return (
        f'{label}\n'
        f'1.0\n'
        f'{A}\n'
        f'{stoichiometry}\n'
        f'Direct\n'
        f'{FX}\n'
    )   # https://stackoverflow.com/q/45965007/6417519


def struct2poscar(struct, poscar):
    """
    Parameters
    ----------
    struct : Struct
    poscar : str, path
    """
    with open(poscar, 'w') as f:
        f.write(struct2str(struct))


def poscar2struct(poscar):
    """
    Parameters
    ----------
    poscar : str, path
    """
    with open(poscar, 'r') as f:
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
    return Struct(A, XS(X, S))

