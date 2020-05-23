import ase, ase.io

import toolkit.functions
from toolkit.struct import Struct
from toolkit.functions import XS

"""ASE writes POSCAR4."""


def atoms2struct(atoms):
    return Struct(
        A=atoms.get_cell(),
        XS=XS(
            X=atoms.get_positions(),
            S=atoms.get_chemical_symbols()
        )
    )


def struct2atoms(struct):
    return ase.Atoms(
        symbols=toolkit.functions.XS['S'].values,
        cell=struct.A,
        positions=toolkit.functions.XS[['X', 'Y', 'Z']].values
    )