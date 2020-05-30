"""
Any attempt to abstract further inevitably falls apart. Copy, paste, and customize.

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
from codebase.toolkit.utils import b64uuid


def to_vasp_subfile(d, struct):
    # prepare d
    exec_file(f"{TEMPLATES}/pbs_qd/sub_vasp/rules.py", d)

    # to vasp
    template(i=f"{TEMPLATES}/pbs_qd/vasp/INCAR_opt", o="INCAR", d=d)
    struct2poscar(struct, 'POSCAR')
    copy(f"{TEMPLATES}/pbs_qd/vasp/KPOINTS", "KPOINTS")
    copy(f"{TEMPLATES}/pbs_qd/vasp/POTCAR", "POTCAR")

    # to subfile
    template(i=f"{TEMPLATES}/pbs_qd/sub_vasp/{d['cluster']}", o="subfile", d=d)

    # write metadata
    with open_json('toolkit.json') as data:
        data['uuid'] = b64uuid()
        data['d'] = d
        data['struct'] = struct
        # data['relations'] = {'opt<-': prev_uuid}
        data['about'] = {
            'workflow': 'pbs_qd_opt',
            'version': '0.2.3'
        }


from codebase.example_usage.jobdict import prepare_jobdict, submit
