import pandas as pd

def array2string(arr):
    """
    Parameters
    ----------
    arr : 2D np.array

    Returns
    -------
    str
        1.0000  2.0000  3.0000
        4.0000  5.0000  6.0000
    """
    return pd.DataFrame(arr).to_string(header=False, index=False)

def struct_to_poscar5(struct):
    string = """struct_to_poscar5
    
    """
