import random
import string
import pandas as pd


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

