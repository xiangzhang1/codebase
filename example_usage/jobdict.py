"""
Parameters
----------
d : dict
    {
        'cluster': str
    }
"""
from toolkit.d import TEMPLATE, template, exec_file


def prepare_jobdict(d):
    jobdict = {'cluster': d['cluster']}
    exec_file(f"{TEMPLATE}/d/jobdict/rules.py", jobdict)
    return jobdict


def