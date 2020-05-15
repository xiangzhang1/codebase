import os
import pandas as pd

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')

class SlurmListener:
    """
    Attributes
    ----------
    jobs : pandas.DataFrame(columns=(cluster, job_name, local, remote, status))
        job_name is assumed to be unique.
    """

    def __init__(self):
        self.jobs = pd.DataFrame(columns=['cluster', 'job_name', 'local', 'remote', 'status'])

    def register(self, **job):
        assert set(job.keys()) <= set(self.jobs.columns)
        self.jobs = self.jobs.append(job)

    def refresh(self):
        for cluster in self.jobs.cluster:

