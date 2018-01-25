# -*- coding: utf-8
#  coding: utf-8
##==========================================================================
##=====    Script         : Outils pour AGOL (CONFIG)                  =====
##=====    Author         : Flavie MORAUX (moraux.flavie@gmail.com)    =====
##=====    Version        : 1.0                                        =====
##=====    Date           : 01/01/2017                                 =====
##==========================================================================
# Exemple d'utilisation :
#
#   ==> Côté configuration :
#   [ORGANISATION]
#   url=http://www.arcgis.com
#
#   ==> Côté code :
#   # Initialisation
#   configPath = r"C:\Temp\ArcGIS\AgolTools\Configuration.ini"
#   config = ConfigTools(configPath)
#   # Lecture du fichier
#   config.readConfig()
#   # Récupération d'un paramètre
#   param = config.getValue("ORGANISATION", "url")
# --------------------------------------------------
import os

from configparser import ConfigParser
# --------------------------------------------------
class ConfigTools(object):
    """Classe dédiée au fichier de configuration"""

    def __init__(self, configPath):
        """
        Initialisation de la configuration
        :param configPath: Chemin du fichier de configuration
        """
        self.__configPath = configPath
        self.__readConfig()
    ##end def __init__

    def __readConfig(self):
        """
        Lecture du fichier de configuration
        :return:
        """
        self.__configDct = {}

        if(self.__configPath != None and os.path.exists(self.__configPath)):
            config = ConfigParser()
            config.readfp(open(self.__configPath))

            # Parcours des sections ([BLABLA])
            for section in config.sections():

                # Parcours des clés de la section (BLABLA=VALUE)
                for (key, value) in config.items(section):
                    #TODO Résoudre le problème de la mise en minscule de la clé
                    #En attendant on ruse en repassant en majuscule
                    # Implique que les clés soient en majuscule dans le fichier
                    key = key.upper()
                    self.__configDct[(section, key)] = value
                ##end for

            ##end for
        ##end if
    ##end def readConfig

    def getValue(self, section, key):
        """
        Retourne une valeur issue de la configuration
        :param section: Section de configuration
        :param key: Clé de configuration
        :return: Valeur ou None
        """
        value = None
        if(section != None and len(section) != 0 and key != None and len(key) != 0 and self.__configDct != None):
            if((section, key) in self.__configDct.keys()):
                value = self.__configDct[(section, key)]
            ##end if
        ##end if
        return value
    ##end def getValue

##end class ConfigTools
# --------------------------------------------------