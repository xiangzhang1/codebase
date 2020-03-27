from toolbox.barebones.functions import d_struct_to_vasp, to_slurm, submit, is_complete, retrieve
from toolbox.barebones.objects import Struct as BarebonesStruct

class Struct(BarebonesStruct):
    # Struct().to_vasp(d).to_slurm(d).submit().retrieve(d)

    def to_vasp(self, d):
        d_struct_to_vasp(d, self)
        return self

    def to_slurm(self, d):
        to_slurm(d)
        return self

    def submit(self):
        submit()
        return self

    def is_complete(self, d):
        return is_complete(d)

    def retrieve(self, d):
        retrieve(d)
        return self