"""
Graph-parallel computation puts very stringent requirements on functions. We satisfy them here.

"Weird": `_to_vasp` shouldn't have to return anything. We had it return struct, because it's gonna be useful for method chaining.
"""

import os
from toolbox.barebones.functions import d_struct_to_vasp, to_slurm, submit, try_retrieve

def _to_vasp(d, struct, path, *control_dependencies):
    """
    Parameters
    ----------
    d : toolbox.barebones.objects.D
    struct : toolbox.barebones.objects.Struct
    path : str
        `os.chdir(); op()` isn't pure. Instead, specify path for every function.
    control_dependencies : list of PrimitiveType
        `with tf.control_dependencies([op]):`

    Returns
    -------
    toolbox.barebones.objects.Struct
        Exactly the same input struct.

    Example:
    >>> _ = d_struct_to_vasp(d, struct, path='/run/folder1', control_dependency=_)
    """
    os.chdir(path)
    d_struct_to_vasp(d, struct)
    return struct

def _to_slurm(d, struct, path, *control_dependencies):
    os.chdir(path)
    to_slurm(d)
    return struct

def _submit(struct, path, *control_dependencies):
    os.chdir(path)
    submit()
    return struct

def _try_retrieve(d, struct, path, *control_dependencies):
    os.chdir(path)
    try_retrieve(d)
    return struct