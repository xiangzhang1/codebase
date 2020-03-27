class Tensor:
    """

    """
    def __init__(self, function=None, args=None, kwargs=None, value=None):
        self.function = function
        self.args = [] if args is None else args
        self.kwargs = {} if kwargs is None else kwargs
        self.value = value

    def get_value(self):
        if self.value is None:
            args = [a.get_value() for a in self.args]
            kwargs = {k:v.get_value() for k,v in self.kwargs.items()}
            self.value = self.function(*args, **kwargs)
        return self.value

def to_op(function):
    """
    Args:
        function (function: primitiveType [1]_ -> primitiveType):
    Returns:
        function: Tensor -> Tensor

    .. [1] Not necessarily primitiveType, just "regular" (i.e. non-Tensor) types.
    """
    def op(*args, **kwargs):
        return Tensor(function, args, kwargs, None)