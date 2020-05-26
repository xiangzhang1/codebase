from codebase_023.toolkit.utils import random_string
import os

hostname = {
    'comet': 'comet',
    'eccle': 'eccle',
    'haswell': 'cori',
    'irmik': 'irmik',
    'knl': 'cori',
    'localhost': 'localhost',
    'nanaimo': 'nanaimo',
}[cluster]

hosttype = {
    'comet': 'slurm',
    'eccle': 'slurm',
    'haswell': 'slurm',
    'irmik': 'slurm',
    'knl': 'slurm',
    'localhost': 'node',
    'nanaimo': 'slurm'
}[cluster]

remote = {
    'comet': f'/oasis/scratch/comet/xzhang1/temp_project/{uid}',
    'eccle': f'{uid}',
    'haswell': f'/global/cscratch1/sd/xzhang1/{uid}',
    'irmik': f'{uid}',
    'knl': f'/global/cscratch1/sd/xzhang1/{uid}',
    'localhost': f'{uid}',
    'nanaimo': f'{uid}'
}[cluster]

if hosttype != 'node':
    job_name = os.path.basename(os.getcwd()) + '_' + random_string(4)   # practicality beats purity
else:
    job_name = hostname

del cluster
del random_string, os  # don't want you polluting namespace
