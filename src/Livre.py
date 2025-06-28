class Livre:

    def __init__(self,ISBN,titre,auteur,annee,genre):
        self.ISBN=ISBN
        self.titre=titre
        self.auteur=auteur
        self.annee=annee
        self.genre=genre
        self.statut=True

    def emprunter(self):
        if self.statut==True:
            self.statut=False

    def retourner(self):
        if self.statut==False:
            self.statut=True

    def __str__(self):
        return f"Livre(ISBN={self.ISBN}, titre={self.titre}, auteur={self.auteur}, année={self.annee}, genre={self.genre}, disponibilité={self.statut})"
    
    def est_disponible(self):
        return self.statut