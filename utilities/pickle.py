import pickle
from typing import Any


def write(data: Any, filename: str):
    with open(filename, 'wb') as file:
        pickle.dump(obj=data, file=file, protocol=pickle.HIGHEST_PROTOCOL)


def read(filename: str) -> Any:
    with open(filename, 'rb') as file:
        return pickle.load(file=file)
