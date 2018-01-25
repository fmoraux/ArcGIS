# -*- coding: utf-8
# coding: utf-8
##==========================================================================
##=====    Script         : Outils pour AGOL                           =====
##=====    Author         : Flavie MORAUX (moraux.flavie@gmail.com)    =====
##=====    Version        : 1.0                                        =====
##=====    Date           : 01/01/2017                                 =====
##==========================================================================
import  datetime
import os
import getpass

from Tools.AgolToolsSDK import AgolToolsSDK
from Tools.ConfigTool import ConfigTools
from Tools.CryptoTool import CryptoTool
from Tools.CsvTool import CsvTool
from Tools.LogTool import LogTool
# --------------------------------------------------

DEFAULT_DIR_LOG = "Log"
DEFAULT_DIR_RESULT = "Result"

def __CheckParamFolder(folder, folderDefault):
    """
    Vérification d'un paramètre de type dossier
    :param folder: Chemin à vérifier
    :param folderDefault: Nom de dossier par défaut
    :return:
    """
    checkFolder = None
    if (os.path.isabs(folder)):
        # Cas d'un chemin absolu
        checkFolder = folder
    elif (folder != None and len(folder)>0):
        # Cas d'un chemin relatif
        scriptDirPath = os.path.dirname(os.path.realpath(__file__))
        checkFolder = os.path.join(scriptDirPath, folder)
    else:
        # Cas d'un chemin non renseigné
        scriptDirPath = os.path.dirname(os.path.realpath(__file__))
        checkFolder = os.path.join(scriptDirPath, "Log")
    #end if
    return checkFolder
##end def __CheckParamFolder

# --------------------------------------------------

def CopyUserItems(loggingArcGisFlag=False, agolUrl=None, agolUserName=None, agolUserPassword=None, agolUrl2=None, agolUserName2=None, agolUserPassword2=None):
    """
    Copie du contenu d'un utilisateur nommé d'une organisation à une autre
    :param loggingArcGisFlag: Flag pour l'ajout des messages dans ArcGIS
    :param agolUrl : Url de l'organisation ArcGIS (si utilisation depuis une TBX ArcGIS Pro)
    :param agolUserName : Identifiant de l'utilisateur nommé (si utilisation depuis une TBX ArcGIS Pro)
    :param agolUserPassword : Mot de passe de l'utilisateur nommé (si utilisation depuis une TBX ArcGIS Pro)
    :param agolUrl2 : Url de l'organisation ArcGIS (si utilisation depuis une TBX ArcGIS Pro)
    :param agolUserName2 : Identifiant de l'utilisateur nommé (si utilisation depuis une TBX ArcGIS Pro)
    :param agolUserPassword2 : Mot de passe de l'utilisateur nommé (si utilisation depuis une TBX ArcGIS Pro)
    :return:
    """
    # Initialisation de la configuration
    scriptDirPath = os.path.dirname(os.path.realpath(__file__))
    configFilePath = os.path.join(scriptDirPath, "Configuration.ini")
    config = ConfigTools(configFilePath)

    # Initialisation des logs
    logPath = __CheckParamFolder(config.getValue("MAIN", "LOG_DIR"), DEFAULT_DIR_LOG)
    LogTool(printFlag=True, loggingFlag=True, loggingArcGisFlag=loggingArcGisFlag, loggingDirPath=logPath)
    LogTool.Instance().addInfo("==========================================================================")
    LogTool.Instance().addInfo("Copie du contenu d'un utilisateur nommé d'une organisation à une autre")

    # Récupération de la configuration
    # ==> Configuration liée à l'organisation source
    if(agolUrl==None):
        agolUrl = config.getValue('ORGANISATION', 'URL')
    ##end if
    if(agolUserName==None):
        agolUserName = config.getValue('ORGANISATION', 'USER')
    ##end if
    if(agolUserPassword==None):
        agolUserPassword = config.getValue('ORGANISATION', 'PASSWORD')
        agolUserPasswordEncrypted = config.getValue('ORGANISATION', 'PASSWORD_ENCRYPTED')
        if (agolUserPasswordEncrypted):
            agolUserPassword = CryptoTool.Decode(agolUserPassword)
        ##end if
    ##end if
    # ==> Configuration liée à l'organisation cible
    if(agolUrl2==None):
        agolUrl2 = config.getValue('ORGANISATION2', 'URL')
    ##end if
    if(agolUserName2==None):
        agolUserName2 = config.getValue('ORGANISATION2', 'USER')
    ##end if
    if(agolUserPassword2==None):
        agolUserPassword2 = config.getValue('ORGANISATION2', 'PASSWORD')
        agolUserPasswordEncrypted2 = config.getValue('ORGANISATION2', 'PASSWORD_ENCRYPTED')
        if (agolUserPasswordEncrypted2):
            agolUserPassword2 = CryptoTool.Decode(agolUserPassword2)
        ##end if
    ##end if

    # Initialisation des connexions aux organisations
    agol = AgolToolsSDK(agolUrl, agolUserName, agolUserPassword)
    agol2 = AgolToolsSDK(agolUrl2, agolUserName2, agolUserPassword2)

    # Récupèration des utilisateurs nommés
    agolUser = agol.getUserFromName(agolUserName)
    LogTool.Instance().addInfo("Source user={}".format(agolUser.username))
    agolUser2 = agol2.getUserFromName(agolUserName2)
    LogTool.Instance().addInfo("Target user={}".format(agolUser2.username))

    # Récupération du contenu de l'utilisateur nommé n°1
    agolUserContent = agol.getUserContent(agolUser)
    LogTool.Instance().addInfo(agolUserContent)

    # Copie d'un item
    LogTool.Instance().addInfo("Copying content...")
    agolUserContentId = {}
    for key in agolUserContent.keys():
        itemSource = agolUserContent[key]

        LogTool.Instance().addInfo(" - Copying '{}' \tfrom\t '{}' \tto\t '{}'".format(itemSource.title, itemSource.owner, agolUserName2))
        itemTarget = agol.copyItem(agolUser, itemSource, agol2.cnx, agolUser2)
        if (itemTarget != None):
            agolUserContentId[key] = itemTarget.itemid
        else:
            agolUserContentId[key] = None
        ##end if
    ##end for

    LogTool.Instance().addInfo("==========================================================================")
##end def CopyUserItems

def EncodePassword(loggingArcGisFlag=False, password=None):
    """
    Encodage d'un mot de passe
    :param loggingArcGisFlag: Flag pour l'ajout des messages dans ArcGIS
    :param paramPassword : Mot de passe à encoder (si utilisation depuis une TBX ArcGIS Pro)
    :return passwordEncoded: Mot depasse encodé
    """
    # Initialisation de la configuration
    scriptDirPath = os.path.dirname(os.path.realpath(__file__))
    configFilePath = os.path.join(scriptDirPath, "Configuration.ini")
    config = ConfigTools(configFilePath)

    # Initialisation des logs
    logPath = __CheckParamFolder(config.getValue("MAIN", "LOG_DIR"), "Log")
    LogTool(printFlag=True, loggingFlag=True, loggingArcGisFlag=loggingArcGisFlag, loggingDirPath=logPath)
    LogTool.Instance().addInfo("==========================================================================")
    LogTool.Instance().addInfo("Encodage d'un mot de passe...")

    # Si pas utilisation depuis une TBX ArcGIS Pro alors on demande la valeur
    if(password == None):
        password = getpass._raw_input("Mot de passe à encoder ?")
    ##end if

    passwordEncoded = None
    if(password != None and len(password)>0):
        print("Mot de passe à encoder : {}".format(password))
        passwordEncoded = CryptoTool.Encode(password)
        print("Mot de passe encodé : {}".format(passwordEncoded.decode("utf-8")))
    ##end if

    LogTool.Instance().addInfo("==========================================================================")
    return passwordEncoded
##end def EncodePassword

def GetWebMaps(loggingArcGisFlag=False, resultCsvName="AgolTools_GetWebMaps", agolUrl=None, agolUserName=None, agolUserPassword=None, flagTestServices=False):
    """
    Retourne la liste des webmap avec des url de service
    :param loggingArcGisFlag: Flag pour l'ajout des messages dans ArcGIS
    :param onlyBroken : Flag pour lister seulement les webmaps cassées
    :param resultCsvName : Nom du fichier CSV résultat
    :param agolUrl : Url de l'organisation ArcGIS (si utilisation depuis une TBX ArcGIS Pro)
    :param agolUserName : Identifiant de l'utilisateur nommé (si utilisation depuis une TBX ArcGIS Pro)
    :param agolUserPassword : Mot de passe de l'utilisateur nommé (si utilisation depuis une TBX ArcGIS Pro)
    :param flagTestServices: Flag pour tester l'URL des services des webmaps
    :return: Chemin du fichier CSV résultat
    """
    # Initialisation de la configuration
    scriptDirPath = os.path.dirname(os.path.realpath(__file__))
    configFilePath = os.path.join(scriptDirPath, "Configuration.ini")
    config = ConfigTools(configFilePath)

    # Initialisation des logs
    logPath = __CheckParamFolder(config.getValue("MAIN", "LOG_DIR"), DEFAULT_DIR_LOG)
    LogTool(printFlag=True, loggingFlag=True, loggingArcGisFlag=loggingArcGisFlag, loggingDirPath=logPath)
    LogTool.Instance().addInfo("==========================================================================")
    if(flagTestServices):
        LogTool.Instance().addInfo("Liste des webmap avec les url de services (non fonctionnel)")
    else:
        LogTool.Instance().addInfo("Liste des webmap avec les url de services")
    ##end if

    # ==> Configuration générales
    resultDir = __CheckParamFolder(config.getValue("MAIN", "RESULT_DIR"), DEFAULT_DIR_RESULT)
    maxItems = int(config.getValue("MAIN", "MAX_ITEMS"))
    # ==> Configuration liée à l'organisation source
    if(agolUrl == None):
        agolUrl = config.getValue('ORGANISATION', 'URL')
    ##end if
    if(agolUserName == None):
        agolUserName = config.getValue('ORGANISATION', 'USER')
    ##end if
    if(agolUserPassword == None):
        agolUserPassword = config.getValue('ORGANISATION', 'PASSWORD')
        agolUserPasswordEncrypted = config.getValue('ORGANISATION', 'PASSWORD_ENCRYPTED')
        if (agolUserPasswordEncrypted):
            agolUserPassword = CryptoTool.Decode(agolUserPassword)
        ##end if
    ##end if

    # Initialisation des connexions aux organisations
    agol = AgolToolsSDK(agolUrl, agolUserName, agolUserPassword)

    # Récupération de la liste des services des webmaps
    webmapsServices = agol.getWebmapsServices(maxItems=maxItems, flagTestServices=flagTestServices)

    # Export CSV de la liste
    # ==> Initialisation du fichier
    csvFile = CsvTool(resultDir, resultCsvName)
    # ==> Entête du fichier
    csvHeader = ["webmapId", "webmapURL", "webmapTitle", "webmapOwner", "serviceType", "serviceUrl"]
    if(flagTestServices):
        csvHeader.extend(["serviceStatus", "serviceStatusCode", "serviceErrorMessage"])
    ##end if
    csvFile.write(*csvHeader)
    # ==> Remplissage du fichier
    for ws in webmapsServices:
        csvRow = [ws["webmapId"], ws["webmapUrl"], ws["webmapTitle"], ws["webmapOwner"], ws["serviceType"], ws["serviceUrl"]]
        if(flagTestServices):
            csvRow.extend([ws["serviceStatus"], ws["serviceStatusCode"], ws["serviceErrorMessage"]])
        ##end if
        csvFile.write(*csvRow)
    ##end for

    # Résultat
    LogTool.Instance().addInfo("Résultat :")
    LogTool.Instance().addInfo(" - CSV : {}".format(csvFile.filePath))
    LogTool.Instance().addInfo("==========================================================================")
    
    return csvFile.filePath
##end def GetWebMaps

def WhatsNew(loggingArcGisFlag=False, agolUrl=None, agolUserName=None, agolUserPassword=None, fromDate=None):
    """
    Récupère la liste des élements nouveaux dans l'organisation
    :param loggingArcGisFlag: Flag pour l'ajout des messages dans ArcGIS
    :param agolUrl : Url de l'organisation ArcGIS (si utilisation depuis une TBX ArcGIS Pro)
    :param agolUserName : Identifiant de l'utilisateur nommé (si utilisation depuis une TBX ArcGIS Pro)
    :param agolUserPassword : Mot de passe de l'utilisateur nommé (si utilisation depuis une TBX ArcGIS Pro)
    :param fromDate : Date de filtrage (si utilisation depuis une TBX ArcGIS Pro)
    :return: Chemin du fichier CSV résultat
    """
    # Initialisation de la configuration
    scriptDirPath = os.path.dirname(os.path.realpath(__file__))
    configFilePath = os.path.join(scriptDirPath, "Configuration.ini")
    config = ConfigTools(configFilePath)

    # Initialisation des logs
    logPath = __CheckParamFolder(config.getValue("MAIN", "LOG_DIR"), DEFAULT_DIR_LOG)
    LogTool(printFlag=True, loggingFlag=True, loggingArcGisFlag=loggingArcGisFlag, loggingDirPath=logPath)
    LogTool.Instance().addInfo("==========================================================================")
    LogTool.Instance().addInfo("Liste des élements nouveaux dans l'organisation")

    # ==> Configuration générales
    resultDir = __CheckParamFolder(config.getValue("MAIN", "RESULT_DIR"), DEFAULT_DIR_RESULT)
    # ==> Configuration liée à l'organisation source
    if(agolUrl == None):
        agolUrl = config.getValue('ORGANISATION', 'URL')
    ##end if
    if(agolUserName == None):
        agolUserName = config.getValue('ORGANISATION', 'USER')
    ##end if
    if(agolUserPassword == None):
        agolUserPassword = config.getValue('ORGANISATION', 'PASSWORD')
        agolUserPasswordEncrypted = config.getValue('ORGANISATION', 'PASSWORD_ENCRYPTED')
        if (agolUserPasswordEncrypted):
            agolUserPassword = CryptoTool.Decode(agolUserPassword)
        ##end if
    ##end if
    if(fromDate == None):
        fromDate = datetime.datetime.strptime(str(config.getValue("WHATS_NEW", "FROM_DATE")), '%Y-%m-%d')
    ##end if
    
    # Initialisation des connexions aux organisations
    agol = AgolToolsSDK(agolUrl, agolUserName, agolUserPassword)
    csvResult = CsvTool(resultDir, "AgolTools_WhatsNew")
    csvResult.write("type", "name", "created", "owner")

    # Cas des utilisateurs nommés
    # ==> Récupération
    users = agol.getUsers(createdFrom=fromDate)
    LogTool.Instance().addInfo("Nombre d'utilisateurs = {}".format(len(users)))
    # ==> Export CSV
    for user in users:
        created = datetime.datetime.utcfromtimestamp(int(user["created"])/1000)
        LogTool.Instance().addInfo(" - {}".format(user["username"]))
        csvResult.write("user", user["username"], created, "")
    ##end for

    # Cas des groupes
    # ==> Récupération
    groups = agol.getGroups(createdFrom=fromDate)
    LogTool.Instance().addInfo("Nombre de groupes = {}".format(len(groups)))
    # ==> Export CSV
    for group in groups:
        created = datetime.datetime.utcfromtimestamp(int(group["created"])/1000)
        LogTool.Instance().addInfo(" - {}".format(group["title"]))
        csvResult.write("group", group["title"], created, group["owner"])
    ##end for

    # Cas du contenu
    # ==> Récupération
    contents = agol.getContents(createdFrom=fromDate)
    LogTool.Instance().addInfo("Nombre de contenu = {}".format(len(contents)))
    # ==> Export CSV
    for content in contents:
        created = datetime.datetime.utcfromtimestamp(int(content["created"])/1000)
        LogTool.Instance().addInfo(" - {}".format(content["title"]))
        csvResult.write("content", content["title"], created, content["owner"])
    ##end for

    # Résultat
    LogTool.Instance().addInfo("Résultat :")
    LogTool.Instance().addInfo(" - CSV : {}".format(csvResult.filePath))
    LogTool.Instance().addInfo("==========================================================================")
    
    return csvResult.filePath
##end def WhatsNew
# --------------------------------------------------

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EXECUTION DEPUIS UNE TOOLBOX ARCGIS PRO 
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if __name__ == '__main__':
    
    # Récupération du nom de l'outil transmis en 1er paramètre
    paramTool = arcpy.GetParameterAsText(0)
    if (paramTool == None or len(paramTool) == 0):
        arcpy.AddError("Erreur grave")
    ##end if
    
    # Cas de l'outil d'encodage de mot de passe ???
    if paramTool == "EncodePassword":                
        # Récupération des paramètre de la TOOLBOX
        paramTextToEncode = arcpy.GetParameterAsText(1)
        # Execution de l'outil
        paramTextEncoded = EncodePassword(loggingArcGisFlag=True, password=paramTextToEncode)
        # Renvoie du résultat
        arcpy.SetParameter(2, paramTextEncoded)
    ##end if
    
    # Cas de l'outil qui récupère la liste des élements nouveaux dans l'organisation
    elif paramTool == "WhatsNew":
        # Récupération des paramètre de la TOOLBOX
        paramAgolUrl = arcpy.GetParameterAsText(1)
        paramAgolUserName = arcpy.GetParameterAsText(2)
        paramAgolUserPassword = arcpy.GetParameterAsText(3)
        paramFromDate = arcpy.GetParameter(4)
        # Execution de l'outil
        paramCsvPath = WhatsNew(loggingArcGisFlag=True, agolUrl=paramAgolUrl, agolUserName=paramAgolUserName, agolUserPassword=paramAgolUserPassword, fromDate=paramFromDate)
        # Renvoie du résultat
        arcpy.SetParameter(5, paramCsvPath)
    ##end if
    
    # Cas de l'outil qui récupère la liste des webmaps
    elif paramTool == "GetWebMaps":
        # Récupération des paramètre de la TOOLBOX
        paramAgolUrl = arcpy.GetParameterAsText(1)
        paramAgolUser = arcpy.GetParameterAsText(2)
        paramAgolPwd = arcpy.GetParameterAsText(3)
        paramOnlyBroken = arcpy.GetParameter(4)
        # Execution de l'outil
        resultCsvName = "AgolTools_GetWebMaps"
        if(paramOnlyBroken):
            resultCsvName = "AgolTools_GetWebMapsBroken"
        ##endif
        paramCsvPath = GetWebMaps(loggingArcGisFlag=True, resultCsvName=resultCsvName, agolUrl=paramAgolUrl, agolUserName=paramAgolUser, agolUserPassword=paramAgolPwd, flagTestServices=paramOnlyBroken)
        # Renvoie du résultat
        arcpy.SetParameter(5, paramCsvPath)
    ##end if
    
    # Cas de l'outil de copie du contenu d'un utilisateur nommé d'une organisation à une autre
    elif paramTool == "CopyUserItems":
        # Récupération des paramètre de la TOOLBOX
        paramAgolSrcUrl = arcpy.GetParameterAsText(1)
        paramAgolSrcUser = arcpy.GetParameterAsText(2)
        paramAgolSrcPwd = arcpy.GetParameterAsText(3)
        paramAgolDstUrl = arcpy.GetParameterAsText(4)
        paramAgolDstUser = arcpy.GetParameterAsText(5)
        paramAgolDstPwd = arcpy.GetParameterAsText(6)
        # Execution de l'outil
        CopyUserItems(loggingArcGisFlag=True, agolUrl=paramAgolSrcUrl, agolUserName=paramAgolSrcUser, agolUserPassword=paramAgolSrcPwd, agolUrl2=paramAgolDstUrl, agolUserName2=paramAgolDstUser, agolUserPassword2=paramAgolDstPwd)
    ##end if
    
##end if