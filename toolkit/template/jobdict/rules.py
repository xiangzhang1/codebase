from toolkit.util import b64uuid, random_string
from os import getcwd

uid = b64uuid()

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

local = getcwd()

if hosttype != 'node':
    job_name = local + '_' + random_string(4)   # practicality beats purity
else:
    job_name = hostname                         # refresh/node

del cluster
del b64uuid, random_string, getcwd  # don't want you polluting namespace
