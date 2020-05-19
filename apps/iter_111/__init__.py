from shutil import copy
from uuid import uuid1
from toolkit.functions import exec_file
from toolkit.io.vasp import struct2poscar
from toolkit.struct import Struct
from toolkit.utils import template
from apps.io.json import dump
from apps.manager.manager import dstruct2jobdict, submit
from apps.assets import ASSETS

sample_d = {
    'cluster': str,
    'nnode': int
}


def prepare(d):
    exec_file(f"{ASSETS}/templates/d/job_vasp/gam/rules.py", d)


def to_vasp(d, struct):
    PREFIX = f"{ASSETS}/templates/d/vasp/pbs_qd_opt"
    template(i=f"{PREFIX}/INCAR", o="INCAR", d=d)
    struct2poscar(struct, 'POSCAR')
    copy(f"{PREFIX}/KPOINTS", "KPOINTS")
    copy(f"{PREFIX}/POTCAR", "POTCAR")


def to_subfile(d):
    template(i=f"{ASSETS}/templates/d/sub_vasp/gam/{d['cluster']}", o="job", d=d)


# ------------------------------------

# apps.manager

jobdict = dstruct2jobdict(d, struct)
submit(jobdict)

# apps.relations

manager.register(jobdict)

uuid = uuid1().hex


# -----------------------------------


dump({
    'd': d,
    'struct': struct,
    'struct_metadata': struct_metadata,

    'jobdict': jobdict,

    'uuid': uuid,

    '__toolkit_version__': '0.2.0'
}, fname='toolkit.json')



sample_json = {
    'd': {
        'cluster': 'knl',
        'nnode': 4,
        'queue': 'low'
    },
    'struct': Struct,
    'struct_metadata': {
        'N': int,
        'pad': float,
        'symmetry': str,
        'unit_cell': str,
        'wulff': {'100': 6.02, '111': 5.48}
    },
    'jobdict': sample_jobdict,
    '__toolkit_version__': '0.2.0'
}
