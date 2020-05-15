import os
import subprocess
from shutil import copy
import random
import string
from toolkit.utils import dict2str, template, ASSETS
from toolkit.io.vasp import struct2poscar


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


sample_jobdict = {
    'hostname': 'cori',
    'hosttype': 'slurm',
    'local': '/home/xzhang1/run/final_journey/iter_111/outputs/Pb104S85',
    'remote': '/global/cscratch1/sd/xzhang1/fj/400_8_knl/Pb140S85',
    'job_name': 'Pb140S85'
}


def submit(jobdict):
    PREFIX = os.path.join(ASSETS, 'submit')
    template(i=f"{PREFIX}/{jobdict['hosttype']}", o="submit", d=jobdict)
    subprocess.run("bash submit", shell=True)


def autosubmit(d, struct):
    # hostname, hosttype, local, remote, job_name
    hostname = d['cluster']
    if hostname in ['knl', 'haswell']:
        hostname = 'cori'
    if hostname in ['comet', 'cori', 'eccle', 'irmik', 'nanaimo']:
        hosttype = 'slurm'
    elif hostname == 'localhost':
        hosttype = 'localhost'
    local = os.getcwd()
    uid = dict2str(struct.stoichiometry) + '_' + ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    remote = uid
    if hostname == 'comet':
        remote = f"/oasis/scratch/comet/xzhang1/temp_project/{uid}"
    elif hostname == 'cori':
        remote = f"/global/cscratch1/sd/xzhang1/{uid}"
    job_name = uid
    # jobdict
    jobdict = {
        'hostname': hostname,
        'hosttype': hosttype,
        'local': local,
        'remote': remote,
        'job_name': job_name
    }
    # submit
    PREFIX = os.path.join(ASSETS, 'submit')
    template(i=f"{PREFIX}/{hosttype}", o="submit", d=jobdict)
    subprocess.run("bash submit", shell=True)


class Listener:
    """
    Attributes
    ----------
    jobs : pandas.DataFrame::

                 cluster           local              remote state
        job_name
        Pb140S85    cori  /home/xzhang1/  /global/cscratch1/   NaN
        localhost       NaN             NaN                 NaN   NaN
    """

    def __init__(self):
        self.jobs = pd.DataFrame(columns=['job_name', 'cluster', 'local', 'remote', 'state']).set_index('job_name')

    def refresh(self):
        for cluster in self.jobs.cluster.unique():
            subprocess.run(f"bash {ASSETS}/refresh.{cluster}")
            self.jobs.update(
                pd.read_csv('refresh.output', delim_whitespace=True)
                  .rename(columns={'NAME': 'job_name', 'STATE': 'state'})
                  .set_index('job_name')
            )

    def retrieve(self):
        self.refresh()
        for index, row in self.jobs.iterrows():
            if not row.state and row.remote:
                subprocess.run(f"rsync -a --info=progress2 {row.cluster}:{row.remote} {row.local}")
                self.jobs.drop(index, inplace=True)
