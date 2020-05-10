import ase, ase.io
from codebase.toolkit.just_enough_functions.barebones import axs_to_struct

def _atoms_to_struct(atoms):
    A = atoms.get_cell()
    X = atoms.get_positions()
    S = atoms.get_chemical_symbols()
    return axs_to_struct(A=A, X=X, S=S)

def _struct_to_atoms(struct):
    cell = struct.A
    positions = struct.X[['X','Y','Z']].values
    symbols = struct.X['S'].values
    return ase.Atoms(symbols=symbols, cell=cell, positions=positions)

def read(*args, **kwargs):
    """ase.io.read but to struct"""
    atoms = ase.io.read(*args, **kwargs)
    return _atoms_to_struct(atoms)

def write(filename, struct, *args, **kwargs):
    """ase.io.write but from struct"""
    atoms = _struct_to_atoms(struct)
    return ase.io.write(filename, atoms, *args, **kwargs)
