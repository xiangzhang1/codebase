from shutil import copy
from toolkit.functions import exec_file
from projects.iter_111.json import load, dump
from toolkit.io.vasp import struct2poscar
from toolkit.manager import dstruct2jobdict, submit
from toolkit.utils import ASSETS, template

sample_d = {
    'cluster': str,
    'nnode': int
}


def prepare(d):
    exec_file(f"{ASSETS}/templates/d/job_vasp/gam/rules.py", d)


def vasp(d, struct):
    PREFIX = f"{ASSETS}/templates/d/vasp/pbs_qd_opt"
    template(i=f"{PREFIX}/INCAR", o="INCAR", d=d)
    struct2poscar(struct, 'POSCAR')
    copy(f"{PREFIX}/KPOINTS", "KPOINTS")
    copy(f"{PREFIX}/POTCAR", "POTCAR")


def job(d):
    template(i=f"{ASSETS}/templates/d/job_vasp/gam/{d['cluster']}", o="job", d=d)


def manage(manager, d, struct, struct_metadata):
    jobdict = dstruct2jobdict(d, struct)
    submit(jobdict)
    manager.register(jobdict)
    dump({
        'd': d,  # possible incompatibility due to upconverting from v0.1.0
        'struct': struct,
        'struct_metadata': struct_metadata,
        'jobdict': jobdict
    }, fname='toolkit.json')
