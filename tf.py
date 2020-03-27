class Op:
    """
    Example:
        >>> import operator
        >>> add = Op(operator.add)
        >>> add(1, 2).eval()
        3

    Attributes:
        function (PrimitiveType -> PrimitiveType [1]_):
        inputs (list of Tensor or PrimitiveType):
        output (Tensor);

    .. [1] Not necessarily primitiveType, but "regular" (i.e. non-Tensor) types.
    """

    def __init__(self, function):
        # Sets function
        self.function = function

    def __call__(self, *inputs):
        """Sets inputs. Returns output Tensor.

        Just as in Tensorflow, this does 2 things
        """
        self.inputs = inputs
        self.output = Tensor(op=self)
        return self.output

    def run(self):
        # Returns: PrimitiveType
        return self.function(*(i.eval() if i is Tensor else i for i in self.inputs))

class Tensor:
    """
    Attributes:
        op (Op): The Op whose output is this Tensor.
        value (PrimitiveType): Cached value.
    """
    def __init__(self, op, value=None):
        self.op = op
        self.value = value

    def eval(self):
        # Returns: PrimitiveType
        if self.value is None:
            self.value = self.op.run()
        return self.value