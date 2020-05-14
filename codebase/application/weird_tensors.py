from codebase.application.weird_pure_functions import _to_vasp, _to_slurm, _submit, _try_retrieve
from codebase.framework.graph_parallel import Tensor, Op


class Struct(Tensor):
    """
    Examples
    --------
import codebase.toolkit.contrib.templates    >>> codebase.toolkit.contrib.templates.retrieve().get_contcar().set_d()...

    Attributes
    ----------
    d : toolkit.contrib.objects.D
        Cached. Temporary.
    path : str
        Cached. Temporary.
    value : toolkit.contrib.objects.Struct
        Yes. It's intended to house a `Struct`.
    """

    def cache_d(self, d):
        self.d = d
        return self

    def cache_path(self, path):
        self.path = path
        return self

    def next_satellite(self):
        """`self.ns().ns().ns()` makes a chain of identical Tensors whose `value` attributes all point to the same `toolkit.contrib.objects.Struct`."""
        return Struct(value=self.value).cache_d(self.d).cache_path(self.path)

    def to_vasp(self):
        """Make tensor. Link with operation."""
        tensor = self.next_satellite()
        op = Op(_to_vasp, inputs=[self.d, self, self.path], output=tensor)
        return tensor

    def to_slurm(self):
        tensor = self.next_satellite()
        op = Op(_to_slurm, inputs=[self.d, self, self.path], output=tensor)
        return tensor

    def submit(self):
        tensor = self.next_satellite()
        op = Op(_submit, inputs=[self, self.path], output=tensor)
        return tensor

    def retrieve(self):
        tensor = self.next_satellite()
        op = Op(_try_retrieve, inputs=[self.d, self, self.path], output=tensor)
        return tensor