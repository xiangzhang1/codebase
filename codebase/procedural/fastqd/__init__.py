import os
from shutil import copy
from codebase.toolkit.common import dict2str, template
from codebase.toolkit.io.vasp import struct2poscar

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')

sample_d = {
    'cluster': 'knl',
    'queue': 'regular',
    'nnode': 4
}


def rules(d, struct):
    d['stoichiometry'] = dict2str(struct.stoichiometry)
    d.exec_file(f"{ASSETS}/rules.py")


def vasp(d, struct):
    ASSETS = os.path.join(ASSETS, 'vasp')
    template(
        i=f"{ASSETS}/INCAR",
        o="INCAR",
        d=d
    )
    struct2poscar(struct, "POSCAR")
    copy(f"{ASSETS}/KPOINTS", "KPOINTS")
    copy(f"{ASSETS}/POTCAR", "POTCAR")


def slurm(d, struct):
    template(i=f"{ASSETS}/submit.vasp.{d['cluster']}", o="submit", d=d)
    template(i=f"{ASSETS}/job.vasp.{d['cluster']}", o="job", d=d)
