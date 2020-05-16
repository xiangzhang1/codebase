from shutil import copy
from toolkit.functions import exec_file
from toolkit.io.json import load
from toolkit.io.vasp import struct2poscar
from toolkit.manager import dstruct2jobdict, submit
from toolkit.utils import ASSETS, template

sample_d = {
    'cluster': str,
    'nnode': int
}


def preprocess(d):
    exec_file(f"{ASSETS}/templates/d/job_vasp/gam/rules.py", d)


def to_vasp(d, struct):
    PREFIX = f"{ASSETS}/templates/d/vasp/pbs_qd_opt"
    template(i=f"{PREFIX}/INCAR", o="INCAR", d=d)
    struct2poscar(struct)
    copy(f"{PREFIX}/KPOINTS", "KPOINTS")
    copy(f"{PREFIX}/POTCAR", "POTCAR")


def to_slurm(d):
    template(i=f"{ASSETS}/templates/d/job_vasp/gam/d['cluster']", o="job", d=d)


manager = load(f"{ASSETS}/persistence/manager.json")


def manage(d, struct):
    jobdict = dstruct2jobdict(d, struct)
    submit(jobdict)
    manager.register(jobdict)


manager.refresh()
manager.jobs
manager._retrieve()
