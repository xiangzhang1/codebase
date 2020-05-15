import os
from shutil import copy
import random
import string
import pandas as pd
from codebase.toolkit.common import dict2str, template
from codebase.toolkit.io.vasp import struct2poscar

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')


sample_d = {
    'cluster': 'knl',
    'queue': 'regular',
    'nnode': 4
}


def exec_(d):
    d.exec_file(f"{ASSETS}/rules.py")


def vasp(d, struct):
    PREFIX = os.path.join(ASSETS, 'vasp')
    template(
        i=f"{PREFIX}/INCAR",
        o="INCAR",
        d=d
    )
    struct2poscar(struct, "POSCAR")
    copy(f"{PREFIX}/KPOINTS", "KPOINTS")
    copy(f"{PREFIX}/POTCAR", "POTCAR")


def job(d):
    PREFIX = os.path.join(ASSETS, 'job')
    template(i=f"{PREFIX}/{d['cluster']}", o="job", d=d)


def auto_submit(d, struct):
    # hostname, local, remote, job_name
    if d['cluster'] in ['knl', 'haswell']:
        hostname = 'cori'
    else:
        hostname = d['cluster']
    local = os.getcwd()
    uid = dict2str(struct.stoichiometry) + '_' + ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    if hostname == 'comet':
        remote = f"/oasis/scratch/comet/xzhang1/temp_project/{uuid}"
    elif hostname == 'cori':
        remote = f"/global/cscratch1/sd/xzhang1/{uuid}"
    else:
        remote = uid
    job_name = uid
    # jobdict
    jobdict = {
        'hostname': hostname,
        'local': local,
        'remote': remote,
        'job_name': job_name
    }
    # submit
    PREFIX = os.path.join(ASSETS, 'submit')
    if hostname in ['comet', 'cori', 'eccle', 'irmik', 'nanaimo']:
        template(i=f"{PREFIX}/slurm", o="submit", d=jobdict)


