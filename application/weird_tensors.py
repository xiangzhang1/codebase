from framework.graph_parallel import Tensor, Op

class Struct(Tensor):
    """
    Attributes
    ----------
    d : toolbox.barebones.objects.D
        Cached. Temporary.
    path : str
        Cached. Temporary.
    value : toolbox.barebones.objects.Struct
        Yes. It's intended to house a `Struct`.
    """

    def set_d(self, d):
        self.d = d
        return self

    def set_path(self, path):
        self.path = path
        return self

    def next_satellite(self):
        """`self.ns().ns().ns()` makes a chain of identical Tensors that all point to the same `toolbox.barebones.objects.Struct`."""
        tensor = Struct(op=None, )

    def to_vasp(self):
        """Make tensor. Link with operation."""
