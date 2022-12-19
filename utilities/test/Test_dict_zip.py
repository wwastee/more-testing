from dictionary import dict_zip , dict_zip_intersection , dict_zip_union

x = 1
y = 2

student = {'nome': 'pino', 'eta': '21', 'soldi in tasca': '148'}
teacher = {'nome': 'pino', 'eta': '21', 'soldi in tasca': '130', 'relazione': 'sposato', 'figli': 'due'}

student2 = {'nome': 'pino', 'eta': '21', 'soldi in tasca': '148'}
teacher2 = {'nome': 'pino', 'eta': '21', 'soldi in tasca': '130'}


'''
dict zip
'''
def test_is_wrong_zip() :
    
    try:
        dict_zip(student, teacher)
    except Exception as e:
        print(e)
        assert e == 'arguments must have the same length'
        

def test_is_right_zip():
    
   assert(set(dict_zip(student2, teacher2))) == {('nome', 'pino', 'pino'), ('soldi in tasca', '148', '130'), ('eta', '21', '21')}
    
'''
dict intesection
'''
    
def test_is_right_intersection():
    
    assert(set(dict_zip_intersection(student, teacher))) == {('nome', 'pino', 'pino'), ('eta', '21', '21'), ('soldi in tasca', '148', '130')}
    
def test_is_wrong_intersection():
    try:
        dict_zip_intersection(x,y)
    except Exception as e:
        print(e)
        assert e == ''
        
'''
dict union
'''

def test_is_right_union():
    
   assert(set(dict_zip_union(student, teacher))) == {('figli', None, 'due'), ('eta', '21', '21'), ('soldi in tasca', '148', '130'), ('nome', 'pino', 'pino'), ('relazione', 
None, 'sposato')}
    
#print (set(dict_zip(student2, teacher2)))
#print(set(dict_zip_intersection(x, y)))
#print (set(dict_zip_union(student, teacher)))

