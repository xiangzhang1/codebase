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
from codebase.toolkit.functions import template, exec_file
from codebase.toolkit.io.vasp import struct2poscar
from codebase.toolkit.io.json import open_json
from codebase.example_usage.templates import TEMPLATES
from codebase.toolkit.struct import Struct
from codebase.toolkit.utils import b64uuid


def to_vasp_2hour(d, struct):
    template(i=f"{TEMPLATES}/pbs_qd_2hour/vasp/INCAR_opt_2hour", o="INCAR", d=d)
    struct2poscar(struct, 'POSCAR')
    copy(f"{TEMPLATES}/pbs_qd_opt/vasp/KPOINTS", "KPOINTS")
    copy(f"{TEMPLATES}/pbs_qd_opt/vasp/POTCAR", "POTCAR")
    with open_json('toolkit.json') as data:
        data['struct'] = struct


def to_vasp_acc(d, struct):
    template(i=f"{TEMPLATES}/pbs_qd_2hour/vasp/INCAR_opt_acc", o="INCAR", d=d)
    struct2poscar(struct, 'POSCAR')
    copy(f"{TEMPLATES}/pbs_qd_opt/vasp/KPOINTS", "KPOINTS")
    copy(f"{TEMPLATES}/pbs_qd_opt/vasp/POTCAR", "POTCAR")
    with open_json('toolkit.json') as data:
        data['struct'] = struct


def to_subfile_2hour(d):
    template(i=f"{TEMPLATES}/pbs_qd_2hour/sub_vasp_{d['cluster']}_2hour", o="subfile", d=d)


def write_additional_metadata():
    with open_json('toolkit.json') as data:
        data['uuid'] = b64uuid()
        # data['relations'] = {'opt<-': uuid}
        data['about'] = {
            'workflow': 'pbs_qd_2hour',
            'version': '0.2.3',
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
