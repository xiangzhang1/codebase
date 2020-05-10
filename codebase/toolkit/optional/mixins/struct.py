import itertools
from collections import OrderedDict
import numpy as np


class StructMixin(object):

    @property
    def X(self):
        """Cartesian coordinates."""
        return self.XS[['X','Y','Z']].values

    @property
    def FX(self):
        """Fractional coordinates."""
        return np.dot(self.X, )

    @property
    def unordered_stoichiometry(self):
        """returns dict"""
        return self.XS.S.value_counts()

    @property
    def stoichiometry(self):
        """For use in POSCAR5. Requires struct to be "blocky", i.e. [Pb, Pb, Pb, S, S, S, S]. Returns OrderedDict. """
        stoichiometry = OrderedDict()
        for k, g in itertools.groupby(self.XS.S):
            assert k not in stoichiometry   # struct must be blocky, and stoichiometry ordered, or information loss.
            stoichiometry[k] = len(list(g))
        return stoichiometry
