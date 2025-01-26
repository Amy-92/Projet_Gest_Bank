import itertools
# pour importer un class il faut: from nom_fichier import NomClass
# egalement le json pour la sauvegarde 
import json 
import csv
import re
# import pour les emails
import smtplib, ssl




" ++++++++++++++++++++++++++++++ "
" creation de ma classe compte "
" ++++++++++++++++++++++++++++++ "

class Compte:
    # utilise pour creer les id de facon auto increment
    id = 0
    
    # intialisation des attributs#
    def __init__(self,titulaire='',solde=0, ad_email=""):
        self.id = Compte.id # pour id autoincrement
        Compte.id +=1 # pour l id du compte suivant 
        self.titulaire = titulaire
        self.solde = solde
        self.ad_email = ad_email
        
    "++++ liste des Methodes++++"
    
    #ma methode ajoute un motant au solde 
    def depot(self):
        montant = self.saisie_montant()
        self.solde += montant
        print('Depot de :', montant,' XAF  effectue avec sucess ,votre nouveau solde est :',self.solde,' XAF')
     #---------------fin methode ------------------# 
         
    # ma methode retrait debite le motant du (solde + solde de base) si > "
    def retrait(self):
        soldedeBase = 5000
        montant = self.saisie_montant()
        # a ce niveu la saisie est correct 
        if (montant>self.solde+soldedeBase):
            print(" solde insuffisant pour ce retrait")
            #save trans
        else:
            self.solde -=montant
            print(" Retrait de ",montant," XAF effectue avec succes, votre nouveau solde est : ",self.solde," XAF")
            #save trans
     #---------------fin methode ------------------# 
    
     # ma methode affiche juste le solde du compte
    def afficher_solde(self):
        print("Votre solde est de :",self.solde," XAF")
     #---------------fin methode ------------------# 
    "+++++ Methodes ajoutees++++"
    # ma methode affiche les detaile de mon compte
    def affiche_detail_compte (self):
        print("id :",self.id," Titulaire :",self.titulaire," Email :",self.ad_email," Solde: ",self.solde," XAF")
     #---------------fin methode ------------------# 
    # ma methode pour controler la saisie du montant
    def saisie_montant(self):
        # controle de la saisie du montant
        saisie  = True 
        while saisie :
            try :
                montant = int(input(" Entrez le motant :"))
                if montant < 0 :
                    print('montant doit etre > 0')
                    saisie = True
                else:
                    saisie = False
            except:
                print(" veuillez saisir un montant en chriffre ")
                saisie = True
        return montant   
     #---------------fin methode ------------------# 


" +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ "
" creation de ma classe compteEpagne  qui herite de la classe Compte"
" ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ "
class ComprteEpargne(Compte):
    def __init__(self, titulaire='', solde=0, ad_email="",interet=0.0):
        super().__init__(titulaire, solde, ad_email)
        self.interet = interet
        
        
      
    def ajoutInteret(self):
        # sassurer de que le comte existe
        # existe et position

        if self.solde>= 0  or self.solde<100000 :
            Taux_interet = self.solde * 0.005
        if self.solde>= 100000  or self.solde<1000000 :
            Taux_interet = self.solde * 0.003
        if self.solde>=1000000:
            Taux_interet = self.solde * 0.001
        
        self.solde += Taux_interet
        self.interet = Taux_interet
        self.affiche_detail_compte()
        print(' votre interet annuel est :',self.interet,' et votre solde est :',self.solde)
        
 # fin de la Methode   
        
        
      
        
" +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ "
" creation de ma classe Gestion de compte pour gerer mon compte "
" ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ "

class GestionnaireDeCompte :
    
    # j'initailise ma classe avec une liste de compte vide
    def __init__(self, listeCompte = [],soldedeBase=5000):
        self.listeCompte = listeCompte
        self.soldedeBase = soldedeBase
        
        
    "++++ Creation des Methodes pour la gestion +++++"
    
    # creer un compte , ma methode prend en param le titulaire et un solde initail
    def creerCompte (self):
        # a la creation le solde initial doit etre >= 5000
        print(' creation de compte ')
        titulaire = input('Entrez le nom du Titulaire : ')
        
        saisie  = True # pour verifier si la saisie  du montant est correct
        while saisie :
            try :
                soldeInitial = int(input(" Entrez le montant de votre 1er Recharge  :"))
                if soldeInitial < self.soldedeBase :
                    print('le solde initial doit etre sup a 5000')
                    saisie = True
                else:
                    saisie = False
            except:
                print(" veuillez saisir un montant en chriffre ")
                saisie = True
        
        
        # saise de lemail
        email = input("Entrez votre adresse e-mail : ")
        while not est_email_valide(email):
            email = input("Adresse e-mail non valide. Veuillez réessayer : ")
         
         
        """
        saisieEmailValide = True
            while saisieEmailValide :
                ad_email = str(input("Entrez votre email ?"'\n'))
                if ad_email not "@" :
                    print("  email invalide: " '\n')
                    saisieEmailValide = True
          """ 
        # tanque le montant saisi nest > 5000 on ne qui pas cetts dmande
        # ayant ainsi id,titulaire et sole on peux creer son compte
        # je cree donc une instance de la classe Compte
        
        compte = Compte(titulaire,soldeInitial,email)
        # puis je lajoute a ma liste
        self.listeCompte.append(compte)
        print(" compte Cree avec sucess")
        print('nom du compte :',titulaire,' solde Initiale :', soldeInitial,' XAF')
        compte.affiche_detail_compte()
        compte.afficher_solde()
        
        #+++++++++++++++++++ fin envoie +++++++++++++++++++
        message = 'bonjour ',titulaire,' votre compte est cree avec succes'
        # apres la creation envoyons un mail au client pour lui enforme 
        envoi_email(email,message)
        #---------------fin methode ------------------# 
    
    # creer compte depargne
    def creerCompteEpargne(self):
        
        self.creerCompte()
       #CptEpargne =  ComprteEpargne (sel) 
    
    # methode pour supprimer un compte avec id passe en param
    def supprimerCompte (self):
        print('Identifaint du compte a supprimer  ')
        trouverCompte , positionIdCompte  = self.chercherCompte()
        # si la position est retrouver alors je supprime sinon jinforme quil nexiste pas
        if trouverCompte :
            self.listeCompte.pop(positionIdCompte) 
            print(' Compte Supprimer Avec Succes')
        else :
            print(" Aucun compte trouve")
     #---------------fin methode ------------------#   
       
 
    # Methode pour affiche liste des compte
    def afficherListeComptes(self):
        tailleListe =  len(self.listeCompte)
        if tailleListe == 0 :
            print(' Aucun Compte Enregistre ')
        else :
             print('---------------- 1er possibilite d afficharge-----------')
            # me permet juste dimprime lentete
             print('numero | id du compte | Titulaire |  Email | solde en XAF')
             for i in range(tailleListe): 
                print(i,' |     ',self.listeCompte[i].id,"  |  ",self.listeCompte[i].titulaire,"  |  ",self.listeCompte[i].ad_email ,"  |  ",self.listeCompte[i].solde)
    
    '''
        # je parcours la liste en affichant chaque compe avec le mothode afficheConpte de la classe Compte
        # 1er possibile
        print(' ----------------1er possibilite dafficharge------------')
        for i in range(tailleListe):
            print(i+1,'-')
            self.listeCompte[i].affiche_detail_compte()
            # exp list[i] pointe sur un compte
     

        # 2er possibilite dafficharge-
        print(' ----------------2nd possibilite dafficharge-----------')
        for i in range(tailleListe):
            if i==0 : # me permet juste dimprime lentete
                print('numero | Titulaire | solde en XAF')
            print(i+1,' |     ',self.listeCompte[i].titulaire,"  |  ",self.listeCompte[i].solde)
   
        
        print(' ----------------3 possibilite dafficharge juste du solde de chaque compte------------')
        for i in range(tailleListe):
            print('Compte Numero ',i+1,'-')
            self.listeCompte[i].afficher_solde()
            # exp list[i] pointe sur un compte        
      
    '''
     #---------------fin methode ------------------# 
     
     
    #Methode pour sauvegarder_comptes()
    # sauvegade des compte dans le fichier Json dans un fichier json et csv 
    def sauvegarder_comptes(self):
        # creation du fichier json
        with open("comptes.json", "w") as fichierCompte:
            json.dump([compte.__dict__ for compte in self.listeCompte], fichierCompte)
        print(" Sauvegarde reuissie avec json ")
        
        # creation du fichier csv
        ''''
        with open("comptes.csv", "a", newline='') as fichierCompte:
            ecrit = csv.writer(fichierCompte)
            ecrit.writerows([compte for compte in self.listeCompte])   
            #ecrit.writerows(self.listeCompte[i].id,self.listeCompte[i].titulaireself.listeCompte[i].solde)
            
        print(" Sauvegarde reuissie avec csv ")
       '''
         
    #Methode pour charger_comptes()
    # avec Json
    def charger_comptes(self):
        try:
        # chargement de la liste des compte a apartir de json
             with open("comptes.json", "r") as fichierCompte:
                 donneesCompte = json.load(fichierCompte)
                 print(" chargement succes")
        except:
            print(" Chargement echoue ou aucun chargement a effectue:-->")
            print(NameError)
        
        try :    
            # creation dune nouvelle liste a partie des donnees chargees
            comtesChargees = [Compte(comp["id"],comp["titulaire"],comp["solde"]) for comp in donneesCompte]
        except:
            print(' erreur de chargemnt  prouduite a :', NameError.add_note)
            
        try :    
            #affiche des comptes 
            for comp in comtesChargees :
                comp.affiche_detail_compte()
        except:
            print(' erreur dafficharge  prouduit a :', NameError.name)    
            
            
            
            
            
    #*********** Methodes ajoutees pour la bonne gestion  dans la classe**************#
    
    def chercherCompte(self):
        saisie  = True # pour verifier si la saisie  de lid est correct
        while saisie :
            try :
                idCompte = int(input(" Entrez  l id du compte   :"))
                if idCompte < 0 :
                    print('lid doit etre > 0')
                    saisie = True
                else:
                    saisie = False
            except:
                print(" veuillez saisir un id en chriffre ")
                saisie = True
        
        # a ce niveau id > 0 selectionne
        # pour supprimer un compte il doit existe dans la liste des compte
        trouverCompte = False
        # positionIdCompte nous permet de retouver la position de lid du compte dans la listCompe
        positionIdCompte = 0
        tailleListe =  len(self.listeCompte)
        
        
        # je parcour la liste en verifiant si lidCompte existe puis je recupere la position
        for i in  range (tailleListe):
            if self.listeCompte[i].id == idCompte :  
                trouverCompte = True
                positionIdCompte = i
                print('le compte  de ',self.listeCompte[i].titulaire,' est selectionne' )
            
                
        return  trouverCompte , positionIdCompte  
    #---------------fin methode ------------------# 
     
    #methode pour loperation de depot
    def effectuer_depot(self):
        print('Identifaint du compte  pour le depot  ')
        # on selectionne le compte 
        trouver , positionIdCompte = self.chercherCompte()

        if trouver:
            print('Entrez le montant pour effectuer le depot')
            self.listeCompte[positionIdCompte].depot()
        else:
            print('l operation depot a echoue  : identifiant non trouve')
    #---------------fin methode ------------------# 
          
    #methode pour loperation de retrait
    def effectuer_retrait(self):
        print('Identifiant du compte  pour le retrait  ')
        # on selectionne le compte 
        trouver , positionIdCompte = self.chercherCompte()

        if trouver:
            print('Entrez le montant pour effectuer le Retrait')
            self.listeCompte[positionIdCompte].retrait()
        else:
            print('l operation retrait a echoue , identifiant non trouve') 
    #---------------fin methode ------------------# 
    
# les methodes externe pour les contoles       
# mothode pour le controle des saisie du menu
def controleSaisieMenu(min,max):
    saisie = True # ce booelen permet d;execute le While tanque cest vraie
    # min et max sont les borne des valeur de ma saisie
    choix = 0
    
    while saisie :
        try:
            choix = int(input(" Entrez votre choix : "))
            if choix<= min or choix>max :
                # on informe a lutilisateur deffectue un bon choix
                print(' faites un choix entre ]',min,'-',max,']')
                saisie = True # pour que la boucle recommance
            else :
                saisie = False # ainsi on sort avec un nomb compris ]min, max]
        except:
            # si le   choix = int(input(" Entrez votre choix : ")) echoue
              print(' Entrez un nombre')
              saisie = True # pour que la boucle recommance
    # appres saisie on retourn le choix
    return choix

# methode pour la saisie email valide
def est_email_valide(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


# methode pour envoie des mails
def envoi_email (adresseRec, msg) :
    # on rentre les renseignements pris sur le site du fournisseur
    print("on rentre les renseignements pris sur le site du fournisseur")
    smtp_address = 'smtp.gmail.com'
    smtp_port = 465

    # on rentre les informations sur notre adresse e-mail
    email_address = 'wamypython@gmail.com'
    email_password = 'Python@123'

    # on rentre les informations sur le destinataire
    email_receiver = adresseRec

    # on crée la connexion
    print(' on cree la connexion ')
    context = ssl.create_default_context()
    print(" on essaie l envoi")
    with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
        try:
            # connexion au compte
            print(" entree 1 py")
            server.login(email_address, email_password)
            print(" entree 2")
            # envoi du mail
            server.sendmail(email_address, email_receiver,msg)
            print('envoi effectue avec succes')
        except :
            print('Erreur d envoi type erreur +++++++++ :',TypeError.add_note)
 # fin methode denvoi   
    
    
      
    
    
# fin de la fonction de controle
mesTransactions = {}

"+++++++++++++ code pour tester ++++++++++++++++++++"


'''
++++++++++++++++ debut de mon menu++++++++++++++
ce menu sera egalement repete tanque contunuer est true
'''
gesttionCompte = GestionnaireDeCompte([],5000) 
continuer = True
while continuer :  
    # J'affiche mon Menu
    print(' 1 - Creer un compte ')
    print(' 2 - Effectuer un Depot dans un compte ') 
    print(' 3 - Effectuer un Retrait dans un compte ') 
    print(' 4 - Afficher la liste des comptes ')  
    print(' 5 - Supprimer un compte ')
    # -------- pour gerer compte epagne ---------- #
    print(' 6 - Creer un compte  Epargne') 
    print(' 7 - Calculer votre Epargne ')
     
    print(' 8 - Quitter ')
     
      
    # fin menu
    print('-'*100) #  juste pour creer des espaces apres chaque code
    choix = controleSaisieMenu(0,8) # luser doit choisir entre 1 et 7
    
    if choix== 1:
        gesttionCompte.creerCompte()
        # apres chaque creation je sauvegarde la liste
        gesttionCompte.sauvegarder_comptes()
    elif choix == 2:
        gesttionCompte.effectuer_depot()
    elif choix == 3:
        gesttionCompte.effectuer_retrait()
    elif choix == 4:
        gesttionCompte.afficherListeComptes()
    elif choix == 5:
        gesttionCompte.supprimerCompte()
    elif choix == 6:
        pass
    elif choix == 7:
        pass
    elif choix == 8:
        print(' Merci et Aurevoir')
        # a ce niveau contunuer devient faux
        continuer =False
    else:
        print(' Aucun choix valide')
    
    print('-'*100) #  juste pour creer des espaces apres chaque code
# fin de la boucle
print(' ----------fin du  programme---------------')
input(' Appuyer sur la touche Entre pour Fermer le Programme')