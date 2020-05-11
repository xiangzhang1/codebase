import pandas as pd


def XS(X, S):
    """
    No such thing as pd.DataFrame(data1, columns1, data2, columns2).

    Used to be axs_to_struct(A, X, S). But consider this use case:

        class MetadataStruct(Struct):
            pass

        axs_to_struct(A, X, S)

    As Bob Martin says, a good architecture allows you to postpone decision making as long as possible.
    """
    return pd.concat([
        pd.DataFrame(X, columns=('X', 'Y', 'Z')),
        pd.Series(S, name='S')
    ], axis=1)
