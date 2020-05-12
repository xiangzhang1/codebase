import os, subprocess
from codebase.toolkit.common import template, dict2str

TEMPLATES = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../assets/templates/slurm')


def to_slurm(d, struct):
    """
    Parameters
    ----------
    d : D
        software: 'vasp'
        cluster: 'knl'
        queue: 'regular'
        nnode: 4
    struct : Struct
    """
    d['stoichiometry'] = dict2str(struct.stoichiometry)
    template(i = f"{TEMPLATES}/submit.{d['software']}.{d['cluster']}", o ="submit", d = d)
    template(i = f"{TEMPLATES}/job.{d['software']}.{d['cluster']}", o ="job", d = d)


def submit():
    subprocess.run("bash submit", shell=True)


def is_complete(d):
    template(i=f"{TEMPLATES}/is_complete.{d['cluster']}", o="is_complete", d = d)
    return eval(subprocess.check_output("bash is_complete", shell=True))


def retrieve(d):
    template(i=f"{TEMPLATES}/retrieve.{d['cluster']}", o="retrieve", d = d)
    subprocess.run("bash retrieve", shell=True)


class Pending(Exception):
    pass


def try_retrieve(d):
    """For recursion.

    Raises
    ------
    Pending
        If `not is_complete()`.
    """
    if is_complete(d):
        retrieve(d)
    else:
        raise Pending
