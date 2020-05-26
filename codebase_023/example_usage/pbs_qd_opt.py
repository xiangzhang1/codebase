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
from codebase_023.toolkit.functions import template, exec_file
from codebase_023.toolkit.io.vasp import struct2poscar
from codebase_023.toolkit.io.json import json
from codebase_023.example_usage.templates import TEMPLATES
from codebase_023.toolkit.struct import Struct
from codebase_023.toolkit.utils import b64uuid


def prepare_d(d):
    exec_file(f"{TEMPLATES}/d/sub_vasp/gam/rules.py", d)
    with json('toolkit.json') as data:
        data['d'] = d


def to_vasp(d, struct):
    PREFIX = f"{TEMPLATES}/d/vasp/pbs_qd_opt"
    template(i=f"{PREFIX}/INCAR", o="INCAR", d=d)
    struct2poscar(struct, 'POSCAR')
    copy(f"{PREFIX}/KPOINTS", "KPOINTS")
    copy(f"{PREFIX}/POTCAR", "POTCAR")
    with json('toolkit.json') as data:
        data['struct'] = struct


def to_subfile(d):
    template(i=f"{TEMPLATES}/d/sub_vasp/gam/{d['cluster']}", o="subfile", d=d)


def write_additional_metadata():
    with json('toolkit.json') as data:
        data['uuid'] = b64uuid()
        # data['relations'] = {'opt<-': uuid}
        data['about'] = {
            'workflow': 'pbs_qd_opt',
            '__toolkit_version__': '0.2.3',
            # 'struct_metadata': dict
        }


signature = {
    'uuid': str,
    'd': dict,
    'struct': Struct,
    'jobdict': dict,    # optional
    'relations': {      # optional
        'opt<-': str
    },
    'about': {
        'version': str,
        'workflow': str,    # optional
        'struct_metadata': dict     # optional
    }
}
