"""
Parameters
----------
d : dict
    {
        'cluster': str
    }
"""
from os import getcwd, remove
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
    subprocess.run(['bash', 'submit'])
    with open_json('toolkit.json') as data:
        jobdict['submit'] = True
        data['jobdict'] = jobdict


def retrieve(jobdict):
    # retrieve to .
    assert jobdict['hostname'] != 'localhost'
    template(i=f"{TEMPLATES}/jobdict/retrieve", o="retrieve", d=jobdict)
    subprocess.run(['bash', 'retrieve'])
    with open_json('toolkit.json') as data:
        del jobdict['submit']
        data['jobdict'] = jobdict


def squeue():
    copy(f"{TEMPLATES}/squeue", '.')
    subprocess.run(['bash', 'squeue'])
    state = pd.read_csv("state", names=['job_name', 'state'], dtype=str, delim_whitespace=True)
    remove('squeue')
    remove('state')
    return state


def retrievable(jobdict, queue):
    return 'submit' in jobdict and jobdict['job_name'] not in queue.job_name.values


def mass_retrieve(root_dir):
    queue = squeue()
    for f in Path(root_dir).walk():
        if f.name == 'toolkit.json':
            with Path(f.dirname()):
                data = load('toolkit.json')
                if 'jobdict' in data:
                    jobdict = data['jobdict']
                    if retrievable(jobdict, queue):
                        print(f"{jobdict['hostname']}: {jobdict['remote']} -> {getcwd()}")
                        retrieve(jobdict)


def mass_report(root_dir):
    report = pd.DataFrame()
    queue = squeue()
    for f in Path(root_dir).walk():
        if f.name == 'toolkit.json':
            with Path(f.dirname()):
                data = load('toolkit.json')
                if 'jobdict' in data:
                    jobdict = data['jobdict']
                    if 'submit' in jobdict:
                        del jobdict['submit']
                        jobdict['local'] = getcwd()
                        report = report.append(jobdict, ignore_index=True)
    return pd.merge(report, queue, on='job_name', how='left')
