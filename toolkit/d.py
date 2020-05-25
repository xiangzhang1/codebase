import os

TEMPLATE = os.path.join(os.path.dirname(__file__), 'template')


def exec_file(fname, d):
    with open(fname) as f:
        exec(f.read(), globals(), d)


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