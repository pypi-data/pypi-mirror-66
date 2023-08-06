"""
Es-Manipulacion de json funciones utility

En-Json manipulation utility functions
"""
import utility.constante as constante
import json
def DictToJson(data=dict()):
    """
    Es-Convierte un diccionario a json.
    
    En-Converts a dictionary to json.
    """
    try:
        return json.dumps(data, sort_keys=True)
    except Exception:
        return constante.GetMsj().GetError("JS01")


def JsonToDict(data=None):
    """
    Es-Convierte un json en diccionario
    
    En-Convert json to dictionary
    """
    try:
        return json.loads(data)
    except Exception:
        return constante.GetMsj().GetError("JS02")