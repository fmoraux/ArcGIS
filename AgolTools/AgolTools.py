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

def CopyUserItems():
    """
    Copie du contenu d'un utilisateur nommé d'une organisation à une autre
    :return:
    """
    # Initialisation de la configuration
    scriptDirPath = os.path.dirname(os.path.realpath(__file__))
    configFilePath = os.path.join(scriptDirPath, "Configuration.ini")
    config = ConfigTools(configFilePath)

    # Initialisation des logs
    logPath = __CheckParamFolder(config.getValue("MAIN", "LOG_DIR"), DEFAULT_DIR_LOG)
    LogTool(printFlag=True, loggingFlag=True, loggingDirPath=logPath)
    LogTool.Instance().addInfo("==========================================================================")
    LogTool.Instance().addInfo("Copie du contenu d'un utilisateur nommé d'une organisation à une autre")

    # Récupération de la configuration
    # ==> Configuration liée à l'organisation source
    agolUrl = config.getValue('ORGANISATION', 'url')
    agolUserName = config.getValue('ORGANISATION', 'USER')
    agolUserPassword = config.getValue('ORGANISATION', 'PASSWORD')
    agolUserPasswordEncrypted = config.getValue('ORGANISATION', 'PASSWORD_ENCRYPTED')
    if (agolUserPasswordEncrypted):
        agolUserPassword = CryptoTool.Decode(agolUserPassword)
    ##end if
    # ==> Configuration liée à l'organisation cible
    agolUrl2 = config.getValue('ORGANISATION2', 'url')
    agolUserName2 = config.getValue('ORGANISATION2', 'USER')
    agolUserPassword2 = config.getValue('ORGANISATION2', 'PASSWORD')
    agolUserPasswordEncrypted2 = config.getValue('ORGANISATION2', 'PASSWORD_ENCRYPTED')
    if (agolUserPasswordEncrypted2):
        agolUserPassword2 = CryptoTool.Decode(agolUserPassword2)
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

def EncodePassword():
    """
    Encodage d'un mot de passe
    :return:
    """
    # Initialisation de la configuration
    scriptDirPath = os.path.dirname(os.path.realpath(__file__))
    configFilePath = os.path.join(scriptDirPath, "Configuration.ini")
    config = ConfigTools(configFilePath)

    # Initialisation des logs
    logPath = __CheckParamFolder(config.getValue("MAIN", "LOG_DIR"), "Log")
    LogTool(printFlag=True, loggingFlag=True, loggingDirPath=logPath)
    LogTool.Instance().addInfo("==========================================================================")
    LogTool.Instance().addInfo("Encodage d'un mot de passe...")

    password = getpass._raw_input("Mot de passe à encoder ?")

    if(password != None and len(password)>0):
        print("Mot de passe à encoder : {}".format(password))
        passwordEncoded = CryptoTool.Encode(password)
        print("Mot de passe encodé : {}".format(passwordEncoded.decode("utf-8")))
    ##end if

    LogTool.Instance().addInfo("==========================================================================")
##end def EncodePassword

def GetWebMaps(resultCsvName="AgolTools_GetWebMaps", flagTestServices=False):
    """
    Retourne la liste des webmap avec des url de service
    :param onlyBroken : Flag pour lister seulement les webmaps cassées
    :param resultCsvName : Nom du fichier CSV résultat
    :param flagTestServices: Flag pour tester l'URL des servcies des webmaps
    :return:
    """
    # Initialisation de la configuration
    scriptDirPath = os.path.dirname(os.path.realpath(__file__))
    configFilePath = os.path.join(scriptDirPath, "Configuration.ini")
    config = ConfigTools(configFilePath)

    # Initialisation des logs
    logPath = __CheckParamFolder(config.getValue("MAIN", "LOG_DIR"), DEFAULT_DIR_LOG)
    LogTool(printFlag=True, loggingFlag=True, loggingDirPath=logPath)
    LogTool.Instance().addInfo("==========================================================================")
    if(flagTestServices):
        LogTool.Instance().addInfo("Liste des webmap avec les url de servcie (non fonctionnel)")
    else:
        LogTool.Instance().addInfo("Liste des webmap avec les url de servcie")
    ##end if

    # ==> Configuration générales
    resultDir = __CheckParamFolder(config.getValue("MAIN", "RESULT_DIR"), DEFAULT_DIR_RESULT)
    maxItems = int(config.getValue("MAIN", "MAX_ITEMS"))
    # ==> Configuration liée à l'organisation source
    agolUrl = config.getValue('ORGANISATION', 'url')
    agolUserName = config.getValue('ORGANISATION', 'USER')
    agolUserPassword = config.getValue('ORGANISATION', 'PASSWORD')
    agolUserPasswordEncrypted = config.getValue('ORGANISATION', 'PASSWORD_ENCRYPTED')
    if (agolUserPasswordEncrypted):
        agolUserPassword = CryptoTool.Decode(agolUserPassword)
    ##end if

    # Initialisation des connexions aux organisations
    agol = AgolToolsSDK(agolUrl, agolUserName, agolUserPassword)

    # Récupération de la liste des servcies des webmaps
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
##end def GetWebMaps

def WhatsNew():
    """
    Récupère la liste des élements nouveaux dans l'organisation
    :return:
    """
    # Initialisation de la configuration
    scriptDirPath = os.path.dirname(os.path.realpath(__file__))
    configFilePath = os.path.join(scriptDirPath, "Configuration.ini")
    config = ConfigTools(configFilePath)

    # Initialisation des logs
    logPath = __CheckParamFolder(config.getValue("MAIN", "LOG_DIR"), DEFAULT_DIR_LOG)
    LogTool(printFlag=True, loggingFlag=True, loggingDirPath=logPath)
    LogTool.Instance().addInfo("==========================================================================")
    LogTool.Instance().addInfo("Liste des élements nouveaux dans l'organisation")

    # ==> Configuration générales
    resultDir = __CheckParamFolder(config.getValue("MAIN", "RESULT_DIR"), DEFAULT_DIR_RESULT)
    # ==> Configuration liée à l'organisation source
    agolUrl = config.getValue('ORGANISATION', 'url')
    agolUserName = config.getValue('ORGANISATION', 'USER')
    agolUserPassword = config.getValue('ORGANISATION', 'PASSWORD')
    agolUserPasswordEncrypted = config.getValue('ORGANISATION', 'PASSWORD_ENCRYPTED')
    if (agolUserPasswordEncrypted):
        agolUserPassword = CryptoTool.Decode(agolUserPassword)
    ##end if
    # ==> Configuration liée à l'outil "WhatsNew"
    fromDate = datetime.datetime.strptime(str(config.getValue("WHATS_NEW", "FROM_DATE")), '%Y-%m-%d')

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
##end def WhatsNew
# --------------------------------------------------

# Copie du contenu d'un utilisateur nommé d'une organisation à une autre
#CopyUserItems()

#Encodage de mot de passe
#EncodePassword()

# Liste des webmap avec les url des servcies
#GetWebMaps()
#GetWebMapsBroken()

# Récupère la liste des élements nouveaux dans l'organisation
#WhatsNew()
