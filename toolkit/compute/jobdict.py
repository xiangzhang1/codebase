import os
import random
import string
import subprocess
import pandas as pd
from toolkit.utils import template, ASSETS

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


class Retriever:
    """
    Attributes
    ----------
    jobs : pd.DataFrame(colummns(hostname, hosttype, local, remote, job_name, state))
    """

    def __init__(self):
        self.jobs = pd.DataFrame(columns=('hostname', 'hosttype', 'local', 'remote', 'job_name', 'state'))

    def register(self, jobdict):
        self.jobs.append(jobdict, ignore_index=True)

    def refresh(self):
        # append to ./state, read ./state, inner join
        for _, job in self.jobs.groupby('hostname').first().reset_index().iterrows():
            template(i=f"bash {ASSETS}/refresh/{job.hosttype}", o="refresh", d=job.to_dict())
            subprocess.run("bash refresh", shell=True)
        state = pd.read_csv("state", header=None, names=['job_name', 'state'], delim_whitespace=True)
        self.jobs = pd.merge(self.jobs.drop('state'), state, how='outer')

    def retrieve(self):
        self.refresh()
        for _, job in self.jobs[self.jobs.state.isnull()].iterrows():
            template(i=f"{ASSETS}/retrieve", o="retrieve", d=job.to_dict())
            subprocess.run(f"bash retrieve", shell=True)