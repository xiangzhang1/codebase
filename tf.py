class Op:
    """
    Examples
    -------
    Clumsily emulates `tf.Operation`_ (or perhaps `tf.layers.dense`)::

        >>> add = Op(operator.add, inputs=[1,2], name='add:0')
        >>> add.run()
        3

    `tf.add` creates an op, but instead of returning that op, returns its output tensor. You can do that confusing shit too::

        >>> def add(x, y):
        ...     return Op(add, inputs=[x, y], name='x').output
        >>> a = add(1, 2)
        >>> a.eval()
        3

    Attributes
    ----------
    function : function(PrimitiveType -> PrimitiveType [1]_)
    inputs : list of Tensor or PrimitiveType
    output : Tensor
    name : str

    .. [1] Not necessarily primitiveType, but "regular" (i.e. non-Tensor) types.
    """

    def __init__(self, function, inputs, name):
        self.function = function
        self.inputs = inputs
        self.output = Tensor(op=self, value=None)
        self.name = name

    def run(self):
        # Returns: PrimitiveType
        return self.function(*(i.eval() if i is Tensor else i for i in self.inputs))

class Tensor:
    """
    Attributes
    ----------
    op : Op
        The Op whose output is this Tensor.
    value :PrimitiveType
        Cached value.
    """
    def __init__(self, op, value):
        self.op = op
        self.value = value

    def eval(self):
        """
        Returns
        -------
        PrimitiveType:
            Result of corresponding op. If value is not None, returns value instead.
        """
        if self.value is None:
            self.value = self.op.run()
        return self.value