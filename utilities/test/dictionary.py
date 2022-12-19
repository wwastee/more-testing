from typing import Any




def dict_zip(*dicts):
    """
    metodo zip per due o piu dizionari
    """
    if not dicts:
        return

    n = len(dicts[0])
    if any(len(d) != n for d in dicts):
        raise ValueError('arguments must have the same length')

    for key, first_val in dicts[0].items():
        yield key, first_val, *(other[key] for other in dicts[1:])
         


def dict_zip_intersection(*dicts):
    """
    metodo zip per due o piu dizionari sui soli elementi in comune
    """
    if not dicts:
        return

    keys = set(dicts[0]).intersection(*dicts[1:])
    for key in keys:
        yield key, *(d[key] for d in dicts)


def dict_zip_union(*dicts, fillvalue=None):
    """
    metodo zip per due o piu dizionari sui soli elementi non in comune
    """
    if not dicts:
        return

    keys = set(dicts[0]).union(*dicts[1:])
    for key in keys:
        yield key, *(d.get(key, fillvalue) for d in dicts)


def post_update(dict_obj: dict, level: list or tuple, value: Any, control: int = 0, dict_type=dict) -> dict:
    """
    funzione ricorsiva che dato una lista che reppresenta la catena di indici dentro un dizionario di dizionari,
    ne posiziona il valore nel posto corretto, andando a creare le chiavi se non esistono

    Args:
        dict_obj (dict): dizionario che si vuole popolare.
        level (list or tuple): lista delle chiavi dei dizionari innestati per arrivare alla posizone del valore
        value (any): valore da inserire del dizionario
        control (int, optional): valore di controllo per fermare il ricorsione. Default to 0.
        dict_type (optional): tipo di classe di dizionario che si vuole usare. Default to dict.

    Returns: dict
    """
    # se la chiave di quel livello non esiste, viene creato un dizionario vuoto come elemento di quella chiave
    if not (level[control] in list(dict_obj.keys())):
        dict_obj[level[control]] = dict_type()
    # viene incrementato il controllo
    control += 1
    # se si e' raggiunti il numero di iterazioni pari al numero di chiavi si interrompe la ricorsione
    if control >= len(level):
        # nel livello piu basso viene inserito il valore
        dict_obj[level[control-1]] = value
        return dict_obj
    # si ripete l'iterazione per i livelli piu bassi se ne rimangono
    dict_obj[level[control-1]] = post_update(dict_obj[level[control-1]], level, value, control)
    return dict_obj


def deep_pop(dict_obj: dict, level: list or tuple, control: int = 0) -> dict:
    """
    funzione ricorsiva che dato una lista che reppresenta la catena di indici dentro un dizionario di dizionari,
    ne elimina il valore dal posto corretto, andando a eliminare le chiavi dei livelli sopra se restano vuote dopo
    l'eliminazione

    Args:
        dict_obj (dict): dizionario che si vuole popolare.
        level (list or tuple): lista delle chiavi dei dizionari innestati per arrivare alla posizone del valore
        control (int, optional): valore di controllo per fermare il ricorsione. Default to 0.

    Returns: dict
    """
    # se la chiave di quel livello non esiste, viene creato un dizionario vuoto come elemento di quella chiave
    if not (level[control] in list(dict_obj.keys())):
        raise ValueError(f'{level[control]} key does not exist.')
    # viene incrementato il controllo
    control += 1
    # se si e' raggiunti il numero di iterazioni pari al numero di chiavi si interrompe la ricorsione
    if control >= len(level):
        # nel livello piu basso viene inserito il valore
        dict_obj.pop(level[control-1])
        return dict_obj
    # si ripete l'iterazione per i livelli piu bassi se ne rimangono
    dict_obj[level[control-1]] = deep_pop(dict_obj[level[control-1]], level, control)
    if dict_obj[level[control-1]].empty():
        dict_obj.pop(level[control - 1])
    return dict_obj

  
def deep_read(dict_obj: dict, level: list, control: int = 0) -> Any:
    """
    funzione ricorsiva che dato una lista che reppresenta la catena di indici dentro un dizionario di dizionari,
    ne trova il valore nel posto corretto e lo ritorna

    Args:
        dict_obj (dict): dizionario che si vuole popolare.
        level (list or tuple): lista delle chiavi dei dizionari innestati per arrivare alla posizone del valore
        control (int, optional): valore di controllo per fermare il ricorsione. Default to 0.

    Returns: Any
    """

    control += 1
#    print(control, level, dict_obj)
    # se si e' raggiunti il numero di iterazioni pari al numero di chiavi si interrompe la ricorsione
    if control >= len(level):
        # nel livello piu basso viene inserito il valore
        return dict_obj[level[control-1]]
    # si ripete l'iterazione per i livelli piu bassi se ne rimangono
    return deep_read(dict_obj[level[control-1]], level, control)

#da fare una volt finite le altre
class DeepDict(dict):
    """estensione della classe dizionario con funzionalita aggiunte per la gestione di dizionari dentro dizionari,
    con una profondita lunga a piacere. Il dizionario creato con questa classe e' a tutti gli effetti un
    tipo dict. Le funziolanita aggiuntive sono:
     - empty
     - deep_update
     - deep_pop
     - deep_read

     Examples:
         Esempio di struttura che si puo gestire con questa classe:
         {"level1":{
                    "level2": {
                                "level3": value3,
                                "level3_1": value3_1
                                },
                    "level2_1": value2_1
                    },
          "level1_2": value1_2
          }
     """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def empty(self) -> bool:
        """metodo che ritorna True o False in base se il livello di dizionario selezionato contiene o meno qualcosa.

        Returns: bool
        """
        return not bool(self)

    def deep_update(self, level: list or tuple, value: Any) -> None:
        """metodo che inserisce un valore in un livello specificato del dizionario se non e' gia presente, se e' gia
        presente lo sostituisce.

        Args:
            level (list or tuple): lista di chiavi che rappresentano il livello di profondita in cui si trova l'oggetto
                da inserire.
            value (Any): oggetto da inserire dentro al dizionario
        """
        post_update(self, level, value, dict_type=DeepDict)

    def deep_pop(self, level: list or tuple) -> None:
        """Metodo per eliminare un oggetto in nel dizionario a livelli. Una volta eliminato un oggetto, se il suo ramo
        non contiene piu nulla, anche i livelli superiori vengono eliminati. A differenza di un pop normale, non ritorna
        l'elemento eliminato.

        Args:
            level (list or tuple): lista di chiavi che identificano la posizione di un oggetto nel dizionario.
        """
        deep_pop(self, level)

    def deep_read(self, level: list or tuple) -> Any:
        """Metodo per leggere un elemento del dizionario, noto il livello in cui si trova.

        Args:
            level (list or tuple): lista di chiavi che identificano la posizione di un oggetto nel dizionario.

        Returns: Any
        """
        return deep_read(self, level)
