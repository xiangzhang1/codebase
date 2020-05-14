import os
from codebase.toolkit.common import template

TEMPLATES = os.path.join(os.path.realpath(__file__), 'templates')


def to_slurm(d, struct):
    """
    Parameters
    ----------
    d : D
        software: 'templates'
        cluster: 'knl'
        queue: 'regular'
        nnode: 4
    struct : Struct
    """
    template(i = f"{TEMPLATES}/templates/submit.{d['software']}.{d['cluster']}", o ="submit", d = d)
    template(i = f"{TEMPLATES}/templates/job.{d['software']}.{d['cluster']}", o ="job", d = d)


