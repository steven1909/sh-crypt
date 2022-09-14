#!/bin/bash
#################################################
#                                               #
#		   GIT TAGGING                  #
#                                               #
#################################################

# NOTICE : 
# Ce script va tagger la branche en cours à partir du numéro de version renseigné dans le code Python du package :
# Il doit être utilisé via la commande : make tag 
#
# ROLLBACK :
# Si vous souhaitez annuler un tag que vous viendriez de faire. il faut pour ça taper les lignes de commande suivantes :
# git push --delete origin YOUR_TAG_NAME
# git tag --delete YOUR_TAG_NAME
# Si tout se passe bien vous revenez dans l'état précédent votre tag.

VERSION_REPO_GIT=$(python -c "import sh_crypt;print(sh_crypt.__version__)")

#Etape 1 : Vérification que vous êtes dans la branche dev
echo -e "Etape 1/5 : Vérification que vous êtes dans la branche master."
if [ $(git rev-parse --abbrev-ref HEAD) = 'master' ];then
	echo -e "\t OK - Vous êtes dans la branche master."
else
	echo -e "\t ERREUR - Vous n'êtes pas dans la branche master, vous êtes actuellement dans la branche" $(git rev-parse --abbrev-ref HEAD)
	exit 1
fi

#Etape 2 : Vérification que le tag n'existe pas déjà.
echo -e "Etape 2/5 : Vérification que le tag $VERSION_REPO_GIT n'existe pas déjà."
git fetch --tags
CHECK_TAG_GIT=$(git tag -l $VERSION_REPO_GIT | grep -c $VERSION_REPO_GIT)

if [ "$CHECK_TAG_GIT" = "0" ];then
	echo -e "\t OK - Le tag est valide."
else
	echo -e "\t ERREUR - Le tag est déjà utilisé sur le serveur. Vous devez choisir un nouveau numéro de version."
	exit 1
fi

#Etape 3 : Vérification que la zone de stage Git est vide.
echo -e "Etape 3/5 : Controle que la zone de stage soit vide."
STAGE_FILE=$(git status | grep -c "git add")
if [ $STAGE_FILE = 0 ];then
	echo -e "\t OK - La zone de staged est vide."
else
	echo -e "\t ERREUR - La zone de staged n'est pas vide. Commiter ou stasher tous vos fichiers avant."
	exit 1
fi

#Etape 4 : On tag le repo_git actuel avec la version qui est dans le fichier version
echo -e "Etape 4/5 : Taging Git."
git tag -a $VERSION_REPO_GIT -m"version $VERSION_REPO_GIT"

#Etape 5 : On pousse les derniers commit sur le serveur
echo -e "Etape 5/5 : Mise à jour du serveur Git."
echo -e "\t Mise à jour de la branche master du serveur."
git push origin master
echo -e "\t Pousse du nouveau tag de version Git."
git push origin $VERSION_REPO_GIT --tags

echo -e ".... FINI ...."
echo -e "Le dernier numéro de version du repo : $VERSION_REPO_GIT"
