"""template(i, o, d); exec_file(rules, d)

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