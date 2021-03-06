# -*-coding:Latin-1 -*
from utils.audit import Audit

audit = Audit()

dossierLog =  '/home/pierre/Documents/Projects/MagentoCodeAnalysis/logs/'
path = '/home/pierre/Documents/Projects/courir/courir/'


#on lance toutes les recherches
result = audit.analyserLeCode(path, dossierLog, None)
etatPlateforme = audit.nbrNamespaceAndModule(path,dossierLog)


#on construit le rapport


############################
###   Debut du fichier   ###
############################

loadsTemplatesLog = open(dossierLog+"load-in-template.html", "w")
loadsTemplatesLog.write("<head>")
loadsTemplatesLog.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">")
loadsTemplatesLog.write("</head>")
loadsTemplatesLog.write("<body>")

############################
###     ETAT GENERAL     ###
############################
loadsTemplatesLog.write("<h2>Etat général de la plateforme</h2>\n")
### Analyse des modules ###
loadsTemplatesLog.write("<h3>Modules et namespaces</h3>\n")
loadsTemplatesLog.write(etatPlateforme)

############################
###      TEMPLATES       ###
############################
loadsTemplatesLog.write("<h2>Etat des templates</h2>\n")

#############################
### Loads dans templates  ###
loadsTemplatesLog.write("<h3>Loads dans les templates</h3>\n")
loadsTemplatesLog.write("<p>Ces appels prennent beaucoup de charges et ne permettent pas à magento d'utiliser le cache correctement. Il faut absolument sortir ces appels des fichiers des templates (.phtml) et les effectuer correctement dans les blocs.</p>\n")
loadsTemplatesLog.write("<table style=\"border:1px solid #000;text-align:left;\">\n")
loadsTemplatesLog.write("<tr><th>Fichier</th><th style=\"width:100px;\">Ligne</th><th>Code concerné</th></tr>\n")

tab=result['template_search_for_load']
for res in tab:
	loadsTemplatesLog.write("<tr><td>"+res[0]['path']+"</td><td>"+res[0]['ligne']+"</td><td>"+res[0]['contents']+"</td></tr>\n")
loadsTemplatesLog.write("</table>\n")

############################
### getBlock dans templates  ###
loadsTemplatesLog.write("<h3>GetBlock dans les templates</h3>\n")
loadsTemplatesLog.write("<p>Ces appels empèchent magento d'utiliser le cache correctement. Il faut absolument sortir ces appels des fichiers des templates (.phtml) et utiliser correctement les layouts.</p>\n")
loadsTemplatesLog.write("<table style=\"border:1px solid #000;text-align:left;\">\n")
loadsTemplatesLog.write("<tr><th>Fichier</th><th style=\"width:100px;\">Ligne</th><th>Code concerné</th></tr>\n")

tab=result['template_search_for_getblock']
for res in tab:
	loadsTemplatesLog.write("<tr><td>"+res[0]['path']+"</td><td>"+res[0]['ligne']+"</td><td>"+res[0]['contents']+"</td></tr>\n")
loadsTemplatesLog.write("</table>\n")

###################################
### createBlock dans templates  ###
loadsTemplatesLog.write("<h3>CreateBlock dans les templates</h3>\n")
loadsTemplatesLog.write("<p>Ces blocs ne sont pas crées correctement, leur création devrait être dans le layout ou dans un contrôleur</p>\n")
loadsTemplatesLog.write("<table style=\"border:1px solid #000;text-align:left;\">\n")
loadsTemplatesLog.write("<tr><th>Fichier</th><th style=\"width:100px;\">Ligne</th><th>Code concerné</th></tr>\n")

tab=result['template_search_for_createblock']
for res in tab:
	loadsTemplatesLog.write("<tr><td>"+res[0]['path']+"</td><td>"+res[0]['ligne']+"</td><td>"+res[0]['contents']+"</td></tr>\n")
loadsTemplatesLog.write("</table>\n")


###################################
### new dans templates  ###
loadsTemplatesLog.write("<h3>New dans les templates</h3>\n")
loadsTemplatesLog.write("<p>On utilise jamais une instanciation directement via un \"new\" sur magento.</p>\n")
loadsTemplatesLog.write("<table style=\"border:1px solid #000;text-align:left;\">\n")
loadsTemplatesLog.write("<tr><th>Fichier</th><th style=\"width:100px;\">Ligne</th><th>Code concerné</th></tr>\n")

tab=result['template_search_for_new']
for res in tab:
	loadsTemplatesLog.write("<tr><td>"+res[0]['path']+"</td><td>"+res[0]['ligne']+"</td><td>"+res[0]['contents']+"</td></tr>\n")
loadsTemplatesLog.write("</table>\n")

###################################
### PHP globals dans templates  ###
loadsTemplatesLog.write("<h3>Appels PHP globals les templates</h3>\n")
loadsTemplatesLog.write("<p>On utilise jamais ces fonctions dans magento pour des raisons de sécurité. à la place de $_POST préférer $this->getRequest()->getPost() par exemple.</p>\n")
loadsTemplatesLog.write("<table style=\"border:1px solid #000;text-align:left;\">\n")
loadsTemplatesLog.write("<tr><th>Fichier</th><th style=\"width:100px;\">Ligne</th><th>Code concerné</th></tr>\n")

tab=result['template_global_php']
for res in tab:
	loadsTemplatesLog.write("<tr><td>"+res[0]['path']+"</td><td>"+res[0]['ligne']+"</td><td>"+res[0]['contents']+"</td></tr>\n")
loadsTemplatesLog.write("</table>\n")

###################################
### Fonctions mysql dans templates  ###
loadsTemplatesLog.write("<h3>Appels aux fonctions mysql dans les templates</h3>\n")
loadsTemplatesLog.write("<p>Magento utilise des objets pour dialoguer directement avec la base de donnée, il ne faut jamais utiliser les fonctions \"mysql_\" de php.</p>\n")
loadsTemplatesLog.write("<table style=\"border:1px solid #000;text-align:left;\">\n")
loadsTemplatesLog.write("<tr><th>Fichier</th><th style=\"width:100px;\">Ligne</th><th>Code concerné</th></tr>\n")

tab=result['template_mysql']
for res in tab:
	loadsTemplatesLog.write("<tr><td>"+res[0]['path']+"</td><td>"+res[0]['ligne']+"</td><td>"+res[0]['contents']+"</td></tr>\n")
loadsTemplatesLog.write("</table>\n")

############################
###         CODE         ###
############################

loadsTemplatesLog.write("<h2>Etat du code</h2>\n")

#########################
### new dans le code  ###
loadsTemplatesLog.write("<h3>New dans le code</h3>\n")
loadsTemplatesLog.write("<p>On utilise jamais une instanciation directement via un \"new\" sur magento.</p>\n")
loadsTemplatesLog.write("<table style=\"border:1px solid #000;text-align:left;\">\n")
loadsTemplatesLog.write("<tr><th>Fichier</th><th style=\"width:100px;\">Ligne</th><th>Code concerné</th></tr>\n")

tab=result['code_search_for_new']
for res in tab:
	loadsTemplatesLog.write("<tr><td>"+res[0]['path']+"</td><td>"+res[0]['ligne']+"</td><td>"+res[0]['contents']+"</td></tr>\n")
loadsTemplatesLog.write("</table>\n")

#################################
### PHP globals dans le code  ###
loadsTemplatesLog.write("<h3>Appels PHP globals le code</h3>\n")
loadsTemplatesLog.write("<p>On utilise jamais ces fonctions dans magento pour des raisons de sécurité. à la place de $_POST préférer $this->getRequest()->getPost() par exemple.</p>\n")
loadsTemplatesLog.write("<table style=\"border:1px solid #000;text-align:left;\">\n")
loadsTemplatesLog.write("<tr><th>Fichier</th><th style=\"width:100px;\">Ligne</th><th>Code concerné</th></tr>\n")

tab=result['code_global_php']
for res in tab:
	loadsTemplatesLog.write("<tr><td>"+res[0]['path']+"</td><td>"+res[0]['ligne']+"</td><td>"+res[0]['contents']+"</td></tr>\n")
loadsTemplatesLog.write("</table>\n")

#################################
###    Mysql dans le code  ###
loadsTemplatesLog.write("<h3>Appels aux fonctions mysql dans le code</h3>\n")
loadsTemplatesLog.write("<p>Magento utilise des objets pour dialoguer directement avec la base de donnée, il ne faut jamais utiliser les fonctions \"mysql_\" de php.</p>\n")
loadsTemplatesLog.write("<table style=\"border:1px solid #000;text-align:left;\">\n")
loadsTemplatesLog.write("<tr><th>Fichier</th><th style=\"width:100px;\">Ligne</th><th>Code concerné</th></tr>\n")

tab=result['code_mysql']
for res in tab:
	loadsTemplatesLog.write("<tr><td>"+res[0]['path']+"</td><td>"+res[0]['ligne']+"</td><td>"+res[0]['contents']+"</td></tr>\n")
loadsTemplatesLog.write("</table>\n")


############################
###   Fin du fichier     ###
############################

loadsTemplatesLog.write("</body>")
loadsTemplatesLog.close()

















############################
###     ANALYSE BDD      ###
############################

# violation de contraintes etrangéres en bdd ?
# presence de traduction dans core_translate (aucune attendue)
# url relative dans le contenu statique (pages et blocs cms)
# table de logs volumineuse
# custom url pour l'admin
# utilisateurs et droits API pas trop nombreux ?
# on verifie que le package utilisé n'est pas default (templates et skin)  (surcharge du theme obligée  pour etre propre)
# nombre de website /store/storeview
# taille des tables de logs
# taille de la table sales_flat_quote
# taxes, montants renseignés en BO HT ou TTC ?
# flat_table (produits et catégorie) activé ?
# nombre de produits
# nombre de clients
# nombre de catégories
# nombre d'inscrits à la newsletter
# nombre de commandes
# compilation activée ?
# utilisation d'un CDN ?
#
#################################################
###     TESTS FICHIERS                        ###
#################################################
# est ce que le core a été modifié ?
# comparaison index.php avec le standard
# presence du downloader
# nombre de surcharges / conflits ?
# module local Mage ?
# encodage non utf8
# .htaccess limitant les acces dans app, lib, var et tout autre dossier non media ou js/theme
# liste des modules commaunautaires => qu'est ce qu'ils font ? => faire un tableau avec un descriptif, nom = Attribuer une note de "confiance"


#################################################
###     COMPARAISON PERF NATIF / PAS NATIF    ###
#################################################
# mesure des pages
# mesure des actions...

#########################################################################
###     PERFORMANCE FRONT (prod ou url accessible depuis internet )   ###
#########################################################################
# analyse css / js etc...comme analytics
# analyse scripts qu'on pourrait mettre en asynchrone
# google page speed insight

##############################
###     INIT DE L'AUDIT    ###
##############################
# description de l'environnement de test (pc, os,  version apache, php, mysql, editeur..)


#### CODE
# getSingleton dnas les templates
# url relatives dans les templates ?
# css en dure dans les fichiers
# var_dump, print_r, zend_debug::dump()
# chaines non encapsulé par un helper de traduction
# code lourd (foreach avec load,..)
# custom url pour l'admin (pas "admin")
# fonction header('Location...);
# on compte le nombre de rewrite
# activation du developer mode
# methode de cache utilisée ?
# version de magento ?



