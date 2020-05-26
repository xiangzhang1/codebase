"""
Parameters
----------
d : dict
    {
        'cluster': str
    }
"""
import subprocess
from shutil import copy
from path import Path
import pandas as pd
from codebase_debug.example_usage.templates import TEMPLATES
from codebase_debug.toolkit.functions import template, exec_file
from codebase_debug.toolkit.io.json import open_json, load


def prepare_jobdict(d):
    jobdict = {'cluster': d['cluster']}
    exec_file(f"{TEMPLATES}/jobdict/rules.py", jobdict)
    return jobdict


def submit(jobdict):
    template(i=f"{TEMPLATES}/jobdict/submit/{jobdict['hosttype']}", o="submit", d=jobdict)
    print(subprocess.check_output(['bash', 'submit']).decode())
    with open_json('toolkit.json') as data:
        jobdict['submit'] = True
        data['jobdict'] = jobdict


def retrieve(jobdict):
    # retrieve to .
    assert jobdict['hostname'] != 'localhost'
    template(i=f"{TEMPLATES}/jobdict/retrieve", o="retrieve", d=jobdict)
    print(subprocess.check_output(['bash', 'retrieve']).decode())
    with open_json('toolkit.json') as data:
        del jobdict['submit']
        data['jobdict'] = jobdict


def squeue():
    copy(f"{TEMPLATES}/squeue", '.')
    print(subprocess.check_output(['bash', 'squeue']).decode())
    return pd.read_csv("state", names=['job_name', 'state'], dtype=str, delim_whitespace=True)


def retrievable(jobdict, queue):
    return 'submit' in jobdict and jobdict['job_name'] not in queue.job_name.values


def mass_retrieve(root_dir):
    queue = squeue()
    for f in Path(root_dir).walk():
        if f.name == 'toolkit.json':
            with Path(f.dirname()):
                jobdict = load('toolkit.json')['jobdict']
                if retrievable(jobdict, queue):
                    retrieve(jobdict)
