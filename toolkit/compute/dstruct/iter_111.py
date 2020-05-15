from shutil import copy
from toolkit.utils import template, ASSETS
from toolkit.io.vasp import struct2poscar


sample_d = {
    'cluster': 'knl',
    'queue': 'regular',
    'nnode': 4
}


def exec_(d):
    d.exec_file(f"{ASSETS}/rules.py")


def vasp(d, struct):
    template(
        i=f"{ASSETS}/vasp/INCAR",
        o="INCAR",
        d=d
    )
    struct2poscar(struct, "POSCAR")
    copy(f"{ASSETS}/vasp/KPOINTS", "KPOINTS")
    copy(f"{ASSETS}/vasp/POTCAR", "POTCAR")


def job(d):
    template(i=f"{ASSETS}/sub_vasp_gam/{d['cluster']}", o="sub_vasp_gam", d=d)


