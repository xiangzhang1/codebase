import os
from shutil import copy
from codebase.toolkit.common import dict2str, template
from codebase.toolkit.io.vasp import struct2poscar

DIRNAME = os.path.dirname(__file__)
TEMPLATES = os.path.join(DIRNAME, 'templates')

sample_d = {
    'cluster': 'knl',
    'queue': 'regular',
    'nnode': 4
}


def exec_(d, struct):
    d['stoichiometry'] = dict2str(struct.stoichiometry)
    d.exec_file(f"{DIRNAME}/rules.py")


def vasp(d, struct):
    template(
        i=f"{TEMPLATES}/INCAR",
        o="INCAR",
        d=d
    )
    struct2poscar(struct, "POSCAR")
    copy(f"{TEMPLATES}/KPOINTS", "KPOINTS")
    copy(f"{TEMPLATES}/POTCAR", "POTCAR")


def slurm(d, struct):
    template(i=f"{TEMPLATES}/slurm/submit.vasp.{d['cluster']}", o="submit", d=d)
    template(i=f"{TEMPLATES}/slurm/job.vasp.{d['cluster']}", o="job", d=d)
