import os
from shutil import copy
from codebase.toolkit.common import template, dict2str
from codebase.toolkit.io.vasp import struct2poscar

RULES = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../assets/rules')
TEMPLATES = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../assets/templates/vasp')


def expand(d, struct):
    d['stoichiometry'] = dict2str(struct.stoichiometry)
    d.exec_file(f"{RULES}/{d['software']}.py")


def to_vasp(d, struct):
    """
    Parameters
    ----------
    d : D
        cluster: 'knl'
    struct : Struct
    """
    template(
        i=f"{TEMPLATES}/INCAR",
        o="INCAR",
        d=d
    )

    struct2poscar(struct, 'POSCAR')

    copy(f"{TEMPLATES}/KPOINTS", "KPOINTS")

    copy(f"{TEMPLATES}/POTCAR", "POTCAR")




