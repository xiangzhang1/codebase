import random
import re
import string
import unicodedata
import pandas as pd


def array2str(arr):
    """
    Parameters
    ----------
    arr : np.array((M, N))

    Returns
    -------
    str
        1.0000  2.0000  3.0000
        4.0000  5.0000  6.0000
    """
    return pd.DataFrame(arr).to_string(header=False, index=False)


def dict2str(d):
    """
    Parameters
    ----------
    d : dict

    Returns
    -------
    str
        Pb55S38
    """
    return ''.join(k+str(v) for k,v in d.items())


def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def slugify(value):
    """Makes a string URL- and filename-friendly. """
    value = unicodedata.normalize('NFKD', value)
    value = re.sub(r'[^\w\s-]', '_', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value
