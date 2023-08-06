"""
Es-Paquete para funciones de encriptacion faciles y rapida.

En-Package for easy and fast encryption functions
"""
import hashlib
import utility.generic as gen
import utility.constante as c
import base64
from Crypto.Cipher import AES
from Crypto import Random
def HashSha256Str(key=""):
    """
    Es-Genera un hash 256 para un string.
    
    En-Generate a 256 hash for a string.
    """
    return hashlib.sha256(key.encode()).hexdigest()

def HashSha512Str(key=""):
    """
    Es-Genera un hash 512 para un string.
    
    En-Generate a 512 hash for a string.
    """
    return hashlib.sha512(key.encode()).hexdigest()

def HashMd5Str(key=""):
    """
    Es-Genera un hash md5 para un string.
    
    En-Generate a md5 hash for a string.
    """
    return hashlib.md5(key.encode()).hexdigest()

def GenToken(str="",ind512=False):
    """
    Es-Genera un token unico dependiendo del string el token lo genera con has256 por defecto pero contiene un indicativo si lo desea en 512.
    
    En-It generates a unique token depending on the string, the token generates it with has256 by default but contains a callsign if you want it in 512.
    """
    dataunique=gen.CharRandon(indUpper=False,digit=False,size=len(str))
    return gen.ReturnIf(ind512,HashSha512Str(dataunique),HashSha256Str(dataunique))


#Es-funciones lambda de ayuda para el cigrado estas son privadas
#En-lambda helper functions these are private
pad = lambda s: s + (c.BS - len(s) % c.BS) * chr(c.BS - len(s) % c.BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESEncryp:
    """
    Es-Clase que encripta en aes256 que contiene funciones de encriptado y desencriptado.
    
    En-Class that encrypts in aes256 that contains encryption and decryption functions.
    """
    def __init__( self, key ):
        self.key = key

    def Encrypt( self, raw="" ):
        """
        Es-Encripta un bloque de string a aes
        
        En-Encrypts a string block to aes
        """
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ) 

    def Decrypt( self, enc ):
        """
        Es-Desencripta un bloque de byte con la llave cargada
        
        En-Decrypt a byte block with the key loaded
        """
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))