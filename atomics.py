import collections
import pandas as pd

class D(collections.MutableMapping):
    # emulates dict
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._dict = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        # ValueError: ('overwrite', 'isif', 4, 'with', 3)
        if key in self._dict and self._dict[key] != value:
            raise ValueError('overwrite', key, self._dict[key], 'with', value)
        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def exec(self, expr):
        # d.exec('isif=4')
        exec(expr, globals(), self)

class Struct(object):
    """
    Attributes:
        A (3x3 numpy array): translation vector of unit cell, or None
        XS (pandas DataFrame: x, y, z, s): cartesian coordinates and chemical symbols
    """
    def __init__(self):
        super().__init__()
        self.A = None
        self.XS = pd.DataFrame(columns=['X', 'Y', 'Z', 'S'])

    @property
    def stoichiometry(self):
        """
        Returns:
            OrderedDict: stoichiometry sorted by symbol A-Z.
        """
        self.XS.sort_values(by='S', inplace=True)
        return collections.OrderedDict(self.XS.S.value_counts(ascending=True))
