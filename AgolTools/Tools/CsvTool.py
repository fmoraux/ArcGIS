# -*- coding: utf-8
# coding: utf-8
##==========================================================================
##=====    Script         : Outils pour AGOL (CSV)                     =====
##=====    Author         : Flavie MORAUX (moraux.flavie@gmail.com)    =====
##=====    Version        : 1.0                                        =====
##=====    Date           : 01/01/2017                                 =====
##==========================================================================
# Exemple d'utilisation :
#
#   ==> Côté code :
#   csvDirPath = r"C:\Temp\ArcGIS\AgolTools\Resultat"
#   csv = CsvTool(csvDirPath, "Test")
#   csv.write("Colone1", "Colone2", "Colone3")
#   csv.writeLine("Value1;Value2;Value3;")
#
#   ==> Côté résultat "Test_20171202-090546.csv":
#   Colone1;Colone2;Colone3;
#   Value1;Value2;Value3;
# --------------------------------------------------
import os
import datetime
# --------------------------------------------------

class CsvTool(object):
    """Classe dédiée au fichier CSV"""

    # Formattage de date utilisé ( console et fichier de log)
    DATE_FORMAT = "%Y%m%d-%H%M%S"

    def __init__(self, dirPath, csvPrefix):
        """
        Initialisation
        :param dirPath: Chemin du dossier où générer le fichier
        :param csvPrefix: Prefixe de nom du fichier
        """
        self.__fileName = "{}_{}.csv".format(csvPrefix, datetime.datetime.now().strftime(CsvTool.DATE_FORMAT))
        self.__filePath = os.path.join(dirPath, self.__fileName)
        self.__file = open(self.__filePath, "w")
    ##end def __init__

    @property
    def filePath(self):
        """
        Chemin du fichierde log
        :return:
        """
        return self.__filePath
    ##end def user

    def write(self, *values):
        """
        Ajout d'un ensemble de valeurs au fichier
        :param values: Ensemble de valeurs à ajouter
        :return:
        """
        if(values!=None):
            line = ""
            for value in values:
                value = str(value).replace(";", ",")
                line += "{};".format(value)
            ##end for
            self.writeLine(line)
        ##end if
    ##end def write

    def writeLine(self, line):
        """
        Ajout d'une ligne au fichier
        :param line: Ligne à ajouter
        :return:
        """
        if(line!=None and len(line)>0):
            try:
                self.__file.write("{}\n".format(line))
                self.__file.flush()
            except Exception as ex:
                pass
        ##end if
    ##end def writeLine

##end class CsvTool
# --------------------------------------------------