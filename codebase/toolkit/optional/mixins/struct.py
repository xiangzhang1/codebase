import itertools
from collections import OrderedDict
import numpy as np
from codebase.toolkit.common import dict2str


class StructMixin(object):

    @property
    def FX(self):
        """
        Returns
        -------
        np.array((3, N))
        """
        return np.dot(self.XS[['X','Y','Z']], np.linalg.inv(self.A))

    @property
    def unordered_stoichiometry(self):
        """
        Returns
        -------
        dict
        """
        return self.XS.S.value_counts()

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