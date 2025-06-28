from Livre import Livre
class Membre:

    def __init__(self,ID,nom):
        self.ID=ID
        self.nom=nom
        self.livres_empruntes=[]

    def emprunter_livre(self,livre:Livre):
        if livre not in self.livres_empruntes and livre.statut==True :
            livre.emprunter()
            self.livres_empruntes.append(livre)

    def retourner_livre(self,livre:Livre):
        if livre in self.livres_empruntes:
            livre.retourner()
            self.livres_empruntes.remove(livre)
            
    def __str__(self):
        return f"le membre nommé {self.nom} portant l'id {self.ID} a emprunté {len(self.livres_empruntes)} livres"
