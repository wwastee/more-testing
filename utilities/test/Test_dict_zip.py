from dictionary import (
    dict_zip,
    dict_zip_intersection,
    dict_zip_union,
    post_update,
    deep_pop,
    deep_read,
    DeepDict
)
from shape import (shape_shifter)

import numpy as np
import pandas as pd


print(shape_shifter(np.array([10, 20])))

x = np.array([10, 20])
z = 1
y = 2



student = {"nome": "pino", "eta": "21", "soldi in tasca": "148"}
teacher = {"nome": "pino", "eta": "21", "soldi in tasca": "130", "relazione": "sposato", "figli": "due",}

student2 = {"nome": "pino", "eta": "21", "soldi in tasca": "148"}
teacher2 = {"nome": "pino", "eta": "21", "soldi in tasca": "130"}

student3 = {"nome": "pino", "eta": "21", "soldi in tasca": "148"}

dictT =  { 'dictA': {'chiave':{'key_1': '5'}, 'dictB': {'key_2': '10', 'key_3': '15'}}}
'''  
test = dict()
test['ciao'] = 1

test = {'ciao': 1}
test = DeepDict()
test.deep_update(['1','2','3'], 15)
test
'''

#creare test deepdict uguali a quelli gia fatti solo scrivere i dizionari con metodo deepdict
# tipo student(deepdict)= nome bla bla

"""
dict zip
"""


def test_is_wrong_zip():

    try:
        dict_zip(student, teacher)
    except Exception as e:
        print(e)
        assert e == "arguments must have the same length"


def test_is_right_zip():

    assert (set(dict_zip(student2, teacher2))) == {
        ("nome", "pino", "pino"),
        ("soldi in tasca", "148", "130"),
        ("eta", "21", "21"),
    }


"""
dict intesection
"""


def test_is_right_intersection():

    assert (set(dict_zip_intersection(student, teacher))) == {
        ("nome", "pino", "pino"),
        ("eta", "21", "21"),
        ("soldi in tasca", "148", "130"),
    }


def test_is_wrong_intersection():
    try:
        dict_zip_intersection(x, y)
    except Exception as e:
        print(e)
        assert e == ""


"""
dict union
"""


def test_is_right_union():

    assert (set(dict_zip_union(student, teacher))) == {
        ("figli", None, "due"),
        ("eta", "21", "21"),
        ("soldi in tasca", "148", "130"),
        ("nome", "pino", "pino"),
        ("relazione", None, "sposato"),
    }


"""
post update
"""


def test_is_right_post_update():

    assert (post_update(student, ["1", "2", "3", "4", "5"], 15)) == {
        "nome": "pino",
        "eta": "21",
        "soldi in tasca": "148",
        "1": {"2": {"3": {"4": {"5": 15}}}},
    }


'''
deep pop
'''

#def test_is_right_deep_pop():
    
    #assert (deep_pop(dictT, 'dictB')) == {'dictA': {'key_1': '5'}}
    
#def test_value_deep_pop():
    
 #   assert (deep_pop(dictT, ['']))
 
 
 
'''
deep read
'''
def test_right_deep_read():
    
    assert deep_read(dictT,['dictA', 'dictB']) == {'key_2': '10', 'key_3': '15'}
    
    

'''
deep dict
'''


def test_deep_dict():
    
    assert DeepDict(student3) == {'nome': 'pino', 'eta': '21', 'soldi in tasca': '148'}

def test_deepD_empty():
    
    assert DeepDict.empty(student3) == False

def test_deepD_update():
    
    assert DeepDict.deep_update(student3, '2', '5') == None
    
def test_deepD_read():
    
    assert DeepDict.deep_read(dictT,['dictA', 'dictB']) == {'key_2': '10', 'key_3': '15'}
    
    
'''
test shape
'''

import pandas as pd
import numpy as np
import pytest

from shape import shape_shifter

k = pd.DataFrame([1, 2, 3])

print(shape_shifter(k))

def test_shape_shifter_numpy():
    # test con un array NumPy
    x = np.array([1, 2, 3])
    assert (shape_shifter(x) == [1, 2, 3]).all()
    

def test_shape_shifter_list():
    # test con una lista
    x = [1, 2, 3]
    assert (shape_shifter(x) == [1, 2, 3]).all()
    

def test_shape_shifter_series():
    # test con una serie di Pandas
    x = pd.Series([1, 2, 3])
    assert (shape_shifter(x) == [1, 2, 3]).all()
    
#da dataframe in poi 

def test_shape_shifter_dataframe():
    # test con un dataframe di Pandas
    x = pd.DataFrame([1, 2, 3])
    assert (shape_shifter(x) == [1, 2, 3]).all()
    

def test_shape_shifter_invalid_tipologia():
    # test con un valore non valido per tipologia
    x = [1, 2, 3]
    with pytest.raises(NotImplementedError):
        shape_shifter(x, tipologia='non valido')

def test_shape_shifter_invalid_dimensions():
    # test con un dataframe di Pandas con più di una colonna
    x = pd.DataFrame([[1, 2], [3, 4], [5, 6]])
    with pytest.raises(ValueError):
        shape_shifter(x)

