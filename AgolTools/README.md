
Aide
====

Aide à l'utilisation des scripts contenu dans le package **AgolTools** :
>- **[EncodePassword](README.md#encodepassword)** pour l'encodage d'un mot de passe ;
>- **[CopyUserItems](README.md#copyuseritems)** pour la copie du contenu d'un utilisateur nommé à un autre ;
>- **[GetWebMaps](README.md#getwebmaps)** pour récupérer la liste des services des webmaps au format CSV ;
>- **[GetWebMapsBroken](README.md#getwebmapsbroken)** pour récupérer la liste des services des webmaps et leurs états au format CSV ;
>- **[WhatsNew](README.md#whatsnew)** pour récupérer la liste des nouveautés au format CSV ;


**Prérequis :**
> - **Python 3 ;**
> - **ArcGIS API for Python ;**
> - **Chemin Python ajouté à la variable d'environnement Path.**
> - **Fichier de configuration à jour.**

----------


EncodePassword
-----------------------

Encodage d'un mot de passe (en base 64).



#### <i class="icon-file"></i> Execution

Voir le fichier de commande **AgolTools_EncodePassword.bat** et saisir le mot de passe à encoder.

*Egalement disponible depuis la boîte à outils **AgolTools_ArcGISPro** dans ArcGIS Pro.*

#### <i class="icon-file"></i> Résultat

Récupérer le mot de passe encodé affiché dans la console.

----------


CopyUserItems
---------------------

Copie le contenu d'un utilisateur nommé d'une organisation à un utilisateur nommé d'une autre organisation.

> **Note:**

> - Ne duplique pas le contenu héberge, mais créé une référence.
> - Ne recâble pas les cartes et applications.

#### <i class="icon-file"></i> Configuration

Renseigner au préalable le fichier **Configuration.ini** :


    ; Configuration générale
    [MAIN]
    LOG_DIR=Log

    ; Configuration liée à l'organisation ArcGIS Online/Portal
    [ORGANISATION]
    URL=http://www.arcgis.com
    USER=
    PASSWORD=
    PASSWORD_ENCRYPTED=

    ; Configuration liée à une deuxième organisation ArcGIS Online/Portal
    [ORGANISATION2]
    URL=http://www.arcgis.com
    USER=
    PASSWORD=
    PASSWORD_ENCRYPTED=

Avec :

 - ***MAIN*** : pour la configuration de l'utilisateur nommé source
	 - ***LOG_DIR*** : Dossier où stocker les fichiers de log (***chemin relatif ou absolu, par défaut 'Log'***)

 - ***ORGANISATION*** : pour la configuration de l'utilisateur nommé source
	 - ***URL*** : Url de l'organisation ArcGIS
	 - ***USER*** : Identifiant de l'utilisateur nommé
	 - ***PASSWORD*** : Mot de passe de l'utilisateur nommé
	 - ***PASSWORD_ENCRYPTED*** : Flag si le mot de passe est encrypté (***True***) ou non (***False***)

 - ***ORGANISATION2*** : pour la configuration de l'utilisateur nommé cible
	 - ***URL*** : Url de l'organisation ArcGIS
	 - ***USER*** : Identifiant de l'utilisateur nommé
	 - ***PASSWORD*** : Mot de passe de l'utilisateur nommé
	 - ***PASSWORD_ENCRYPTED*** : Flag si le mot de passe est encrypté (***True***) ou non (***False***)

#### <i class="icon-file"></i> Execution

Voir le fichier de commande **AgolTools_CopyUserItems.bat**.

*Egalement disponible depuis la boîte à outils **AgolTools_ArcGISPro** dans ArcGIS Pro.*


----------


GetWebMaps
----------------------------

Récupère la liste des services des webmaps  au format CSV.

#### <i class="icon-file"></i> Configuration

Renseigner au préalable le fichier **Configuration.ini** :

    ; Configuration générale
    [MAIN]
    RESULT_DIR=\Result
    LOG_DIR=Log
    MAX_ITEMS=100

    ; Configuration liée à l'organisation ArcGIS Online/Portal
    [ORGANISATION]
    URL=http://www.arcgis.com
    USER=
    PASSWORD=
    PASSWORD_ENCRYPTED=

Avec :

  - ***MAIN*** : pour la configuration de l'organisation
	 - ***RESULT_DIR*** : Chemin du dossier résultat (***chemin relatif ou absolu, par défaut 'Result'***)
	 - ***LOG_DIR*** : Dossier où stocker les fichiers de log (***chemin relatif ou absolu, par défaut 'Log'***)
	 - ***MAX_ITEMS*** : Nombre d'item maximale à analyser

  - ***ORGANISATION*** : pour la configuration de l'organisation
	 - ***URL*** : Url de l'organisation ArcGIS
	 - ***USER*** : Identifiant de l'utilisateur nommé
	 - ***PASSWORD*** : Mot de passe de l'utilisateur nommé
	 - ***PASSWORD_ENCRYPTED*** : Flag si le mot de passe est encrypté (***True***) ou non (***False***)

#### <i class="icon-file"></i> Execution

Voir le fichier de commande **AgolTools_GetWebMaps.bat**.

*Egalement disponible depuis la boîte à outils **AgolTools_ArcGISPro** dans ArcGIS Pro.*

#### <i class="icon-file"></i> Résultat

Voir le fichier CSV **AgolTools_GetWebMapsBroken*** généré dans le dossier résultat.

La structure du fichier est la suivante :

 - **webmapId** : Identifiant de la webmap ;
 - **MapURL** : Url de la webmap ;
 - **webmapTitle** : Libellé de la webmap ;
 - **webmapOwner** : Propriétaire de la webmap ;
 - **serviceType** : Type de service (**Basemap** | **Operational**) ;
 - **serviceUrl**: Url du service.


GetWebMapsBroken
----------------------------

Récupère la liste des services des webmaps et leurs états  au format CSV.

#### <i class="icon-file"></i> Configuration

Renseigner au préalable le fichier **Configuration.ini** :

    ; Configuration générale
    [MAIN]
    RESULT_DIR=Result
    LOG_DIR=Log
    MAX_ITEMS=100

    ; Configuration liée à l'organisation ArcGIS Online/Portal
    [ORGANISATION]
    URL=http://www.arcgis.com
    USER=
    PASSWORD=
    PASSWORD_ENCRYPTED=

Avec :

  - ***MAIN*** : pour la configuration de l'organisation
	 - ***RESULT_DIR*** : Chemin du dossier résultat (***chemin relatif ou absolu, par défaut 'Result'***)
	 - ***LOG_DIR*** : Dossier où stocker les fichiers de log (***chemin relatif ou absolu, par défaut 'Log'***)
	 - ***MAX_ITEMS*** : Nombre d'item maximale à analyser

  - ***ORGANISATION*** : pour la configuration de l'organisation
	 - ***URL*** : Url de l'organisation ArcGIS
	 - ***USER*** : Identifiant de l'utilisateur nommé
	 - ***PASSWORD*** : Mot de passe de l'utilisateur nommé
	 - ***PASSWORD_ENCRYPTED*** : Flag si le mot de passe est encrypté (***True***) ou non (***False***)

#### <i class="icon-file"></i> Execution

Voir le fichier de commande **AgolTools_GetWebMapsBroken.bat**.

*Egalement disponible depuis la boîte à outils **AgolTools_ArcGISPro** dans ArcGIS Pro.*

#### <i class="icon-file"></i> Résultat

Voir le fichier CSV **AgolTools_GetWebMapsBroken*** généré dans le dossier résultat.

La structure du fichier est la suivante :

 - **webmapId** : Identifiant de la webmap ;
 - **MapURL** : Url de la webmap ;
 - **webmapTitle** : Libellé de la webmap ;
 - **webmapOwner** : Propriétaire de la webmap ;
 - **serviceType** : Type de service (**Basemap** | **Operational**) ;
 - **serviceUrl**: Url du service ;
 - **serviceStatus** : Etat du service (***OK***| ***KO*** | ***ERROR*** | ***UNKNOW***) ;
 - **serviceStatusCode** : Message en cas d'anomalie ;
 - **serviceErrorMessage**: Message complémentaire en cas d'anomalie.

Un trie sur la colonne serviceStatus permet de lister les webmaps cassées.


WhatsNew
----------------------------

Récupère la liste des nouveautés au format CSV soit

- Utilisateurs
- Groupes
- Contenus.

#### <i class="icon-file"></i> Configuration

Renseigner au préalable le fichier **Configuration.ini** :

    ; Configuration générale
    [MAIN]
    RESULT_DIR=Result
    LOG_DIR=Log
    MAX_ITEMS=100

    ; Configuration liée à l'organisation ArcGIS Online/Portal
    [ORGANISATION]
    URL=http://www.arcgis.com
    USER=
    PASSWORD=
    PASSWORD_ENCRYPTED=

    ; Configuration liée à l'outil "WhatsNew"
    [WHATS_NEW]
    FROM_DATE=2017-01-01

Avec :

  - ***MAIN*** : pour la configuration de l'organisation
	 - ***RESULT_DIR*** : Chemin du dossier résultat (***chemin relatif ou absolu, par défaut 'Result'***)
	 - ***LOG_DIR*** : Dossier où stocker les fichiers de log (***chemin relatif ou absolu, par défaut 'Log'***)
	 - ***MAX_ITEMS*** : Nombre d'item maximale à analyser

  - ***ORGANISATION*** : pour la configuration de l'organisation
	 - ***URL*** : Url de l'organisation ArcGIS
	 - ***USER*** : Identifiant de l'utilisateur nommé
	 - ***PASSWORD*** : Mot de passe de l'utilisateur nommé
	 - ***PASSWORD_ENCRYPTED*** : Flag si le mot de passe est encrypté (***True***) ou non (***False***)

  - ***WHATS_NEW*** : pour la configuration liée à l'outil "WhatsNew"
	 - ***FROM_DATE*** : Date au format ***YYYY-MM-DD*** utilisée pour le filtrage sur la date de création

#### <i class="icon-file"></i> Execution

Voir le fichier de commande **AgolTools_GetWebMapsBroken.bat**.

*Egalement disponible depuis la boîte à outils **AgolTools_ArcGISPro** dans ArcGIS Pro.*

#### <i class="icon-file"></i> Résultat

Voir le fichier CSV **AgolTools_WhatsNew*** généré dans le dossier résultat.

La structure du fichier est la suivante :

 - **type** : Type de nouveauté (**user** | **group** | **content**) ;
 - **name** : Libellé ;
 - **created** : Date de création ;
 - **owner** : Propriétaire.


----------


*Rédigé avec https://stackedit.io*
