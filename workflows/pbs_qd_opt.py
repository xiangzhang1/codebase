"""Function-like.

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
from toolkit.io.vasp import struct2poscar
from toolkit.struct import Struct
from toolkit import template, exec_file
from toolkit.io.json import Store
from apps.assets import ASSETS


def prepare(d):
    exec_file(f"{ASSETS}/templates/d/sub_vasp/gam/rules.py", d)
    Store('toolkit.json')['d'] = d


def to_vasp(d, struct):
    PREFIX = f"{ASSETS}/templates/d/vasp/pbs_qd_opt"
    template(i=f"{PREFIX}/INCAR", o="INCAR", d=d)
    struct2poscar(struct, 'POSCAR')
    copy(f"{PREFIX}/KPOINTS", "KPOINTS")
    copy(f"{PREFIX}/POTCAR", "POTCAR")
    Store('toolkit.json')['struct'] = struct


def to_subfile(d):
    template(i=f"{ASSETS}/templates/d/sub_vasp/gam/{d['cluster']}", o="subfile", d=d)


def write_additional_metadata():
    store = Store('toolkit.json')
    store['workflow'] = 'pbs_qd_opt'
    store['__toolkit_version__'] = '0.2.2'
