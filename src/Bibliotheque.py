from Livre import Livre
from Membre import Membre
import datetime
from Exception import MembreInexistantError
from Exception import LivreInexistantError
from Exception import LivreIndisponibleError
from Exception import QuotaEmpruntDepasseError
class Bibliotheque:

    max_emprunts=4

    def __init__(self):
        self.livres={}
        self.membres={}

    def ajouter_livre(self,livre:Livre,quantite=1):
        if livre.ISBN in self.livres:
            self.livres[livre.ISBN]["stock"]+=quantite
        else:
            self.livres[livre.ISBN]={
                "livre":livre,
                "stock":quantite
            }

    def supprimer_livre(self,livre:Livre):
        if livre.ISBN in self.livres:
            if self.livres[livre.ISBN]["stock"]>1:
                self.livres[livre.ISBN]["stock"]-=1
            else:
                del self.livres[livre.ISBN]

    def ajouter_membre(self,membre:Membre):
        if membre.ID not in self.membres:
            self.membres[membre.ID]=membre

    def emprunter_livre(self,id_membre,titre_livre):
        membre=self.membres.get(id_membre)
        if membre is None:
            raise MembreInexistantError()
        livre_info=None
        for info in self.livres.values():
            if info["livre"].titre.lower()==titre_livre.lower():
                livre_info=info
                break
        if livre_info is None :
            raise LivreInexistantError()
        if livre_info["stock"]<=0:
            raise LivreIndisponibleError()
        if len(membre.livres_empruntes)>=self.max_emprunts:
            raise QuotaEmpruntDepasseError()
        membre.emprunter_livre(livre_info["livre"])
        livre_info["stock"]-=1
        self.sauvegarder_historique_csv(livre_info["livre"],membre,"emprunt")

    def retourner_livre(self,id_membre,titre_livre):
        membre=self.membres.get(id_membre)
        if membre is None:
            raise MembreInexistantError()
        livre_info=None
        for info in self.livres.values():
            if info["livre"].titre.lower()==titre_livre.lower():
                livre_info=info
                break
        if livre_info is None:
            raise LivreInexistantError
        livre=livre_info["livre"]
        if livre not in membre.livres_empruntes:
            print("ce membre n'a pas emprunté ce livre .")
            return
        membre.retourner_livre(livre)
        livre_info["stock"]+=1
        self.sauvegarder_historique_csv(livre,membre,"retour")

    def __str__(self):
        livres_dispo=[info["livre"].titre for info in self.livres.values() if info["stock"]>0]
        livres_nondispo=[info["livre"].titre for info in self.livres.values() if info["stock"]==0]
        return( f"la liste des livre disponibles : {livres_dispo}\n"
               f"les livres empruntés : {livres_nondispo}")
    
    def sauvegarder_livres_txt(self):
        with open("data/livres.txt","w") as l:
            for isbn,info in self.livres.items():
                livre=info["livre"]
                stock=info["stock"]
                statut="disponible" if stock>0 else "emprunté"
                ligne=f"{livre.ISBN};{livre.titre};{livre.auteur};{livre.annee};{livre.genre};{statut};{stock}\n"
                l.write(ligne)

    def sauvegarder_membre_txt(self):
        with open("data/membres.txt","w") as m:
            for id,membre in self.membres.items():
                titre_list=[livre.titre for livre in membre.livres_empruntes]
                chaine_titre=",".join(titre_list)
                ligne=f"{membre.ID};{membre.nom};{chaine_titre}\n"
                m.write(ligne)

    def sauvegarder_historique_csv(self,livre:Livre,membre:Membre,action):
        with open("data/historique.csv","a") as h:
            date=str(datetime.date.today())
            ligne=f"{date};{livre.ISBN};{membre.ID};{action}\n"
            h.write(ligne)
    
    def charger_livres_txt(self):
        with open("data/livres.txt","r") as L:
            for f in L:
                champs =f.split(";")
                isbn=champs[0]
                titre=champs[1]
                auteur=champs[2]
                annee=int(champs[3])
                genre=champs[4]
                statut=champs[5]
                stock=int(champs[6])
                livre=Livre(isbn,titre,auteur,annee,genre)
                self.livres[isbn]={
                    "livre":livre,
                    "stock":stock
                }
    def charger_membres_txt(self):
        with open("data/membres.txt","r") as m:
            for f in m:
                champs=f.split(";")
                id=champs[0]
                nom=champs[1]
                titres_str=champs[2].strip()
                liste_titres=titres_str.split(",") if titres_str else[]
                membre=Membre(id,nom)
                for titre in liste_titres:
                    for info in self.livres.values():
                        if info["livre"].titre==titre:
                            membre.livres_empruntes.append(info["livre"])
                self.membres[id]=membre

            
