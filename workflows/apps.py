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


from uuid import uuid1
from apps.io.json import Store
from apps.manager.manager import dstruct2jobdict, submit


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
