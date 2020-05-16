from shutil import copy
from toolkit.functions import exec_file
from toolkit.io.json import load, dump
from toolkit.io.vasp import struct2poscar
from toolkit.manager import dstruct2jobdict, submit
from toolkit.utils import ASSETS, template
from projects import PROJECTS

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
    template(i=f"{ASSETS}/templates/d/job_vasp/gam/d['cluster']", o="job", d=d)


def load_manager():
    return load(f"{PROJECTS}/manager.json")


def dump_manager(manager):
    dump(manager, f"{PROJECTS}/manager.json")


def manage(manager, d, struct):
    jobdict = dstruct2jobdict(d, struct)
    submit(jobdict)
    manager.register(jobdict)
