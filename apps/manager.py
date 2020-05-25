import os
from os import getcwd, remove
import subprocess
import pandas as pd
from toolkit.utils import template, random_string
from apps.assets import ASSETS

"""
So you're here.

I expected more of you. I expected you to be able to submit your 49 jobs from 3 projects to 8 clusters,
mentally keep track of them, and retrieve them when completed.

Give me your request in the form of a `jobdict`, and I'll take it from there.
"""

sample_jobdict = {
    'hostname': 'cori',
    'hosttype': 'slurm',
    'local': '/home/xzhang1/run/final_journey/iter_111/outputs/Pb104S85',
    'remote': '/global/cscratch1/sd/xzhang1/fj/400_8_knl/Pb140S85',
    'job_name': 'Pb140S85'
}


def submit(jobdict):
    template(i=f"{ASSETS}/templates/jobdict/submit/{jobdict['hosttype']}", o="submit", d=jobdict)
    subprocess.run("bash submit", shell=True)


class Manager(object):
    """
    Attributes
    ----------
    jobs : pd.DataFrame(columns=('hostname', 'hosttype', 'local', 'remote', 'job_name', 'state'))
    """

    def __init__(self, jobs):
        self.jobs = jobs

    def register(self, jobdict):
        self.jobs = self.jobs.append(jobdict, ignore_index=True)

    def refresh(self):
        # write state
        open("state", "w").close()
        for _, job in self.jobs.groupby('hostname').first().reset_index().iterrows():
            template(i=f"{ASSETS}/templates/jobdict/refresh/{job.hosttype}", o="refresh", d=job.to_dict())
            subprocess.run("bash refresh", shell=True)
            remove("refresh")
        state = pd.read_csv("state", names=['job_name', 'state'], dtype=str, delim_whitespace=True)
        remove("state")
        # join tables
        self.jobs = pd.merge(self.jobs.drop('state', axis='columns'), state, on='job_name', how='left')

    def _retrieve(self):
        for _, job in self.jobs[self.jobs.state.isnull()].iterrows():
            jobdict = job.to_dict()
            print(f"{jobdict['hostname']}:{jobdict['remote']} -> {jobdict['local']}")
            template(i=f"{ASSETS}/templates/jobdict/retrieve", o="retrieve", d=jobdict)
            subprocess.run(f"bash retrieve", shell=True)
            remove("retrieve")
            self.jobs.drop(_, inplace=True)

    def retrieve(self):
        self.refresh()
        self._retrieve()


"""
What? Still here? You don't even want to manually specify remote_path etc.? Okay.
"""


def to_jobdict(cluster, job_name_prefix=''):
    cwd = getcwd()
    job_name = job_name_prefix + random_string(4)
    template(i=f"{ASSETS}/templates/jobdict/auto_jobdict", o="auto_jobdict", d=dict(cwd=cwd, job_name=job_name))
    return pd.read_csv('auto_jobdict').set_index('cluster').loc[cluster].to_dict()


def dstruct2jobdict(d):
    return to_jobdict(cluster=d['cluster'], job_name_prefix=os.path.split(os.getcwd())[-1])

