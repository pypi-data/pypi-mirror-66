"""
Es-Manejo de mensajes genericos e personzalidos para proyectos

En-Handling of generic and personalized messages for projects
"""

import utility.error as err

class Msj():
    """
    Es-Clase para capturar mensajes de los sistema.

    En-Class to capture system messages.
    """
    def __init__(self,store=dict()):
        super().__init__()
        self.store=store

    def AddMsj(self, code="",msj=""):
        """
        Es-Agrega un mensaje ala coleccion.

        En-Add a message to the collection.
        """
        self.store[code]=msj
    
    def AddStore(self,store=dict()):
        """
        Es-Agrega una coleccion de mensajes.
        
        En-Add a collection of messages.
        """
        self.store=store
    
    def GetString(self, code=""):
        """
        Es-Envia un string de un mensaje guardado en la coleccion.
        
        En-Send a string of a message stored in the collection.
        """
        try:
            return self.store[code]
        except Exception:
            return ""

    def GetError(self, code=""):
        """
        Es-Envia un error Personalizado guardado en la coleccion.
        
        En-Submits a custom error saved in the collection.
        """
        try:
            return err.CustumerError(self.store[code])
        except Exception:
            return None
        
