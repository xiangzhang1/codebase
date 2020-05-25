"""exec_file(rules, d); template(i, o, d)

Parameters
----------
d : dict
    {
        'cluster': str,
        'queue': str,
        'nnode': int
    }

Returns
-------
dict
    adds {
        'taskpernode': int,
        'ntask': int
    }
"""