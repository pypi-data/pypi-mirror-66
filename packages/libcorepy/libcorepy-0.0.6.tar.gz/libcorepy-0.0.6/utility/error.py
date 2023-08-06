"""
Es-Archivo de manejo de errores

En-Error handling file
"""


class CustumerError(Exception):
    """
    Es-Ingresa una excepcion personalizada.
    
    En-Enter a custom exception.
    """
    def __init__(self,message=""):
        self.message=message

    def __str__(self):
        return 'Error {message}'.format(message=self.message)