import os
from shutil import copy
import random
import string
import pandas as pd
from codebase.toolkit.common import dict2str, template
from codebase.toolkit.io.vasp import struct2poscar

sample_d = {
    'cluster': 'knl',
    'queue': 'regular',
    'nnode': 4
}

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')


def prepare(d, struct):
    d['job_name'] = dict2str(struct.stoichiometry) + '_' + ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    d.exec_file(f"{ASSETS}/d.py")


def to_vasp(d, struct):
    PREFIX = os.path.join(ASSETS, 'vasp')
    template(
        i=f"{PREFIX}/INCAR",
        o="INCAR",
        d=d
    )
    struct2poscar(struct, "POSCAR")
    copy(f"{PREFIX}/KPOINTS", "KPOINTS")
    copy(f"{PREFIX}/POTCAR", "POTCAR")


def to_slurm(d):
    PREFIX = os.path.join(ASSETS, 'slurm')
    template(i=f"{PREFIX}/job.{d['cluster']}", o="job", d=d)


def submit(d):
    cluster = 'cori' if d['cluster'] in ['knl', 'haswell'] else d['cluster'],
    subprocess.run(f"rsync", shell=True)



def for_listener(d, listener):
    listener.jobs.append(
        pd.Series({
            'cluster':
            'local': os.getcwd()
        }, name=d['job_name'])
    )


