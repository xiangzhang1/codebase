import os
import subprocess
from shutil import copy
import random
import string
import pandas as pd
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
    template(
        i=f"{ASSETS}/vasp/INCAR",
        o="INCAR",
        d=d
    )
    struct2poscar(struct, "POSCAR")
    copy(f"{ASSETS}/vasp/KPOINTS", "KPOINTS")
    copy(f"{ASSETS}/vasp/POTCAR", "POTCAR")


def job(d):
    template(i=f"{ASSETS}/job/{d['cluster']}", o="job", d=d)


sample_jobdict = {
    'hostname': 'cori',
    'hosttype': 'slurm',
    'local': '/home/xzhang1/run/final_journey/iter_111/outputs/Pb104S85',
    'remote': '/global/cscratch1/sd/xzhang1/fj/400_8_knl/Pb140S85',
    'job_name': 'Pb140S85'
}


def auto_jobdict(cluster, uid_prefix=''):
    cwd = os.getcwd()
    uid = uid_prefix + ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    template(i=f"{ASSETS}/jobdicts.csv", o="jobdict.csv", d=dict(cwd=cwd, uid=uid))
    jobdicts = pd.read_csv('jobdicts.csv').set_index('cluster')
    jobdict = jobdicts.loc[cluster]
    return jobdict


def submit(jobdict):
    template(i=f"{ASSETS}/submit/{jobdict['hosttype']}", o="submit", d=jobdict)
    subprocess.run("bash submit", shell=True)


class SlurmListener:

    def __init__(self):
        self.jobs = pd.DataFrame(columns=('hostname', 'hosttype', 'local', 'remote', 'job_name', 'state'))

    def add(self, jobdict):
        self.jobs.append(jobdict, ignore_index=True)

    def status(self):

    def fetch(self):


class Retriever:
    """
    Attributes
    ----------
    jobs : pandas.DataFrame::

                 cluster           local              remote state
        job_name
        Pb140S85    cori  /home/xzhang1/  /global/cscratch1/   NaN
        node       NaN             NaN                 NaN   NaN
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


