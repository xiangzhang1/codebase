class Op:

    def __init__(self, function):
        self.function = function

    def __call__(self, *inputs):
        self.inputs = inputs
        self.output = Tensor(self)
        return self.output

    def run(self):
        return self.function(*(i.eval() if i is Tensor else i for i in self.inputs))

class Tensor:

    def __init__(self, op, value=None):
        self.op = op
        self.value = value

    def eval(self):
        if self.value is None:
            self.value = self.op.run()
        return self.value

