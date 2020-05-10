import subprocess

from codebase.toolkit.common import template

def to_slurm(d):
    """
    Parameters
    ----------
    d: D
        software: 'compute'
        cluster: 'nersc'
    """
    template(i = f"{LIB_PATH}/submit.{d['software']}.{d['cluster']}", o = "submit", d = d)
    template(i = f"{LIB_PATH}/job.{d['software']}.{d['cluster']}", o = "job", d = d)


def submit():
    subprocess.run("bash submit", shell=True)


def is_complete(d):
    template(i=f"{LIB_PATH}/is_complete.{d['cluster']}", o="is_complete", d = d)
    return eval(subprocess.check_output("bash is_complete", shell=True))


def retrieve(d):
    template(i=f"{LIB_PATH}/retrieve.{d['cluster']}", o="retrieve", d = d)
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