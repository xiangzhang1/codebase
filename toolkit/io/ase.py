import ase, ase.io

import toolkit.functions
from toolkit.struct import Struct
from toolkit.functions import XS

"""ASE writes POSCAR4."""


def atoms_to_struct(atoms):
    return Struct(
        A=atoms.get_cell(),
        XS=XS(
            X=atoms.get_positions(),
            S=atoms.get_chemical_symbols()
        )
    )


def struct_to_atoms(struct):
    return ase.Atoms(
        symbols=toolkit.functions.XS['S'].values,
        cell=struct.A,
        positions=toolkit.functions.XS[['X', 'Y', 'Z']].values
    )


def read(*args, **kwargs):
    """ase.io.read but to struct"""
    atoms = ase.io.read(*args, **kwargs)
    return _atoms_to_struct(atoms)


def write(fname, struct, *args, **kwargs):
    """
    ase.io.write but from struct

    Writes POSCAR4.
    """
    atoms = _struct_to_atoms(struct)
    return ase.io.write(fname, atoms, *args, **kwargs)
