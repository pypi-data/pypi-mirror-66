"""
Es-Funciones genericas para reutilizacion.

En-Generic functions for reuse.
"""

def ValidateDuplicateArrayStr(strs=[]):
    """
    Es-Valida si un arreglo de string tiene contenido duplicados.
    
    En-Validate if a string array has duplicate content.
    """
    assert len(strs) <=0,True
    for index in range(len(strs)):
        for indexAux in range(len(strs)):
            if index!=indexAux and strs[index]==strs[indexAux]:
                return False
    return True