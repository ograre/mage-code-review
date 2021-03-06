import os
import sys
import glob
import re
from repertoire import Repertoire

class Audit:

	def __init__(self):
		"""commentaires"""

	# Fonction qui liste le nombre de namespaces et de modules	
	def nbrNamespaceAndModule(self, path, dossierLog):
		retour=""
		rep = Repertoire()
		codePoolDirs = os.listdir(path+'app/code/')			
		nombreDeModulesTotal = 0
		nombreDeNamespacesTotal = 0	
		for codePool in codePoolDirs:
			namespaceDirs = os.listdir(path+'app/code/'+codePool+'/')
			nombreDeNamespaces = rep.countFolders(path+'app/code/'+codePool+'/')
			nombreDeModules = 0
			nombreDeNamespacesTotal+=nombreDeNamespaces
			for namespace in namespaceDirs:
				nombreDeModules += rep.countFolders(path+'app/code/'+codePool+'/'+namespace+'/')
			nombreDeModulesTotal = nombreDeModulesTotal + nombreDeModules
			retour +=  "- codePool : "+codePool+" ("+str(nombreDeNamespaces)+" namespaces, "+str(nombreDeModules)+" modules) <br />\n"
		retour+="\n"
		retour+="<br  />  <strong>Total  :</strong>  "+str(nombreDeNamespacesTotal)+" namespaces et "+str(nombreDeModulesTotal)+" modules. \n"
		
		return retour


	# Fonction qui analyse les templates
	def analyserLeCode(self, path, dossierLog, tab):	
		#DEBUT LOADS IN TEMPLATES			
		rep = Repertoire()	
		if(tab is None):
			results = {}
			#code
			results['code_search_for_new']=[]
			results['code_global_php']=[]
			results['code_mysql']=[]

			#templates
			results['template_search_for_load']=[]
			results['template_search_for_getblock']=[]
			results['template_search_for_createblock']=[]
			results['template_search_for_new']=[]
			results['template_global_php']=[]
			results['template_mysql']=[]
		else:
			results=tab

		dirs = os.listdir(path)	
		for ligne in dirs:		
			if os.path.isdir(path+ligne):
				self.analyserLeCode(path+ligne+"/", dossierLog, results)
			else:
				#ici on est dans chaque fichier du dossier
				if(re.search(r"app",path+ligne)):
					#si dans le code
					if(re.search(r"app\/code\/core",path+ligne)):
						continue

					#si dans le code
					if(re.search(r"app\/code",path+ligne)):

						#ici on est dans chaque fichier PHP
						if(ligne.endswith('.php')):
						
							#new dans le  code
							search_for_new =self.searchForNew(path+ligne, dossierLog,1)
							if(len(search_for_new) is not 0):
								results['code_search_for_new'].append(search_for_new)

							#globalPHP dans le  code
							search_for_globalphp =self.searchForPhpGlobals(path+ligne, dossierLog)
							if(len(search_for_globalphp) is not 0):
								results['code_global_php'].append(search_for_globalphp)

							#fonctions mysql_ dans le code
							search_for_mysql =self.searchForMysql(path+ligne, dossierLog)
							if(len(search_for_mysql) is not 0):
								results['code_mysql'].append(search_for_mysql)

							#A FAIRE LOAD COUTEUX

					#si dans design
					if(re.search(r"app\/design",path+ligne)):	
			
						#ici on est dans chaque fichier du dossier
						if(ligne.endswith('.phtml')):

							#load dans les templates
							search_for_load =self.searchForLoad(path+ligne, dossierLog)
							if(len(search_for_load) is not 0):
								results['template_search_for_load'].append(search_for_load)

							#getblock dans les templates
							search_for_getblock =self.searchForGetblock(path+ligne, dossierLog)
							if(len(search_for_getblock) is not 0):
								results['template_search_for_getblock'].append(search_for_getblock)

							#createblock dans les templates
							search_for_createblock =self.searchForCreateblock(path+ligne, dossierLog)
							if(len(search_for_createblock) is not 0):
								results['template_search_for_createblock'].append(search_for_createblock)
					
							#new dans les templates
							search_for_new =self.searchForNew(path+ligne, dossierLog, 0)
							if(len(search_for_new) is not 0):
								results['template_search_for_new'].append(search_for_new)

							#globalPHP dans les templates
							search_for_globalphp =self.searchForPhpGlobals(path+ligne, dossierLog)
							if(len(search_for_globalphp) is not 0):
								results['template_global_php'].append(search_for_globalphp)

							#fonctions mysql_ dans le code
							search_for_mysql =self.searchForMysql(path+ligne, dossierLog)
							if(len(search_for_mysql) is not 0):
								results['template_mysql'].append(search_for_mysql)

							
	
		return results

	#
	# Fonction qui repere les loads dans les templates
	#
	def searchForLoad(self, path, dossierLog):
		fichier = open(path, 'r')
		nbrLigne=0	
		nbrLoads=0		
		retoursAll=[]
		for ligne in fichier:
			nbrLigne+=1	
			result = re.search(r"->load\(",ligne)					
			if result is not None:
				retours = {}
				retours['path'] = path
				retours['ligne'] = str(nbrLigne)  
				retours['contents']=ligne.strip(" \t\n\r")	
				retoursAll.append(retours)
				nbrLoads+=1
		return retoursAll


	#
	# Fonction qui repere les getBlock dans les templates
	#
	def searchForGetblock(self, path, dossierLog):
		fichier = open(path, 'r')
		nbrLigne=0	
		nbrLoads=0		
		retoursAll=[]
		for ligne in fichier:
			nbrLigne+=1	
			result = re.search(r"->getBlock\(",ligne)					
			if result is not None:
				retours = {}
				retours['path'] = path
				retours['ligne'] = str(nbrLigne)  
				retours['contents']=ligne.strip(" \t\n\r")	
				retoursAll.append(retours)
				nbrLoads+=1
		return retoursAll

	#
	# Fonction qui repere les getBlock dans les templates
	#
	def searchForPhpGlobals(self, path, dossierLog):
		fichier = open(path, 'r')
		nbrLigne=0	
		nbrLoads=0		
		retoursAll=[]
		for ligne in fichier:
			nbrLigne+=1	
			post = re.search(r"\$_POST",ligne)
			get = re.search(r"\$_GET",ligne)
			glo = re.search(r"\$_GLOBAL",ligne)	
			if ( (post is not None) or (get is not None) or (glo is not None) ):
				retours = {}
				retours['path'] = path
				retours['ligne'] = str(nbrLigne)  
				retours['contents']=ligne.strip(" \t\n\r")	
				retoursAll.append(retours)
				nbrLoads+=1
		return retoursAll

	#
	# Fonction qui repere les fonctions mysql non magento dans le code
	#
	def searchForMysql(self, path, dossierLog):
		fichier = open(path, 'r')
		nbrLigne=0	
		nbrLoads=0		
		retoursAll=[]
		for ligne in fichier:
			nbrLigne+=1	
			mysql = re.search(r"mysql_",ligne)	
			if ( (mysql is not None)):
				retours = {}
				retours['path'] = path
				retours['ligne'] = str(nbrLigne)  
				retours['contents']=ligne.strip(" \t\n\r")	
				retoursAll.append(retours)
				nbrLoads+=1
		return retoursAll

	#
	# Fonction qui repere les createBlock dans les templates
	#
	def searchForCreateblock(self, path, dossierLog):
		fichier = open(path, 'r')
		nbrLigne=0	
		nbrLoads=0		
		retoursAll=[]
		for ligne in fichier:
			nbrLigne+=1	
			result = re.search(r"->createBlock\(",ligne)
			resultWidgetName = re.search("customer/widget_",ligne)					
			if ( result is not None ) and ( resultWidgetName is None ):
				retours = {}
				retours['path'] = path
				retours['ligne'] = str(nbrLigne)  
				retours['contents']=ligne.strip(" \t\n\r")	
				retoursAll.append(retours)
				nbrLoads+=1
		return retoursAll


	#
	# Fonction qui repere les new dans les templates
	# si code=1 on est dans le code
	# si code=0 on est dans les templates
	#
	def searchForNew(self, path, dossierLog, code):
		fichier = open(path, 'r')
		nbrLigne=0	
		nbrLoads=0
		isInScript=0	
		isInComment=0
		retoursAll=[]
		for ligne in fichier:
			inscript_one = re.search("text/javascript",ligne)
			inscript_two = re.search("script",ligne)
			inscript_three = re.search("<script>",ligne)
			outcript = re.search("</script",ligne)		
			intraduct = re.search("__\(",ligne)

			if(code is 1):
				varien = re.search("new Varien",ligne)
				stdclass = re.search("new StdClass",ligne)
				zend = re.search("new Zend",ligne)	
				exception = re.search("Exception",ligne)
				soap = re.search("new SoapClient",ligne)	
				simplexml = re.search("new SimpleXMLElement",ligne)
				arrayiterator = re.search("new ArrayIterator",ligne)
				stdclassbis = re.search("new stdClass",ligne)	
				date = re.search("DateTime",ligne)
			

			incomment = re.search("\/\*",ligne)
			outcomment = re.search("\*\/",ligne)

			if ( (( inscript_one  is not None ) and ( inscript_two is not None )) or ( inscript_three is not None )  ):
				isInScript=1
			if(outcript is not None):
				isInScript=0

			if(incomment is not None):
				isInComment=1
			if(outcomment is not None):
				isInComment=0

			nbrLigne+=1	
			result = re.search("new ",ligne)				
			if ( result is not None ) and ( isInScript is not  1) and (intraduct is None)  and (isInComment is not 1):
				if( (code is not 1) or ((varien is None) and (stdclass is None) and (zend is None) and (exception is None)  and (soap is None) and (exception is None)  and (simplexml is None) and (arrayiterator is None) and (stdclassbis is None) and (date is None))):
					retours = {}
					retours['path'] = path
					retours['ligne'] = str(nbrLigne)  
					retours['contents']=ligne.strip(" \t\n\r")	
					retoursAll.append(retours)
					nbrLoads+=1
		return retoursAll


