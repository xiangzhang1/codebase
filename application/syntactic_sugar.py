from framework.graph_parallel import Tensor, Op

class Struct(Tensor):
    """
    Instead of
    >>> _ = d_struct_to_vasp(d, struct, path='/run/folder1', op_dependency=None)
    >>> _ = to_slurm(d, path='/run/folder1', op_dependency=_)

    we provide
    >>> poscar().set_d().set_path().to_vasp().to_slurm().retrieve().get_contcar().set_d()...

    at the cost of code weirdness. A special class of Tensors. Can create Ops using its methods. Op outputs same class of weird Tensors.
    """

    def set_path(self, path):
        # caches path for the next few function calls
        self.path = path
        return self

    def set_d(self, d):
        self.d = d
        return self

    def to_vasp(self):
        """
        As explained in the class docstring, this does `d_struct_to_vasp(d, struct, path='/run/folder1', op_dependency=None)`, but with less verbosity and more code stench. More of these to come.

        We have a long chain of Tensors, all of whose values point to the same `barebones.objects.struct` object.

        Make Tensor. Link with Op.
        """
        inputs = [self.d, self.value, self.path, self]
        output = self._next_struct()
        Op(to_vasp, inputs, output, name=None)
        return output

    def _next_struct(self):
        # To understand my purpose, substitute me into `to_vasp`. Don't wanna write the same line 1000 times. That's all.
        return Struct(op=None, value=self.value).set_path(self.path).set_d(self.d)

    def to_slurm(self):
        inputs = [self.d, self.path, self]
        output = self._next_struct()
        Op(to_slurm, inputs, output, name=None)
        return output

    def submit(self):
        inputs = [self.path, self]
        output = self._next_struct()
        Op(submit, inputs, output, name=None)
        return output

    def retrieve(self):
        inputs = [self.d, self.path, self]
        output = self._next_struct()
        Op(retrieve, inputs, output, name=None)
        return output