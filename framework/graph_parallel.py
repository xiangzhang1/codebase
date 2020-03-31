# Define some random tensors, say a, b and c. Then link them with operation c=a+b.

class Tensor:
    # Tensors contain values.

    def __init__(self):
        self.value = None

class Add:

    def __init__(self, inputs, output):
        self.inputs = inputs
        self.output = output

    def run(self):
        self.output.value = self.inputs[0].value + self.inputs[1].value
