# Define some random tensors, say a, b and c. Then link them with operation c=a+b.

class Tensor:
    """Tensors contain values.

    Attributes
    ----------
    op : Op
        The Op whose output is this Tensor.
    value : PrimitiveType
        None if hasn't been evaluated.
    """

    def __init__(self, op, value):
        super().__init__()      # to be subclassed by application.graph_parallel_compat.Struct
        self.op = op
        self.value = value

    def eval(self):
        if self.value is None:
            self.value = self.op.run()
        return self.value

class Op:
    """Ops link Tensors.

    Examples
    --------
    Not unlike `tf.layers.dense`::

        >>> add = Op(operator.add, inputs=[1,2], output=None, name='add:0')
        >>> add.run()
        3

    Except that `tf.add` creates an Op, but instead of returning that Op, returns its output Tensor. You can do that confusing shit here too:

        >>> def add(x, y):
        ...     return Op(add, inputs=[x, y], output=None, name='x').output
        >>> a = add(1, 2)
        >>> a.eval()
        3

    Attributes
    ----------
    function : function(PrimitiveType -> PrimitiveType)
    inputs : list of PrimitiveType or Tensor
    output : Tensor
    name : str
    """

    def __init__(self, function, inputs, output, name):
        self.function = function
        self.inputs = inputs
        if output is None:
            self.output = Tensor(op=self, value=None)
        else:
            self.output = output
            output.op = self
        self.name = name

    def run(self):
        # Returns: PrimitiveType
        return self.function(*(i.eval() if i is Tensor else i for i in self.inputs))