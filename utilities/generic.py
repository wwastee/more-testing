import numpy as np
import pandas as pd
from typing import List, Literal


def isalmostequal(element1: int or float or pd.DataFrame or pd.Series,
                  element2: int or float or pd.DataFrame or pd.Series,
                  order: int = 6, ignore_index=False, verbose: bool = False) -> bool:
    """
    funzione che verifica l'uguaglianza tra 2 elementi con un ordine di approssimazione
    il valore di ordine indica il numero di decimali che vogliono essere usati come accuratezza

    Args:
        element1 (int or float or pd.DataFrame or pd. Series): primo elemento da confrontare
        element2 (int or float or pd.DataFrame or pd. Series): secondo elemento da confrontare
        order (int, optional): numero di decimali di accuratezza. Default to 6.
        ignore_index (bool, optional): nel caso in cui gli lementi fossero dei pandas si puo decidere di paragonarli
            ignorando i valore degli inidici e delle colonne.
        verbose (bool, optional): reportistica del flusso

    Returns: True or False, in base a se i 2 elementi sono uguali dentro l'accuratezza scelta.
    """
    # calcolo la risoluzione con cui si cerca l'uguaglianza tramite l'ordine di approssimazione dato
    resolution = 1 / (10 ** order)

    # controllo che gli ingressi siano supportati e li sostituisco con variabili locali, cosi da non modificare
    # il dato originale se è un valore numerico faccio le operazioni standard per verificare la somiglianza dentro
    # l'ordine di approssimazione
    if ((isinstance(element1, int)) or isinstance(element1, float)) and (
            (isinstance(element2, int)) or isinstance(element2, float)):
        if verbose: print('gli elementi sono numeri')
        obj1, obj2 = element1, element2
        diff = np.abs(obj1 - obj2)
        if diff < resolution:
            return True
        else:
            if verbose: print('gli oggetti non sono uguali per uno scarto di ', diff)
            return False

    # se è un pandas controllo gli indici separatamente dai valori
    elif (isinstance(element1, pd.DataFrame) or isinstance(element1, pd.Series)) and (
            isinstance(element2, pd.DataFrame) or isinstance(element2, pd.Series)):
        if verbose: print('gli elenti sono pandas')
        obj1 = element1.copy()
        obj2 = element2.copy()
        # se uno degli oggetti è una serie, viene trasformata in un dataframe
        if isinstance(obj1, pd.Series): obj1 = obj1.to_frame()
        if isinstance(obj2, pd.Series): obj2 = obj2.to_frame()

        # se richiesto ignoro gli indici, se no verifico che questi siamo uguali
        if not ignore_index:
            if not obj1.index.equals(obj2.index) or not obj1.columns.equals(obj2.columns):
                if verbose: print('gli indici sono diversi')
                return False
        # se non si vuole controllare gli indici li forzo ad essere uguali
        else:
            # se i 2 oggetti hanno una dimensione deiversa dico che sono diversi
            if obj1.shape != obj2.shape:
                if verbose: print('la dimensione dei due oggetti è diversa')
                return False
            # forzo gli indici ad essere uguali
            obj2.index = obj1.index
            obj2.columns = obj1.columns

        # se le colonne non sono numeriche vengono trattate separatamente
        obj1_num = obj1.select_dtypes(include=[float, int])
        obj2_num = obj2.select_dtypes(include=[float, int])

        obj1_not_num = obj1.loc[:, obj1.columns.difference(obj1_num.columns, sort=False)]
        obj2_not_num = obj2.loc[:, obj2.columns.difference(obj2_num.columns, sort=False)]

        if obj1_not_num.shape != obj2_not_num.shape:
            if verbose: print('ci sono un numero diverso di colonne numeriche e non numeriche')
            return False
        else:
            if not obj1_not_num.equals(obj2_not_num):
                if verbose: print('gli oggetti hanno colonne non numeriche con valori diversi')
                return False

        diff = obj1_num - obj2_num
        num_non_equal = (diff > resolution).sum().sum()
        # se esiste almeno un valore che non rispetta l'uguaglianza do il False
        if num_non_equal > 0:
            if verbose: print('il numero di oggetti numerici non uguali è', num_non_equal)
            return False
        else:
            return True

    else:
        raise Exception("not supported format of entries")


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


def chunks(lst: list, n: int) -> List[list]:
    """
    metodo per suddividere una lista madre in una nuova lista composta di sotto liste piu piccole

    Args:
        lst (list): lista da suddividere
        n (int): numero di componenti dentro ogni sotto suddivisione

    Returns:
        chunked_list (dict): lista di liste, ogni elemento e' una lista con il numero di oggetti indicati
            provenienti dalla lista madre
    """
    chunked_list = []
    for i, ii in enumerate(range(0, len(lst), n)):
        chunked_list.append(lst[ii:ii + n])
    return chunked_list


def concat_light(df: pd.DataFrame or pd.Series, creator: bool = True, axis: Literal[0, 1] = 0,
                 file_format: str = 'txt', include_index = False, include_header = True):
    """
    Metodo che svrutta la scrittura su file in modalita append per concatenare i dati.
    Alla prima iterazione va chiamato in modalita creator = True, dalla seconda in poi creator = False.
    Se si usa axis = 1, il risultato viene scritto trasposto.

    Args:
        df (pd.DataFrame or pd.Series): dataframe con i valori da concatenare
        creator (bool, optional): If true viene creato il file o rimpiazzato il file gia esistente, if False viene
            appeso il dato al file creato quando creator = True. Default to True.
        axis (int, optional): if 0 il file viene caricato cosi come è e le successive append vengono fatte aggiungendo
            nuove righe, if 1 il file viene prima trasposto e poi le successive append vengono fatte aggiungendo nuove
            righe ma dopo aver trasposto il dataframe. Default to 0.
        file_format (str, optional): estensione su con cui salvare il file temporaneo. Default to 'txt'.
        include_index (bool, optional): viene salvato anche l'indice
        include_header (bool, optional): viene salvato anche l'indice delle colonne
    """
    if axis == 1:
        df = df.T
        temp_include_header = include_header
        include_header = include_index
        include_index = temp_include_header

    if creator:
        df.to_csv('temp_concat.' + file_format, mode='w', index=include_index, header=include_header)
    else:
        df.to_csv('temp_concat.' + file_format, mode='a', index=include_index, header=False)


def line_generator(num_points: int = None, step: float = None, start: float = None, stop: float = None,
                   rounding: int = None) -> list:
    """
    funzione che produce una lista di numeri successivi una volta scelti i parametri di riempimento

    Args:
        num_points (int, optional): numero di punti nella lista
        step (float, optional): step tra i punti
        start (float, optional): valore di partenza della lista
        stop (float, optional): valore finale della lista
        rounding (int, optional): valore di arrotondamento sugli elementi della lista

    Returns: list
    """

    if start is None and stop is None and step is not None and num_points is not None:
        # step + num_pints
        res = [i * step for i in range(num_points)]

    elif start is not None and stop is not None and num_points is not None and step is None:
        # start + stop + num_points
        res = list(np.linspace(start, stop, num_points, endpoint=True))

    elif start is not None and stop is not None and step is not None and num_points is None:
        # start + stop + step
        res = list(np.arange(start, stop, step))

    elif start is None and stop is None and step is None and num_points is not None:
        # num_points
        res = [i for i in range(num_points)]

    elif start is not None and stop is None and step is not None and num_points is not None:
        # start + step + num_points
        res = [start + i*step for i in range(num_points)]

    elif start is None and stop is not None and step is not None and num_points is not None:
        # start + step + num_points
        res = [stop - (num_points - i - 1)*step for i in range(num_points)]

    else:
        raise ValueError('wrong parameters selection')

    if rounding is not None:
        res = [round(i, rounding) for i in res]

    return res


def mode(array: list or np.ndarray or pd.Series or pd.DataFrame, num_bin: int = None, axis: int = 0) -> float or pd.DataFrame:
    """
    funzione che calcola la moda di una distribuzione andando a verificare quale è il punto piu alto dell'istogramma
    dei dati. Metodo piu corretto rispetto che verificare il valore che si presenta piu volte, se si lavora con
    valori continui

    Args:
        array (list or np.ndarray or pd.Series or pd.DataFrame): lista di valori e dataframe.
        num_bin (int, optional): Se impostato, l'istogramma usato per definire la distribuzione usera il numero di
            bin da num_bin, se non viene impostato il numero di bin viene calcolato automaticamente. Default to None.
        axis (int, optional): Se si sta calcolando la moda di un dataframe, questo parametro definisce la direzione
            su cui viene calcolata la moda. Con axis = 0 viene calcolcata la moda di ogni colonna, con axis = 1 viene
            calcolata la moda di ogni riga. Default to 0.

    Returns: float or pd.DataFrame

    """
    def _mode(_array):
        if num_bin is None:
            edge = np.histogram_bin_edges(_array, bins='fd')
            if len(edge) < 10: edge = 10
        else:
            edge = num_bin
        counts, bin_edges = np.histogram(_array, bins=edge)
        counts = counts.astype(np.float)
        bin_size = bin_edges[1] - bin_edges[0]
        bin_centre = []
        for i in range(len(bin_edges) - 1):
            bin_centre.append(bin_edges[i] + bin_size / 2)
        bin_centre = np.asarray(bin_centre)
        df_hist = pd.DataFrame(bin_centre, columns=['x'])
        df_hist['conteggi'] = counts
        df_hist = df_hist[df_hist['conteggi'] > 0]
        x_picco = df_hist[df_hist['conteggi'] == df_hist['conteggi'].max()]['x'].values[0]
        return x_picco
    if isinstance(array, list) or isinstance(array, np.ndarray) or isinstance(array, pd.Series):
        x_mode = _mode(array)
    else:
        x_mode = array.apply(_mode, axis = axis)
    return x_mode