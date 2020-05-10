import os
import pandas as pd

periodic_table = pd.read_excel('/utils/periodic_table2.xlsx')

def lookup(symbol, column):
    """
    Args:
        symbol (str): 'Pb'
        column (str): 'pot_encut'
    """
    return periodic_table.loc[periodic_table.symbol == symbol, column].values[0]