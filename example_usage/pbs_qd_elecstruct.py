"""
Parameters
----------
d : dict
    {
        'cluster': 'knl',
        'queue': 'low',
        'nnode': 4
    }
struct : Struct
"""


from shutil import copy
from toolkit.struct import Struct
from toolkit.d import TEMPLATE, template, exec_file
from toolkit.io.json import Store
from toolkit.io.vasp import struct2poscar


def prepare_d(d):
    exec_file(f"{TEMPLATE}/d/sub_vasp/gam/rules.py", d)
    Store('toolkit.json')['d'] = d


def to_vasp(d, struct):
    PREFIX = f"{TEMPLATE}/d/vasp/pbs_qd_sc_bd_lm"
    template(i=f"{PREFIX}/INCAR", o="INCAR", d=d)
    struct2poscar(struct, 'POSCAR')
    copy(f"{PREFIX}/KPOINTS", "KPOINTS")
    copy(f"{PREFIX}/POTCAR", "POTCAR")
    Store('toolkit.json')['struct'] = struct


def to_subfile(d):
    template(i=f"{TEMPLATE}/d/sub_vasp/gam/{d['cluster']}", o="subfile", d=d)


# scp; sbatch; rsync
