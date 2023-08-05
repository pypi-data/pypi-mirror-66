"""
Es-Funciones genericas para reutilizacion.

En-Generic functions for reuse.
"""

import random
import string
import uuid

def ValidateDuplicateArrayStr(strs=[]):
    """
    Es-Valida si un arreglo de string tiene contenido duplicados.
    
    En-Validate if a string array has duplicate content.

    test:

    >>> ValidateDuplicateArrayStr(["a","b"])
    True
    >>> ValidateDuplicateArrayStr(["a","b","b"])
    False
    """
    if  len(strs) <=0:
        return True
    for index in range(len(strs)):
        for indexAux in range(len(strs)):
            if index!=indexAux and strs[index]==strs[indexAux]:
                return False
    return True

def InStr(data="",*strs):
    """
    Es-Valida si un string esta dentros de una lista de string
    
    En-Validate if a string is inside a string list
    
    test:

    >>> InStr("a","a","b","c")
    True
    >>> InStr("a","b","c")
    False
    """
    if len(strs)<=0:
        return False
    for item in strs:
        if data==item:
            return True
    return False

def FilterStrs(strsOrig=[],strsFilter=[]):
    """
    Es-Se filtra una lista de string origenes con una lista de exclusion de string generando una lista nueva
    
    En-Filtering a list of string sources with a string exclusion list generating a new list

    test:

    >>> FilterStrs(["a","b","c"],["a"])
    ['b', 'c']
    """
    newData=[]
    for item in strsOrig:
        ind=True
        for itemAux in strsFilter:
            if item==itemAux:
                ind=False
        if ind:
            newData.append(item)
    return newData

def ReturnIf(expre=bool,a=None,b=None):
    """
    Es-Retorna un if ternario con una expresion boleana y dos retornos.
    
    En-Returns a ternary if with a boolean expression and two returns.

    test:

    >>> ReturnIf(5 > 4,"a","b")
    'a'
    """
    if expre:
        return a
    return b

def CharRandon(indUpper=True,digit=False,size=1):
    """
    Es-Envia letras aleatoria con un indicativo mayuscula true o false en minuscula indicativo si acepta digitos y el tamaño de la cadena.
    
    En-Send random letters with a capital letter true or lowercase callsign if you accept digits and the size of the string.
    """
    size=ReturnIf(size<=0,1,size)
    chars=ReturnIf(indUpper,string.ascii_uppercase,string.ascii_lowercase)+ReturnIf(indUpper,string.digits,"")
    return ''.join(random.choice(chars) for _ in range(size))

def UuidStr():
    """
    Es-Genera un uuid en cadena de caracteres.
    
    En-Generate a uuid in character string.
    """
    return str(uuid.uuid4())


if __name__ == '__main__':
    import doctest
    doctest.testmod()