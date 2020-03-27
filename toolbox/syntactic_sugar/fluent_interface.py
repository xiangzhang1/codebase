from toolbox.barebones.functions import d_struct_to_vasp
from toolbox.barebones.objects import Struct as BarebonesStruct

class Struct(BarebonesStruct):
    # Struct().to_vasp(d).to_slurm(d).submit(d).retrieve(d)

    def to_vasp(self, d):
        d_struct_to_vasp(d, self)
        return self