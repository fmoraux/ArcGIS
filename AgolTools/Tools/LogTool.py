# -*- coding: utf-8
# coding: utf-8
##==========================================================================
##=====    Script         : Outils pour AGOL (LOG)                     =====
##=====    Author         : Flavie MORAUX (moraux.flavie@gmail.com)    =====
##=====    Version        : 1.0                                        =====
##=====    Date           : 01/01/2017                                 =====
##==========================================================================
# Exemple d'utilisation : Test avec des log dans la console et dans un fichier de log
#
#   ==> Côté code :
#   logDirPath = r"C:\Temp\ArcGIS\AgolTools"
#   LogTool(printFlag=True, loggingFlag=True, loggingDirPath=logDirPath)
#   LogTool.Instance().addInfo("Ceci est un message")
#   LogTool.Instance().addWarning("Ceci est un warning")
#   LogTool.Instance().addError("Ceci est une erreur")
#
#   ==> Côté résultat :
#   [2017/12/01 10:51:04][INFO   ] Ceci est un message
#   [2017/12/01 10:51:04][WARNING] Ceci est un warning
#   [2017/12/01 10:51:04][ERROR  ] Ceci est une erreur
# --------------------------------------------------
import datetime
import logging
import os
# --------------------------------------------------

class LogTool(object):
    """Classe dédiée aux logs"""

    # Singleton
    __instance = None

    # Formattage de date utilisé ( console et fichier de log)
    DATE_FORMAT = "%Y%m%d-%H%M%S"
    # Formattage utilisé (fichier de log)
    LOGGING_FORMAT = "[%(asctime)s][%(levelname)s] %(message)s"
    # Niveau de log utilisé (fichier de log)
    LOGGING_LEVEL = logging.DEBUG

    def __new__(cls, *args, **kwargs):
        """
        Constructeur
        :param args:
        :param kwargs:
        :return:
        """
        if(LogTool.__instance is None):
            LogTool.__instance = object.__new__(cls)
        ##end if
        return LogTool.__instance
    ##end def __new__

    def __init__(self, printFlag=True, loggingFlag=False, loggingArcGisFlag=False, loggingDirPath=None, loggingPrefix="Log", loggingDateSufix=True):
        """
        Initialisation
        :param printFlag: Flag pour l'ajout des messages dans la console
        :param loggingFlag: Flag pour l'ajout des messages dans un fichier de log
        :param loggingArcGisFlag: Flag pour l'ajout des messages dans ArcGIS
        :param loggingDirPath : Chemin du dossier où générer les logs
        :param loggingPrefix : Préfixe utilisé pour nommé le fichier de log
        :param loggingDateSufix : Flag utilisé pour suffixer le nom du fichier de log avec la date courante
        """
        self.__printFlag = printFlag

        self.__loggingFlag = loggingFlag
        self.__loggingDirPath = loggingDirPath
        self.__loggingPrefix = loggingPrefix
        self.__loggingDateSufix = loggingDateSufix
        
        # On test l'import d'arcpy avant d'initialiser les logs ArcGIS
        try:
            import arcpy
        except:
            loggingArcGisFlag = False
        ##end try
            
        self.__loggingArcGisFlag = loggingArcGisFlag

        # Initialisation du logger
        if (self.__loggingFlag):
            if(self.__loggingDateSufix):
                loggingName = "{}_{}.log".format(self.__loggingPrefix, datetime.datetime.now().strftime(LogTool.DATE_FORMAT))
            else:
                loggingName = "{}.log".format(self.__loggingPrefix)
            ##end if
            
            loggingPath = os.path.join(self.__loggingDirPath, loggingName)
            logging.basicConfig(filename=loggingPath, level=LogTool.LOGGING_LEVEL, format=LogTool.LOGGING_FORMAT, datefmt=LogTool.DATE_FORMAT)
        ##end if
    ##end def __init__

    def addInfo(self, message):
        """
        Ajout d'un message d'information
        :param message:Message
        :return:
        """
        if(self.__printFlag):
            print("[{}][INFO   ] {}".format(self.__getDate(), message))
        ##end if
        if(self.__loggingFlag):
            logging.debug(message)
        ##end if
        if(self.__loggingArcGisFlag):
            arcpy.AddMessage(message)
        ##end if
    ##end def addInfo

    def addWarning(self, message):
        """
        Ajout d'un message d'alerte
        :param message:Message
        :return:
        """
        if(self.__printFlag):
            print("[{}][WARNING] {}".format(self.__getDate(), message))
        ##end if
        if(self.__loggingFlag):
            logging.warning(message)
        ##end if
        if(self.__loggingArcGisFlag):
            arcpy.AddWarning(message)
        ##end if
    ##end def addWarning

    def addError(self, message):
        """
        Ajout d'un message d'erreur
        :param message:Message
        :return:
        """
        if(self.__printFlag):
            print("[{}][ERROR  ] {}".format(self.__getDate(), message))
        ##end if
        if(self.__loggingFlag):
            logging.error(message)
        ##end if
        if(self.__loggingArcGisFlag):
            arcpy.AddError(message)
        ##end if
    ##end def addError

    def __getDate(self):
        """
        Retourne la date courante formatée
        :return: Date du jour formatée
        """
        return datetime.datetime.now().strftime(LogTool.DATE_FORMAT)
        ##end def getDate

    @staticmethod
    def Instance():
        """
        Retourne l'instance de classe
        :return:
        """
        return LogTool.__instance
    ##end def Instance
##end class LogTools
# --------------------------------------------------