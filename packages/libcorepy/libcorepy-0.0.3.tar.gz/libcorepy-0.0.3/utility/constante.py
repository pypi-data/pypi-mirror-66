"""
Es-Se carga todas las constante del paquete utility.

En-All utility package constants are loaded.
"""

import utility.msj as msj

MSJ=msj.Msj({
    "P01":"Prueba",
    "JS01":"Error converting dictionary to json",
    "JS02":"Error converting json to dictionary"
})

def GetMsj():
    """
    Es-Obtiene una instancia de la variable global de errores.
    
    En-Gets an instance of the global error variable.
    """
    global MSJ
    return MSJ
