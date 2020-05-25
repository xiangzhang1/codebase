from os.path import exists, abspath
from collections.abc import MutableMapping
import numpy as np
import pandas as pd
import json
from toolkit.struct import Struct
from apps.manager import Manager


"""
If you want interoperability, go with JSON.

`json<https://docs.python.org/3/library/json.html>`_
"""


def my_decoder(dct):
    if '__ndarray__' in dct:
        return np.array(dct['data'])
    if '__DataFrame__' in dct:
        dct.pop('__DataFrame__')
        return pd.DataFrame.from_dict(dct)
    if '__Struct__' in dct:
        return Struct(dct['A'], dct['XS'])
    if '__Manager__' in dct:
        return Manager(dct['jobs'])
    return dct


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return {'__ndarray__': True, 'data': obj.tolist()}
        if isinstance(obj, pd.DataFrame):
            return {'__DataFrame__': True, **obj.to_dict()}
        if isinstance(obj, Struct):
            return {'__Struct__': True, **obj.__dict__}
        if isinstance(obj, Manager):
            return {'__Manager__': True, **obj.__dict__}
        return json.JSONEncoder.default(self, obj)


# syntactic sugar below


def dump(obj, fname):  # wraps json.dump
    with open(fname, 'w') as f:
        json.dump(obj, f, cls=MyEncoder)


def load(fname):  # wraps json.load
    with open(fname, 'r') as f:
        return json.load(f, object_hook=my_decoder)


class Store(MutableMapping):
    """Implements API like pd.HDFStore. Not efficient at all.

    `How to perfectly override a dict<https://stackoverflow.com/q/3387691/6417519>`_
    """
    def __init__(self, fname):
        self.fname = abspath(fname)
        if not exists(fname):
            dump({}, fname)

    def __getitem__(self, key):
        return load(self.fname)[key]

    def __setitem__(self, key, val):
        d = load(self.fname)
        d[key] = val
        dump(d, self.fname)

    def __delitem__(self, key):
        d = load(self.fname)
        del d[self.__keytransform__(key)]
        dump(d, self.fname)

    def __iter__(self):
        d = load(self.fname)
        return iter(d)

    def __len__(self):
        d = load(self.fname)
        return len(d)

    def __keytransform__(self, key):
        return key