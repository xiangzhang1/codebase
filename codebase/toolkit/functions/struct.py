import itertools
from collections import OrderedDict
import pandas as pd
from codebase.toolkit.objects import Struct


def axs_to_struct(A, X, S):
    XS = pd.DataFrame(X, columns=('X','Y','Z')).join(
        pd.Series(S, name='S')
    )
    return Struct(A=A, XS=XS)


def unordered_stoichiometry(struct):
    """returns dict"""
    return struct.XS.S.value_counts()


def ordered_stoichiometry(struct):
    """For use in POSCAR5. Requires struct.XS to be "blocky", i.e. [Pb, Pb, Pb, S, S, S, S]. Returns OrderedDict. """
    stoichiometry = OrderedDict()
    for k, g in itertools.groupby(struct.XS.S):
        assert k not in stoichiometry   # struct must be blocky, or information loss may occur.
        stoichiometry[k] = len(list(g))

