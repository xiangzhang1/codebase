from codebase.toolkit.utils import random_string
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

if hosttype != 'node':
    job_name = os.path.basename(os.getcwd()) + '_' + random_string(4)   # practicality beats purity
else:
    job_name = hostname

remote = {
    'comet': f'/oasis/scratch/comet/xzhang1/temp_project/{job_name}',
    'eccle': f'{job_name}',
    'haswell': f'/global/cscratch1/sd/xzhang1/{job_name}',
    'irmik': f'{job_name}',
    'knl': f'/global/cscratch1/sd/xzhang1/{job_name}',
    'localhost': os.getcwd(),
    'nanaimo': f'{job_name}'
}[cluster]

del cluster
del random_string, os  # don't want you polluting namespace
