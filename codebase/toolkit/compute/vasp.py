import os
from shutil import copy
from codebase.toolkit.common import template, dict2str
from codebase.toolkit.io.vasp import struct2poscar

RULES = os.path.dirname(os.path.realpath(__file__)) + '../assets/rules'
TEMPLATES = os.path.dirname(os.path.realpath(__file__)) + '../assets/templates/vasp'


def to_vasp(d, struct):
    """
    Parameters
    ----------
    d : D
        cluster: 'knl'
    struct : Struct
    """
    d.exec_file(f"{RULES}/vasp.py")

    template(
        i=f"{TEMPLATES}/INCAR",
        o="INCAR",
        d=d
    )

    struct2poscar(struct, 'POSCAR')

    copy(f"{TEMPLATES}/KPOINTS", "KPOINTS")

    copy(f"{TEMPLATES}/POTCAR", "POTCAR")


def to_slurm(d, struct):
    """
    Parameters
    ----------
    d : D
        cluster: 'knl'
        queue: 'regular'
        nnode: 4
    struct : Struct
    """
    d['stoichiometry'] = dict2str(struct.stoichiometry)
    cluster = d['cluster']

    template(
        i=f"{TEMPLATES}/slurm/{cluster}/subfile",
        o="INCAR",
        d=d
    )

    template(
        i=f"{TEMPLATES}/slurm/{cluster}/wrapper",
        o="INCAR",
        d=d
    )

