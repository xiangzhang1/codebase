import os
import itertools
from collections import OrderedDict
import numpy as np


class Struct(object):
    """
    Attributes
    ----------
    A : np.array((3,3)), or None
        Unit cell
    XS : pandas.DataFrame(columns=('X','Y','Z','S'))
        Cartesian coordinates and chemical symbols
    """
    def __init__(self, A, XS):
        self.A = A
        self.XS = XS

    @property
    def FX(self):
        """
        Returns
        -------
        np.array((3, N))
        """
        return np.dot(self.XS[['X', 'Y', 'Z']], np.linalg.inv(self.A))

    @property
    def stoichiometry(self):
        """
        For use in POSCAR5. Requires struct to be "blocky", i.e. [Pb, Pb, Pb, S, S, S, S].

        Returns
        -------
        OrderedDict.
        """
        stoichiometry = OrderedDict()
        for k, g in itertools.groupby(self.XS.S):
            assert k not in stoichiometry   # struct must be blocky, and stoichiometry ordered, or information loss.
            stoichiometry[k] = len(list(g))
        return stoichiometry

    def sort(self):
        """Makes struct blocky."""
        self.XS.sort_values(by='S', inplace=True)


def template(i, o, d):
    """i.format(d)

    Parameters
    ----------
    i : str
        input file path
    o : str
        output file path
    d : dict
    """
    with open(i, "r") as i:
        with open(o, "w") as o:
            o.write(
                i.read().format(**d)
            )


TEMPLATE = os.path.join(os.path.dirname(__file__), 'template')