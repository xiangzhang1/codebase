import ase, ase.io
from codebase.toolkit.objects_ import axs_to_struct

def _atoms_to_struct(atoms):
    return axs_to_struct(
        A = atoms.get_cell(),
        X = atoms.get_positions(),
        S = atoms.get_chemical_symbols()
    )

def _struct_to_atoms(struct):

    return ase.Atoms(
        symbols = struct.XS['S'].values,
        cell = struct.A,
        positions = struct.XS[['X','Y','Z']].values
    )

def read(*args, **kwargs):
    """ase.io.read but to struct"""
    atoms = ase.io.read(*args, **kwargs)
    return _atoms_to_struct(atoms)

def write(filename, struct, *args, **kwargs):
    """ase.io.write but from struct"""
    atoms = _struct_to_atoms(struct)
    return ase.io.write(filename, atoms, *args, **kwargs)
