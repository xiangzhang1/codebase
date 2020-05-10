import collections
import pandas as pd


class D(collections.MutableMapping):
    # emulates a dict
    def __init__(self, *args, **kwargs):
        self._dict = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        # ValueError: ('overwrite', 'isif', 1, 'with', 2)
        if key in self._dict and self._dict[key] != value:
            raise ValueError('overwrite', key, self._dict[key], 'with', value)
        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def exec_(self, expr):
        # d.exec_('isif=1')
        exec(expr, globals(), self)     # globals must be a dict


class Struct(object):
    """
    Attributes
    ----------
    A : 3x3 numpy array, or None
        Unit cell
    XS : pandas.DataFrame(columns=(X,Y,Z,S))
        Cartesian coordinates and chemical symbols
    """
    def __init__(self, A, XS):
        self.A = A
        self.XS = XS

