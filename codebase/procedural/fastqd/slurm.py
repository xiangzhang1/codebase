import os
from codebase.toolkit.common import template

ASSETS = os.path.join(os.path.dirname(__file__), 'assets', 'slurm')


def to_slurm(d, struct):
    template(i=f"{ASSETS}/submit.vasp.{d['cluster']}", o="submit", d=d)
    template(i=f"{ASSETS}/job.vasp.{d['cluster']}", o="job", d=d)
