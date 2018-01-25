# -*- coding: utf-8
# coding: utf-8
##==========================================================================
##=====    Script         : Outils pour AGOL (CRYPTO)                  =====
##=====    Author         : Flavie MORAUX (moraux.flavie@gmail.com)    =====
##=====    Version        : 1.0                                        =====
##=====    Date           : 01/01/2017                                 =====
##==========================================================================
# Exemple d'utilisation :
#
#   ==> Côté code :
#   valueToEncypt = "Test"
#   print ("valueToEncypt={}".format(valueToEncypt))
#   valueEncrypted = CryptoTool.Encode(valueToEncypt)
#   print ("valueEncrypted={}".format(valueEncrypted))
#   valueDecrypted = CryptoTool.Decode(valueEncrypted)
#   print ("valueDecrypted={}".format(valueDecrypted))
#
#   ==> Côté résultat :
#   valueToEncypt=Test
#   valueEncrypted=b'VGVzdA=='
#   valueDecrypted=Test
# --------------------------------------------------
import base64
# --------------------------------------------------

class CryptoTool(object):
    """Classe dédiée au cryptage"""

    ENCODING = "utf-8"

    @staticmethod
    def Encode(value):
        """
        Encodage d'une valeur
        :param value: Valeur à encoder
        :return: Valeur encodée
        """
        encodeValue = None
        if(value != None):
            encodeValue = base64.b64encode(bytes(value, CryptoTool.ENCODING))
        ##end if
        return encodeValue
    ##end def Encode

    @staticmethod
    def Decode(encodeValue):
        """
        Décodage d'une valeur
        :param value: Valeur à décoder
        :return: Valeur décodée
        """
        value = None
        if (encodeValue != None):
            value = base64.b64decode(encodeValue).decode(CryptoTool.ENCODING)
        ##end if
        return value
    ##end def Decode

##end class CryptoTool
# --------------------------------------------------

# valueToEncypt = "Test"
# print ("valueToEncypt={}".format(valueToEncypt))
# valueEncrypted = CryptoTool.Encode(valueToEncypt)
# print ("valueEncrypted={}".format(valueEncrypted))
# valueDecrypted = CryptoTool.Decode(valueEncrypted)
# print ("valueDecrypted={}".format(valueDecrypted))