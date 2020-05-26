from contextlib import contextmanager
from os.path import exists

import numpy as np
import pandas as pd
import json
from toolkit.struct import Struct


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
    return dct


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return {'__ndarray__': True, 'data': obj.tolist()}
        if isinstance(obj, pd.DataFrame):
            return {'__DataFrame__': True, **obj.to_dict()}
        if isinstance(obj, Struct):
            return {'__Struct__': True, **obj.__dict__}
        return json.JSONEncoder.default(self, obj)


# syntactic sugar


def dump(obj, fname):
    with open(fname, 'w') as f:
        json.dump(obj, f, cls=MyEncoder)


def load(fname):
    with open(fname, 'r') as f:
        return json.load(f, object_hook=my_decoder)


@contextmanager
def json(fname):
    data = load(fname) if exists(fname) else {}
    try:
        yield data
    finally:
        dump(data, fname)