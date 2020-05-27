"""exec_file(rules, d); template(i, o, d)

Parameters
----------
jobdict : dict
    {
        'cluster': str
    }

Returns
-------
jobdict : dict
    adds {
        'hostname': str,
        'hosttype': str,
        'job_name': str,
        'remote': str
    }
    removes {
        'cluster': str
    }
"""