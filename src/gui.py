from tkinter import *
from tkinter import ttk, messagebox
from Livre import Livre
from Bibliotheque import Bibliotheque
from Membre import Membre
from Exception import MembreInexistantError, LivreInexistantError, LivreIndisponibleError, QuotaEmpruntDepasseError
import Visualisation

biblio = Bibliotheque()
biblio.charger_livres_txt()

fenetre = Tk()
fenetre.geometry('600x600')
fenetre.title("Gestion de bibliothèque")
fenetre.resizable(height=False, width=False)

onglets = ttk.Notebook(fenetre)
onglets.pack(expand=1, fill='both')

frame_livres = Frame(onglets, bg="#dda15e")
frame_membres = Frame(onglets, bg="#dda15e")
frame_emprunts = Frame(onglets, bg="#dda15e")
frame_stats = Frame(onglets, bg="#dda15e")

onglets.add(frame_livres, text="Livres")
onglets.add(frame_membres, text="Membres")
onglets.add(frame_emprunts, text="Emprunts")
onglets.add(frame_stats, text="Statistiques")

# === Onglet LIVRES ===
Label(frame_livres, text="Ajouter un Livre", font=("Arial", 14), bg="#fdf0d5").grid(row=0, column=0, columnspan=2, pady=10)

Label(frame_livres, text="ISBN :", bg="#fdf0d5").grid(row=1, column=0, sticky=E, padx=5, pady=5)
entry_isbn = Entry(frame_livres)
entry_isbn.grid(row=1, column=1)

Label(frame_livres, text="Titre :", bg="#fdf0d5").grid(row=2, column=0, sticky=E, padx=5, pady=5)
entry_titre = Entry(frame_livres)
entry_titre.grid(row=2, column=1)

Label(frame_livres, text="Auteur :", bg="#fdf0d5").grid(row=3, column=0, sticky=E, padx=5, pady=5)
entry_auteur = Entry(frame_livres)
entry_auteur.grid(row=3, column=1)

Label(frame_livres, text="Année de publication :", bg="#fdf0d5").grid(row=4, column=0, sticky=E, padx=5, pady=5)
entry_annee = Entry(frame_livres)
entry_annee.grid(row=4, column=1)

Label(frame_livres, text="Genre :", bg="#fdf0d5").grid(row=5, column=0, sticky=E, padx=5, pady=5)
entry_genre = Entry(frame_livres)
entry_genre.grid(row=5, column=1)

Label(frame_livres, text="Quantité :", bg="#fdf0d5").grid(row=6, column=0, sticky=E, padx=5, pady=5)
entry_qte = Entry(frame_livres)
entry_qte.grid(row=6, column=1)

# Zone d'affichage
affichage_livres = Text(frame_livres, height=8, width=50, wrap=WORD, font=("Arial", 10))
affichage_livres.grid(row=9, column=0, columnspan=2, pady=10)
affichage_livres.config(state=DISABLED)

def afficher_livres():
    livres_text = str(biblio)
    affichage_livres.config(state=NORMAL)
    affichage_livres.delete(1.0, END)
    affichage_livres.insert(END, livres_text)
    affichage_livres.config(state=DISABLED)

def ajouter_livre():
    try:
        isbn = entry_isbn.get()
        titre = entry_titre.get()
        auteur = entry_auteur.get()
        annee = int(entry_annee.get())
        genre = entry_genre.get()
        quantite = int(entry_qte.get())

        livre = Livre(isbn, titre, auteur, annee, genre)
        biblio.ajouter_livre(livre, quantite)

        for e in (entry_isbn, entry_titre, entry_auteur, entry_annee, entry_genre, entry_qte):
            e.delete(0, END)
        afficher_livres()
        messagebox.showinfo("Succès", "📚 Livre ajouté avec succès !")
    except ValueError:
        messagebox.showerror("Erreur", "L'année ou la quantité n'est pas un entier.")

btn_ajouter_livre = Button(frame_livres, text="Ajouter le livre", command=ajouter_livre, bg="#fdf0d5")
btn_ajouter_livre.grid(row=7, column=0, columnspan=2, pady=10)

btn_lister_livres = Button(frame_livres, text="Lister les livres", command=afficher_livres, bg="#fdf0d5")
btn_lister_livres.grid(row=8, column=0, columnspan=2, pady=5)

# === Onglet MEMBRES ===
Label(frame_membres, text="Ajouter un membre", font=("Arial", 14), bg="#fdf0d5").grid(row=0, column=0, columnspan=2, pady=10)

Label(frame_membres, text="ID :", bg="#fdf0d5").grid(row=1, column=0, sticky=E, padx=5, pady=5)
entry_id_membre = Entry(frame_membres)
entry_id_membre.grid(row=1, column=1)

Label(frame_membres, text="Nom complet :", bg="#fdf0d5").grid(row=2, column=0, sticky=E, padx=5, pady=5)
entry_nom_membre = Entry(frame_membres)
entry_nom_membre.grid(row=2, column=1)

def ajouter_membre():
    id = entry_id_membre.get()
    nom = entry_nom_membre.get()
    if id and nom:
        membre = Membre(id, nom)
        biblio.ajouter_membre(membre)
        for e in (entry_id_membre, entry_nom_membre):
            e.delete(0, END)
        messagebox.showinfo("Succès", "👤 Membre ajouté avec succès !")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

btn_ajouter_membre = Button(frame_membres, text="Ajouter un membre", command=ajouter_membre, bg="#fdf0d5")
btn_ajouter_membre.grid(row=7, column=0, columnspan=2, pady=10)

# === Onglet EMPRUNTS ===
Label(frame_emprunts, text="Emprunter un livre", font=("Arial", 14), bg="#fdf0d5").grid(row=0, column=0, columnspan=2, pady=10)

Label(frame_emprunts, text="Id membre :", bg="#fdf0d5").grid(row=1, column=0, sticky=E, padx=5, pady=5)
entry_id_emprunt = Entry(frame_emprunts)
entry_id_emprunt.grid(row=1, column=1)

Label(frame_emprunts, text="Titre du livre :", bg="#fdf0d5").grid(row=2, column=0, sticky=E, padx=5, pady=5)
entry_titre_emprunt = Entry(frame_emprunts)
entry_titre_emprunt.grid(row=2, column=1)

def emprunter_livre():
    id = entry_id_emprunt.get()
    titre = entry_titre_emprunt.get()
    for e in (entry_id_emprunt, entry_titre_emprunt):
        e.delete(0, END)
    try:
        biblio.emprunter_livre(id, titre)
        afficher_livres()
        messagebox.showinfo("Succès", f"✅ Livre '{titre}' emprunté.")
    except (MembreInexistantError, LivreInexistantError, LivreIndisponibleError, QuotaEmpruntDepasseError) as e:
        messagebox.showerror("Erreur", str(e))

btn_emprunter = Button(frame_emprunts, text="Emprunter le livre", command=emprunter_livre, bg="#fdf0d5")
btn_emprunter.grid(row=7, column=0, columnspan=2, pady=10)

Label(frame_emprunts, text="Rendre un livre", font=("Arial", 14), bg="#fdf0d5").grid(row=10, column=0, columnspan=2, pady=10)

Label(frame_emprunts, text="Id membre :", bg="#fdf0d5").grid(row=11, column=0, sticky=E, padx=5, pady=5)
entry_id_retour = Entry(frame_emprunts)
entry_id_retour.grid(row=11, column=1)

Label(frame_emprunts, text="Titre du livre :", bg="#fdf0d5").grid(row=12, column=0, sticky=E, padx=5, pady=5)
entry_titre_retour = Entry(frame_emprunts)
entry_titre_retour.grid(row=12, column=1)

def rendre_livre():
    id = entry_id_retour.get()
    titre = entry_titre_retour.get()
    for e in (entry_id_retour, entry_titre_retour):
        e.delete(0, END)
    try:
        biblio.retourner_livre(id, titre)
        afficher_livres()
        messagebox.showinfo("Succès", f"🔄 Livre '{titre}' retourné.")
    except (MembreInexistantError, LivreInexistantError) as e:
        messagebox.showerror("Erreur", str(e))

btn_rendre = Button(frame_emprunts, text="Rendre le livre", command=rendre_livre, bg="#fdf0d5")
btn_rendre.grid(row=17, column=0, columnspan=2, pady=10)

# === Onglet STATISTIQUES ===
def genre():
    Visualisation.diagramme_genre(biblio)

def top():
    Visualisation.top_diagramme(biblio)

def activite():
    Visualisation.courbe_activite()

btn_genre = Button(frame_stats, text="Statistiques du genre", command=genre, bg="#fdf0d5")
btn_genre.grid(row=1, column=5, columnspan=2, pady=10)

btn_top = Button(frame_stats, text="Top 10 auteurs", command=top, bg="#fdf0d5")
btn_top.grid(row=10, column=5, columnspan=2, pady=10)

btn_acti = Button(frame_stats, text="Courbe d'activité", command=activite, bg="#fdf0d5")
btn_acti.grid(row=20, column=5, columnspan=2, pady=10)

fenetre.mainloop()
