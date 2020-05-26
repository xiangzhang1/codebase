from math import sqrt

import numpy as np
from scipy.spatial.distance import pdist

from codebase_023.toolkit.io.vasp import poscar2struct
from codebase_023.toolkit.struct import Struct, XS


def wulff_cut(unit_cell, unit_cell_metadata, wulff, symmetry='sc', pad=10, N=10):
    """
    Repeat unit cell indefinitely (N times) in all directions, wulff-cut it, then pad.

    Parameters
    ----------
    unit_cell : Struct
    unit_cell_metadata: str
    wulff : dict
        {
            (1, 0, 0): 3.1,
            (1, 1, 0): 4.0,
            (1, 1, 1): 5.7
        }
    symmetry : str, 'sc' or None
        (1, 0, 0) -> (-1, 0, 0)
    pad : float, unit is Angstrom
    N : int

    Returns
    -------
    Struct
    dict
        {
            'unit_cell': unit_cell_metadata,
            'wulff': wulff0,
            'symmetry': symmetry,
            'pad': pad,
            'N': N
        }

    Examples
    --------
    >>> odd_Pb = poscar2struct('odd_Pb.vasp')
    >>> wulff = {
    ...    (1, 0, 0): 3.1,
    ...    (1, 1, 1): 5.7
    ... }
    >>> struct, metadata = wulff_cut(odd_Pb, 'odd_Pb', wulff)
    """
    # image
    FX = unit_cell.FX
    S = unit_cell.XS.S.tolist()

    FX = np.concatenate(
        [
            FX + [ix, iy, iz]
            for ix in range(-N, N + 1)
            for iy in range(-N, N + 1)
            for iz in range(-N, N + 1)
        ],
        axis=0
    )
    X = np.dot(FX, unit_cell.A)
    S = np.array(S * (2 * N + 1) ** 3)

    # wulff cut
    ## symmetrize directions
    wulff0 = wulff.copy()    # StructWithMetadata
    if symmetry == 'sc':
        for ABC, D in wulff.copy().items():
            A, B, C = ABC
            wulff[(-A, B, C)] = wulff[(A, -B, C)] = wulff[(A, B, -C)] = wulff[(-A, -B, C)] = wulff[(-A, B, -C)] = wulff[
                (A, -B, -C)] = wulff[(-A, -B, -C)] = D
        for ABC, D in wulff.copy().items():
            A, B, C = ABC
            wulff[(A, C, B)] = wulff[(B, A, C)] = wulff[(B, C, A)] = wulff[(C, A, B)] = wulff[(C, B, A)] = D
    else:
        print("WARNING: no symmetry imposed, equivalent crystal direction families not added.")

    # normalize
    normalized = {}
    for ABC, D in wulff.items():
        ABC = np.dot(ABC, unit_cell.A)
        ABC = ABC / np.linalg.norm(ABC)
        normalized[tuple(ABC)] = D
    wulff = normalized

    # execute the wulff cut: Ax+By+Cz<=D
    masks = []
    for ABC, D in wulff.items():
        mask = np.dot(X, ABC) <= D
        masks.append(mask)
    mask = np.logical_and.reduce(masks)
    X = X[mask]
    S = S[mask]

    # clean up, pad
    X -= np.amin(X, axis=0)
    box = np.amax(X, axis=0)

    A = np.diag(box + 2 * pad)
    X += pad

    struct = Struct(A, XS(X,S))
    wulff0 = {''.join(map(str, k)):v for k,v in wulff0.copy().items()}  # (1,0,0): 1.7 is not json serializable
    metadata = {
        'unit_cell': unit_cell_metadata,
        'wulff': wulff0,
        'symmetry': symmetry,
        'pad': pad,
        'N': N
    }
    struct.sort()
    return struct, metadata


def wulff_cuts(unit_cell, unit_cell_metadata):
    """
    Notes
    -----
    NOT A FUNCTION.

    What do you mean?
    Wraps wulff_cut. Enumerates all posssible wulff_cut results.
    "All possible", like what?
    Well, read the first 6 lines of code.
    You see, you'll have to customize that. It's not arguments. Just modify it.

    Returns
    -------
    [
        {
            'struct': Struct,
            'metadata': dict
        }
    ]

    Examples
    --------
    >>> SMs = wulff_cuts(odd_Pb, 'odd_Pb')
    """
    # enumerate
    SMs = []
    for d100 in np.multiply([1, 2, 3, 4], 3.01):
        for d111 in np.linspace(
                start=3.01 * sqrt(3) / 2,
                stop=d100 * sqrt(3),
                num=20
        ):
            wulff = {
                (1, 0, 0): d100,
                (1, 1, 1): d111
            }
            struct, metadata = wulff_cut(unit_cell, unit_cell_metadata, wulff)
            SMs.append({
                'struct': struct,
                'metadata': metadata
            })
    # unique
    unique_SMs = []
    fingerprints = [np.sort(pdist(SM['struct'].XS[['X', 'Y', 'Z']])) for SM in SMs]
    for i, SM in enumerate(SMs):
        if not any(np.array_equal(fingerprints[i], fingerprints[j]) for j in range(i)):
            unique_SMs.append(SM)

    return unique_SMs