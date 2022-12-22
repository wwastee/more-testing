import pandas as pd
import numpy as np 
from typing import Literal
#prende 2 argomenti: x e tipologia da lasciare intoccata

def shape_shifter(x: pd.DataFrame or pd.Series or np.array or list, tipologia: Literal['numpy', 'numpy-1'] = 'numpy'):
    
    """
    metodo che garantisce la formattazione dei dati indipendentemente dal formato di origine

    Args:
        x (pd.DataFrame or pd.Series or np.array): vettore di ingresso
        tipologia (['numpy', 'numpy-1'], optional): Default to numpy

    Returns:
        X (np.array): nel formato corretto
    """

    def shape_to_numpy(_x):
        # se è un pandas df lo trasformo in una serie
        if isinstance(_x, pd.DataFrame) and _x.shape[1] == 1:
            _x = _x.iloc[:, 0]

        # se il df ha piu di una riga do un errore
        elif isinstance(_x, pd.DataFrame) and _x.shape[1] > 1:
            if _x.shape[0] == 1:
                _x = _x.iloc[0, :]
            else:
                raise ValueError('dimensione di x sbagliata')

        # se è un pandas serie lo trasformo in un numpy
        if isinstance(_x, pd.Series): _x = _x.to_numpy()

        # se è numpy ma con la dimensione sbagliata lo converto
        if isinstance(_x, np.ndarray) and len(np.shape(_x)) > 1 and np.shape(_x)[0] > 1:
            _x = _x[:, 0]
        elif isinstance(_x, np.ndarray) and len(np.shape(_x)) > 1 and np.shape(_x)[1] > 1:
            _x = _x[0, :]

        # se invece è una lista
        if isinstance(_x, list):
            _x = np.array(_x)
        return _x

    if tipologia == 'numpy':
        return shape_to_numpy(x)
    elif tipologia == 'numpy-1':
        return shape_to_numpy(x).reshape(-1, 1)
    else:
        raise NotImplementedError