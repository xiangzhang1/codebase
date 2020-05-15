import os
import subprocess
import pandas as pd

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')


class Listener:
    """
    Attributes
    ----------
    jobs : pandas.DataFrame::

                 cluster           local              remote state
        job_name
        Pb140S85    cori  /home/xzhang1/  /global/cscratch1/   NaN
        dellpc       NaN             NaN                 NaN   NaN
    """

    def __init__(self):
        self.jobs = pd.DataFrame(columns=['job_name', 'cluster', 'local', 'remote', 'state']).set_index('job_name')

    def register(self, job_name, **details):
        self.jobs.loc[job_name] = details

    def squeue(self):
        self.jobs.state = 'NOT_IN_SQUEUE'
        for cluster in self.jobs.cluster.unique():
            subprocess.run(f"bash {ASSETS}/squeue.{cluster}") # generates squeue.output, columns=(NAME, STATE)
            self.jobs.update(
                pd.read_csv('refresh.output', delim_whitespace=True)
                  .rename({'NAME': 'job_name', 'STATE': 'state'})
                  .set_index('job_name')
            )

    def retrieve(self):
        for index, row in self.jobs.iterrows():
            if row.state == 'PRESUMED_COMPLETE' and row.remote:
                subprocess.run(
                    f"rsync -a --info=progress2 {row.cluster}:{row.remote} {row.local}"
                ) # careful trailing slash


