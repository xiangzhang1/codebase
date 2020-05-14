import os
from shutil import copy
from codebase.toolkit.common import dict2str, template
from codebase.toolkit.io.vasp import struct2poscar

sample_d = {
    'cluster': 'knl',
    'queue': 'regular',
    'nnode': 4
}

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')


def rules(d):
    d.exec_file(f"{ASSETS}/rules.py")


def vasp(d, struct):
    PREFIX = os.path.join(ASSETS, 'vasp')
    template(
        i=f"{PREFIX}/INCAR",
        o="INCAR",
        d=d
    )
    struct2poscar(struct, "POSCAR")
    copy(f"{PREFIX}/KPOINTS", "KPOINTS")
    copy(f"{PREFIX}/POTCAR", "POTCAR")


def slurm(d, struct):
    PREFIX = os.path.join(ASSETS, 'slurm')
    template(i=f"{PREFIX}/submit.{d['cluster']}", o="submit", d=d)
    template(i=f"{PREFIX}/job.{d['cluster']}", o="job", d=d)