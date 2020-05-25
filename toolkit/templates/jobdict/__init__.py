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
        'uuid': str,
        'hostname': str,    # haswell -> cori
        'hosttype': str,
        'local': str,       # submit, retrieve
        'remote': str,      # /scratch/xzhang1
        'job_name': str
    }
    removes {
        'cluster': str
    }
"""