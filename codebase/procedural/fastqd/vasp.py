import os
from shutil import copy
from codebase.toolkit.common import dict2str, template
from codebase.toolkit.io.vasp import struct2poscar

ASSETS = os.path.join(os.path.dirname(__file__), 'assets', 'vasp')


def exec_rules(d, struct):
    d['stoichiometry'] = dict2str(struct.stoichiometry)
    d.exec_file(f"{ASSETS}/rules.py")


def to_vasp(d, struct):
    template(
        i=f"{ASSETS}/INCAR",
        o="INCAR",
        d=d
    )
    struct2poscar(struct, "POSCAR")
    copy(f"{ASSETS}/KPOINTS", "KPOINTS")
    copy(f"{ASSETS}/POTCAR", "POTCAR")

