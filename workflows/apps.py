"""Function-like.

Parameters
----------
d : dict
    {
        'cluster': 'knl'
    }
manager : Manager
relations : dict
"""

import os
from os.path import join
from uuid import uuid1
from apps.io.json import load, dump, Store
from apps.manager import dstruct2jobdict, submit

SAVE = join(os.path.dirname(__file__), 'save')


def load_manager_relations():
    return load(join(SAVE, 'manager.json')), load(join(SAVE, 'relations.json'))


def dump_manager_relations(manager, relations):
    dump(manager, join(SAVE, 'manager.json'))
    dump(relations, join(SAVE, 'relations.json'))


def to_uuid():
    uuid = uuid1().hex
    Store('toolkit.json')['uuid'] = uuid
    return uuid


def tell_relations_opt(relations, prev_uuid, uuid):   # tell relations it's opt->opt, presumbaly because prev walltime'd
    relations['opt->opt'] = relations['opt->opt'].append({
        'prev': prev_uuid,
        'next': uuid
    }, ignore_index=True)


def let_manager_submit(manager, d):
    jobdict = dstruct2jobdict(d)
    submit(jobdict)
    manager.register(jobdict)
    Store('toolkit.json')['jobdict'] = jobdict
