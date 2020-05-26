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
from example_usage.templates import TEMPLATES
from toolkit.functions import template, exec_file
from toolkit.io.json import json, load


def prepare_jobdict(d):
    jobdict = {'cluster': d['cluster']}
    exec_file(f"{TEMPLATES}/d/jobdict/rules.py", jobdict)
    return jobdict


def submit(jobdict):
    template(i=f"{TEMPLATES}/jobdict/submit/{jobdict['hosttype']}", o="submit", d=jobdict)
    print(subprocess.check_output(['bash', 'submit']))
    jobdict['submit'] = True
    with json('toolkit.json') as data:
        data['jobdict'] = jobdict


def retrieve(jobdict):
    # retrieve to .
    template(i=f"{TEMPLATES}/jobdict/retrieve", o="retrieve", d=jobdict)
    print(subprocess.check_output(['bash', 'retrieve']))
    del jobdict['submit']
    with json('toolkit.json') as data:
        data['jobdict'] = jobdict


def squeue():
    copy(f"{TEMPLATES}/squeue", '.')
    print(subprocess.check_output(['bash', 'squeue']))
    return pd.read_csv("state", names=['job_name', 'state'], dtype=str, delim_whitespace=True)


def retrievable(jobdict, queue):
    return 'submit' in jobdict and jobdict['job_name'] not in queue.job_name.values


def mass_retrieve(root_dir):
    queue = squeue()
    for f in Path(root_dir).walk():
        if f.name == 'toolkit.json':
            with Path(f.dirname()):
                jobdict = load('toolkit.json')
                if retrievable(jobdict, queue):
                    retrieve(jobdict)
