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


