# Projet test machine à café
# Cet outil marche en commande line
# prérequis
$ git clone https://github.com/samiamerni/RT9011.git
 Placer le fichier config.json dans le meme répertoire que le dossier RT9011
# Pour lancer le projet
$ cd RT9011/
$ python3 input.py et choisir un Tp de 1 à 33
# Ce tp fonctionne avec le localhost 
 Les logs vont trouver dans un fichier log.csv après lancement d'un tp
# Explication du fichier de log
["Time","IdTp","reqID","Action","MessageType","lenghtString","Attendu","Observe","Verdic", "Message","VersionOutil"]

time: date de lancement de la requete

idTp: l'identifiant du tp exemple TP/COM/INFO/PRT/BO-01

reqID: le numéro de la requete du tp

Action: le message qu'on envoit

MessageType: la valeur du messagetype

lenghtString: la taille du message

Attendu: ce qu'on attend du test exmple: success

Observe: ce qu'on observe aprés le test exemple: success

Verdic: si la requete a  bien marché exmeple: pass

Message: la totalité du message qu'on a reçu

Version: la version de l'outil développer 
