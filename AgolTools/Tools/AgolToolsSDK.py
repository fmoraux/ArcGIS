# -*- coding: utf-8
# coding: utf-8
##==========================================================================
##=====    Script         : Outils pour AGOL (SDK)                     =====
##=====    Author         : Flavie MORAUX (moraux.flavie@gmail.com)    =====
##=====    Version        : 1.0                                        =====
##=====    Date           : 01/01/2017                                 =====
##==========================================================================
import  datetime
import tempfile
import requests

from Tools.LogTool import LogTool
from arcgis.gis import GIS
# --------------------------------------------------

class AgolToolsSDK(object):
    """Classe utilitaire pour les organisations ArcGIS Online/Portal"""

    ITEM_FEATURE_SERVICE = "Feature Service"
    TEXT_BASED_ITEM_TYPES = frozenset(['Web Map', ITEM_FEATURE_SERVICE, 'Map Service', 'Web Scene',
                                       'Image Service', 'Feature Collection',
                                       'Feature Collection Template',
                                       'Web Mapping Application', 'Mobile Application',
                                       'Symbol Set', 'Color Set',
                                       'Windows Viewer Configuration'])

    FILE_BASED_ITEM_TYPES = frozenset(['File Geodatabase', 'CSV', 'Image', 'KML', 'Locator Package',
                                       'Map Document', 'Shapefile', 'Microsoft Word', 'PDF',
                                       'Microsoft Powerpoint', 'Microsoft Excel', 'Layer Package',
                                       'Mobile Map Package', 'Geoprocessing Package', 'Scene Package',
                                       'Tile Package', 'Vector Tile Package'])

    ITEM_COPY_PROPERTIES = ['title', 'type', 'typeKeywords', 'description', 'tags',
                            'snippet', 'extent', 'spatialReference', 'name',
                            'accessInformation', 'licenseInfo', 'culture', 'url']

    MAX_COUNT=100

    def __init__(self, url, user, password):
        """
        Initialisation
        :param url: url de l'organisation
        :param user: Nom de l'utilisateur nommé
        :param password: Mot de passe de l'utilisateur nommé
        """
        self.__url = url
        self.__user = user
        self.__password = password

        self.__cnx = GIS(self.__url, self.__user, self.__password)
    ##end def __init__

    @property
    def url(self):
        """
        :return: url de l'organisation
        """
        return self.__url
    ##end def

    @property
    def user(self):
        """
        :return: Nom de l'utilisateur nommé
        """
        return self.__user
    ##end def user

    @property
    def cnx(self):
        """
        :return: Connexion à l'organisation
        """
        return self.__cnx
    ##end def user

    def getUsers(self, createdFrom=False):
        """
        Retourne la liste des utilisateurs nommés de l'organisation
        :param createdFrom : Filtrage des utilisateurs créés à partir d'une date donnée
        :return:
        """
        users = self.__cnx.users.search(max_users=AgolToolsSDK.MAX_COUNT)

        # Filtrage sur la date de création
        if(createdFrom != None):
            newUsers = []

            for user in users:
                createdTimestamp = int(user["created"])/1000
                createdDate = datetime.datetime.fromtimestamp(createdTimestamp)
                if (createdDate >= createdFrom):
                    newUsers.append((user))
                ##end if
            ##end for

            return newUsers
        ##end if

        return users
    ##end def getUsers

    def getGroups(self, createdFrom=None):
        """
        Retourne la liste des groupes
        :param createdFrom : Filtrage des utilisateurs créés à partir d'une date donnée
        :return:
        """
        groups = self.__cnx.groups.search(max_groups=AgolToolsSDK.MAX_COUNT)

        # Filtrage sur la date de création
        if(createdFrom != None):
            newGroups = []

            for group in groups:
                createdTimestamp = int(group["created"])/1000
                createdDate = datetime.datetime.fromtimestamp(createdTimestamp)
                if (createdDate >= createdFrom):
                    newGroups.append((group))
                ##end if
            ##end for

            return newGroups
        ##end if

        return groups
    ##end def getGroups

    def getContents(self, createdFrom=None):
        """
        Retourne la liste du contenu
        :param createdFrom : Filtrage des utilisateurs créés à partir d'une date donnée
        :return:
        """
        contents = self.__cnx.content.search(query="title:*", max_items=AgolToolsSDK.MAX_COUNT)

        # Filtrage sur la date de création
        if(createdFrom != None):
            newContents = []

            for content in contents:
                createdTimestamp = int(content["created"])/1000
                createdDate = datetime.datetime.fromtimestamp(createdTimestamp)
                if (createdDate >= createdFrom):
                    newContents.append((content))
                ##end if
            ##end for

            return newContents
        ##end if

        return contents
    ##end def getContents

    def getUserFromName(self, userName):
        """
        Récupèration d'un utilisateur nommé
        :param userName: Nom de l'utilisateur nommé
        :return: Utilisateur nommé
        """
        user = None
        if (userName != None):
            agolUsers = self.__cnx.users.search(userName)
            if (agolUsers != None and len(agolUsers) >= 1):
                user = agolUsers[0]
                ##end if
        ##end if
        return user
    ##end def getUserFromName

    def getUserContent(self, user):
        """
        Récupération du contenu d'un utilisateur nommé
        :param user: Utilisateur nommé
        :return: Contenu de l'utilistaeur nommé
        """
        agolContent = {}
        if (user != None):
            numItems = 0
            numFolders = 0
            LogTool.Instance().addInfo("Collecting item ids for {}\t\t".format(user.username))
            content = user.items()

            # Get item ids from root folder first
            for item in content:
                numItems += 1
                agolContent[item.itemid] = item
            ##end for

            # Get item ids from each of the folders next
            folders = user.folders
            for folder in folders:
                numFolders += 1
                folderItems = user.items(folder=folder['title'])
                for item in folderItems:
                    numItems += 1
                    agolContent[item.itemid] = item
                    ##end for
            ##end for

            LogTool.Instance().addInfo("Number of folders {} # Number of items {}".format(str(numFolders), str(numItems)))
        ##end if
        return agolContent
    ##end def getUserContent

    def getWebmapsServices(self, maxItems=MAX_COUNT, flagTestServices=False):
        """
        Retourne la liste des services des webmaps
        :param maxItems: Nombre maximale de webmaps
        :param flagTestServices: Flag pour tester l'URL des services des webmaps
        :return: Liste des services des webmaps
        """
        services = []

        # Récupération de toutes les webmaps
        webmaps = self.__cnx.content.search("title:%", item_type="Web Map", max_items=maxItems)
        webmapsCount = len(webmaps)
        LogTool.Instance().addInfo("Nombre de webmaps={}".format(webmapsCount))

        # Test des URLs des BaseMaps et OperationalLayers des webmaps
        LogTool.Instance().addInfo("Parcours des webmaps:")
        webmapsIndex = 1
        for webmap in webmaps:
            LogTool.Instance().addInfo(" - Webmap n°{} '{}' ({}/{})...".format(webmap["id"], webmap["title"], webmapsIndex, webmapsCount))
            webmapData = webmap.get_data(try_json=True)

            # Cas des BaseMap
            baseMapLayers = webmapData["baseMap"]["baseMapLayers"]
            for baseMapLayer in baseMapLayers:
                service = {}
                service["webmapId"] = webmap["id"]
                service["webmapUrl"] = "{}/home/item.html?id={};".format(self.__url, webmap["id"])
                service["webmapTitle"] = webmap["title"]
                service["webmapOwner"] = webmap["owner"]
                service['serviceType'] = "Basemap"

                url = ""
                if ("url" in baseMapLayer):
                    url = baseMapLayer["url"]
                ##end if
                service["serviceUrl"] = url

                # Test de l'url
                if(flagTestServices):
                    status, statusCode, errorMessage = self.__testUrl(url)

                    service["serviceStatus"] = status
                    service["serviceStatusCode"] = statusCode
                    service["serviceErrorMessage"] = errorMessage

                    LogTool.Instance().addInfo("    - baseMapLayer={} ({} ==> {} / {})".format(url, status, statusCode, errorMessage))
                else:
                    LogTool.Instance().addInfo("    - baseMapLayer={}".format(url))
                ##end if

                services.append(service)
            ##end for

            # Cas des OperationalLayers
            operationalLayers = webmapData["operationalLayers"]
            for operationalLayer in operationalLayers:
                service = {}
                service["webmapId"] = webmap["id"]
                service["webmapUrl"] = "{}/home/item.html?id={};".format(self.__url, webmap["id"])
                service["webmapTitle"] = webmap["title"]
                service["webmapOwner"] = webmap["owner"]
                service['serviceType'] = "Operational"

                url = ""
                if ("url" in baseMapLayer):
                    url = operationalLayer["url"]
                ##end if
                service["serviceUrl"] = url

                # Test de l'url
                if(flagTestServices):
                    status, statusCode, errorMessage = self.__testUrl(url)

                    service["serviceStatus"] = status
                    service["serviceStatusCode"] = statusCode
                    service["serviceErrorMessage"] = errorMessage

                    LogTool.Instance().addInfo("    - operationalLayer={} ({} ==> {} / {})".format(url, status, statusCode, errorMessage))
                else:
                    LogTool.Instance().addInfo("    - operationalLayer={}".format(url))
                ##end if

                services.append(service)
            ##end for

            webmapsIndex += 1
        ##end for

        return services
    ##end def getWebmapsServices

    def copyItem(self, userSource, itemSource, organizationTarget, userTarget):
        """
        Copie d'un item
        :param userSource:  Utilisateur source
        :param itemSource:  Item source
        :param organizationTarget: Organisation cible
        :param userTarget: Utilisateur cible
        :return: Item cible
        """
        itemTarget = None
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                itemProperties = {}
                for propertyName in AgolToolsSDK.ITEM_COPY_PROPERTIES:
                    itemProperties[propertyName] = itemSource[propertyName]
                ##end for

                dataFile = None
                if itemSource.type in AgolToolsSDK.TEXT_BASED_ITEM_TYPES:
                    # If its a text-based item, then read the text and add it to the request.
                    text = itemSource.get_data(False)
                    itemProperties['text'] = text
                elif itemSource.type in AgolToolsSDK.FILE_BASED_ITEM_TYPES:
                    # download data and add to the request as a file
                    dataFile = itemSource.download(temp_dir)
                ##end if

                thumbnailFile = itemSource.download_thumbnail(temp_dir)
                metadataFile = itemSource.download_metadata(temp_dir)

                # find item's folder
                itemFolderTitles = [f['title'] for f in userSource.folders if f['id'] == itemSource.ownerFolder]
                folderName = None
                if len(itemFolderTitles) > 0:
                    folderName = itemFolderTitles[0]
                ##end if

                # if folder does not exist for target user, create it
                if folderName:
                    userTargetFolders = [f['title'] for f in userTarget.folders if f['title'] == folderName]
                    if len(userTargetFolders) == 0:
                        # create the folder
                        organizationTarget.content.create_folder(folderName, userTarget)
                        ##end if
                ##end if

                # Add the item to the target portal, assign owner and folder
                itemTarget = organizationTarget.content.add(itemProperties, dataFile, thumbnailFile, metadataFile, userTarget, folderName)

                # Specific item type
                # ==> Feature service
                if itemSource.type == AgolToolsSDK.ITEM_FEATURE_SERVICE:
                    # Download data
                    # Publish data on new organization
                    # Update copied item
                    pass
                ##end if

                # Set sharing (privacy) information
                shareEveryone = (itemSource.access == 'public')
                shareOrg = itemSource.access in ['org', 'public']
                shareGroups = []
                if itemSource.access == 'shared':
                    shareGroups = itemSource.groups
                ##end if
                itemTarget.share(shareEveryone, shareOrg, shareGroups)
                return itemTarget

        except Exception as ex:
            LogTool.Instance().addError("\tError copying " + itemSource.title)
            LogTool.Instance().addError("\t" + str(ex))
            return itemTarget
        ##end try
    ##end def copyItem

    def __testUrl(self, url):
        """
        Test si une url est cassée
        :param url: url à tester
        :return: status : Status de la requête de l'URL (OK|KO|UNKNOW|ERROR)
        :return: statusCode : Code d'erreur de la requête de l'URL
        :return: errorMessage : Message d'erreur de la requête de l'URL
        """
        status = None
        statusCode = None
        errorMessage = ""

        if (url != None and len(url) > 0):
            try:
                response = requests.get(url)
                statusCode = response.status_code

                if str(statusCode).startswith('2'):
                    status = "OK"
                elif str(statusCode).startswith('4') or str(statusCode).startswith('5'):
                    status = "KO"
                else:
                    status = "UNKNOWN"
            except Exception as ex:
                status = "ERROR"
                statusCode = ""
                errorMessage = ex
                ##end try
        else:
            status = "UNKNOWN"
            statusCode = ""
            errorMessage = "*** Empty url ***"
        ##end if

        return status, statusCode, errorMessage
    ##end def __testUrl

##end class AgolToolsSDK

# --------------------------------------------------