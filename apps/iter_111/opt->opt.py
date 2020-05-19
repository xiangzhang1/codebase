from os import chdir, mkdir
from uuid import uuid1

from apps.io.json import load, dump
from apps.iter_111 import prepare, to_vasp, to_subfile
from apps.manager.manager import dstruct2jobdict, submit
from toolkit.io.vasp import poscar2struct

dirname = 'Pb201S260'

chdir(dirname)
struct = poscar2struct('CONTCAR')
data = load('toolkit.json')
struct_metadata = data['struct_metadata']
prev_uuid = data['uuid']
chdir('..')

mkdir(dirname + '-cont')
chdir(dirname + '-cont')

d = {
    'cluster': 'knl',
    'queue': 'low',
    'nnode': 8
}

prepare(d)
to_vasp(d, struct)
to_subfile(d)

jobdict = dstruct2jobdict(d, struct)
submit(jobdict)

manager.register(jobdict)

uuid = uuid1().hex
relations['opt->opt'] = relations['opt->opt'].append({
    'prev': prev_uuid,
    'next': uuid
}, ignore_index=True)

dump({
    'd': d,
    'struct': struct,
    'struct_metadata': struct_metadata,

    'jobdict': jobdict,

    'uuid': uuid,

    '__toolkit_version__': '0.2.1'
}, fname='toolkit.json')

chdir('..')