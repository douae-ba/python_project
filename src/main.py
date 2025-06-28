from Livre import Livre
from Membre import Membre
from Bibliotheque import Bibliotheque
import Visualisation as Visualisation
from Exception import MembreInexistantError
from Exception import LivreInexistantError
from Exception import LivreIndisponibleError
from Exception import QuotaEmpruntDepasseError
biblio=Bibliotheque()
biblio.charger_livres_txt()
biblio.charger_membres_txt()
while(True):
    print("     ===== GESTION BIBLIOTHEQUE=====")
    print("\t1 . Ajouter un livre\n\t2 . Inscrire un membre\n\t3 . Emprunter un livre\n\t4 . Rendre un livre\n\t5 . Lister tous les livres\n\t6 . Afficher les statistiques\n\t7 . Sauvegarder et quitter")
    choix=input("entrez votre choix : ")
    match choix :
        case "1":
            print("=== Ajouter un livre ===")
            isbn=input("ISBN : ")
            titre=input("Titre : ")
            auteur=input("Auteur : ")
            try :
                annee=int(input("année de publication : "))
            except ValueError:
                print("Année invalide.")
                break
            genre=input("Genre : ")
            try:
                quantite=int(input("Quantité à ajouter : "))
            except ValueError:
                print("quantité invalide.")
                break
            livre=Livre(isbn,titre,auteur,annee,genre)
            biblio.ajouter_livre(livre,quantite)
            print(livre)
        case "2":
            print("=== Inscrire un membre ===")
            id=input("ID du membre : ")
            nom=input("Nom du memebre : ")
            membre=Membre(id,nom)
            biblio.ajouter_membre(membre)
            print(membre)
        case "3" :
            print("=== Emprunter un livre ===")
            id_membre=input("id du membre : ")
            titre=input("titre du livre : ")
            try:
                biblio.emprunter_livre(id_membre,titre)
                print("✅ Livre emprunté avec succès.")
            except(MembreInexistantError,LivreInexistantError,LivreIndisponibleError,QuotaEmpruntDepasseError) as e :
                print(f"❌ Erreur : {e}")
        case "4" :
            print("=== Rendre un livre ===")
            id_membre=input("id du membre : ")
            titre=input("titre du livre : ")
            try:
                biblio.retourner_livre(id_membre,titre)
                print("✅ Livre retourné avec succès.")
            except(MembreInexistantError,LivreInexistantError) as e:
                print(f"❌ Erreur : {e}")
        case "5":
            print("=== Lister tous les livres ===")
            print(biblio)
        case "6":
            print("=== affichage des statistiques ===")
            Visualisation.diagramme_genre(biblio)
            Visualisation.top_diagramme(biblio)
            Visualisation.courbe_activite()
        case "7":
            print("=== Sauvgarder ===")
            biblio.sauvegarder_livres_txt()
            biblio.sauvegarder_membre_txt()
            print("Données sauvegaedées.")
            break


