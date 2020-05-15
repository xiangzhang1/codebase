import ase, ase.io
from toolkit.objects import Struct
from toolkit.optional.functions.struct import XS


def _atoms_to_struct(atoms):
    return Struct(
        A=atoms.get_cell(),
        XS=XS(
            X=atoms.get_positions(),
            S=atoms.get_chemical_symbols()
        )
    )


def _struct_to_atoms(struct):
    return ase.Atoms(
        symbols=struct.XS['S'].values,
        cell=struct.A,
        positions=struct.XS[['X', 'Y', 'Z']].values
    )


def read(*args, **kwargs):
    """ase.io.read but to struct"""
    atoms = ase.io.read(*args, **kwargs)
    return _atoms_to_struct(atoms)


def write(filename, struct, *args, **kwargs):
    """
    ase.io.write but from struct

    Writes POSCAR4.
    """
    atoms = _struct_to_atoms(struct)
    return ase.io.write(filename, atoms, *args, **kwargs)
