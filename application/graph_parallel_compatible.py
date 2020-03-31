import os

from toolbox.barebones.functions import d_struct_to_vasp, to_slurm, submit, retrieve

def make_function_gp_compatible(func):
    """Decorator. Modifies toolbox functions to be graph-parallel compatible.

    Clean, but verbose af. I doubt if anyone would be arsed to use them.

    Examples
    --------
    >>> to_vasp(d, struct)
    None
    >>> _to_vasp = make_function_gp_compatible(to_vasp)
    >>> _to_vasp(d, struct, path, dependency)
    1

    Notes
    -----
    What is "graph-parallel compatible", and why do I need to modify toolbox functions? See README.

    About `return 1`::

        True, the return variable does nothing but resolves dependency. But if we let `to_vasp` return None, a future `Tensor.eval` will result in `Tensor.value=None`.
        Which is bad because `T.value=None` means "Tensor has yet to be evaluated", not "Tensor evaluated, evaluated value happens to be None". Thus `return 10086`.
        See `framework.graph_parallel.Tensor.eval`.
    """
    def newfunc(*args, path, op_dependency, **kwargs):
        os.chdir(path)
        func(*args, **kwargs)
        return 10086
    return newfunc

to_vasp, to_slurm, submit, retrieve = map(make_function_gp_compatible, (d_struct_to_vasp, to_slurm, submit, retrieve))

