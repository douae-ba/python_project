#  Projet Python – Système de Gestion de Bibliothèque Moderne

##  Objectif

Créer une application Python professionnelle pour gérer une bibliothèque avec :

-  **Interface graphique moderne** avec PyQt5
-  **Design premium** avec thème sombre et animations
-  **Programmation orientée objet (POO)**
-  **Gestion des erreurs** avec exceptions personnalisées
-  **Sauvegarde/chargement** des données (`txt`, `csv`)
-  **Visualisations interactives** avec `matplotlib`
-  **Expérience utilisateur moderne** et intuitive

---

##  Fonctionnalités

###  Gestion des Livres
-  Ajouter un livre avec ISBN, titre, auteur, année, genre et quantité
-  Supprimer un livre
-  Afficher tous les livres disponibles et empruntés
-  Recherche par titre

###  Gestion des Membres
-  Enregistrer un nouveau membre
-  Suivi des emprunts par membre
-  Quota d'emprunts configurables (max 4 livres)

###  Gestion des Emprunts
-  Emprunter un livre avec vérifications automatiques
-  Retourner un livre
-  Historique complet des transactions
-  Validation en temps réel de la disponibilité

###  Statistiques Avancées
-  **Diagramme des genres** : Visualisation de la répartition par genre
-  **Top 10 auteurs** : Les auteurs les plus présents
-  **Courbe d'activité** : Évolution des emprunts dans le temps

---

##  Interface Moderne

### Design Features
- 🌙 **Thème sombre élégant** avec palette cyan/bleu
- 💎 **Cartes flottantes** avec ombres portées
- ✨ **Animations smooth** sur interactions
- 🎯 **Navigation par onglets** intuitive
- 📱 **Design responsive** et professionnel

### Technologies UI
- **PyQt5** : Framework moderne pour interfaces graphiques
- **Style CSS-like** : Personnalisation complète
- **Effets visuels** : Dégradés, ombres, hover effects
- **Icônes emoji** : Interface conviviale et moderne

---

## Installation

### Prérequis
- Python 3.7+
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```


## Lancer le Programme

### Mode Graphique (Recommandé)

```bash
python src/gui.py
```

**Interface PyQt5 moderne avec :**
- 📚 Onglet Livres : Gestion complète du catalogue
- 👥 Onglet Membres : Enregistrement et suivi
- 🔄 Onglet Emprunts : Transactions facilitées
- 📊 Onglet Statistiques : Visualisations interactives

### Mode CLI (Ligne de commande) 💻

```bash
python src/main.py --cli
```

**Menu interactif :**
```
===== MENU BIBLIOTHÈQUE =====
1. Ajouter un livre
2. Enregistrer un membre 
3. Emprunter un livre
4. Retourner un livre
5. Lister tous les livres
6. Afficher les statistiques
7. Sauvegarder et quitter
```

---

## 📁 Structure du Projet

```
projet_bibliotheque/
├── src/
│   ├── main.py              # Point d'entrée CLI
│   ├── gui.py               # Interface PyQt5 moderne
│   ├── Livre.py             # Classe Livre
│   ├── Membre.py            # Classe Membre
│   ├── Bibliotheque.py      # Classe principale
│   ├── Exception.py         # Exceptions personnalisées
│   └── Visualisation.py     # Graphiques matplotlib
├── data/
│   ├── livres.txt           # Base de données livres
│   ├── membres.txt          # Base de données membres
│   └── historique.csv       # Historique des transactions
├── requirements.txt         # Dépendances Python
└── README.md               # Documentation
```

---

## 🎯 Exemples d'Utilisation

### Ajouter un Livre (GUI)
1. Ouvrir l'onglet **📚 Livres**
2. Remplir les champs (ISBN, Titre, Auteur, etc.)
3. Cliquer sur **➕ Ajouter le Livre**
4. Confirmation avec message de succès ✅

### Emprunter un Livre (GUI)
1. Onglet **🔄 Emprunts**
2. Entrer l'**ID Membre** et le **Titre du Livre**
3. Cliquer sur **📤 Emprunter**
4. Vérification automatique et mise à jour du stock

### Visualiser les Statistiques (GUI)
1. Onglet **📊 Statistiques**
2. Choisir parmi :
   - **📊 Répartition par Genre**
   - **🏆 Top 10 Auteurs**
   - **📈 Courbe d'Activité**
3. Graphiques interactifs générés avec matplotlib

---

## 🔒 Gestion des Erreurs

### Exceptions Personnalisées
- `MembreInexistantError` : Membre non trouvé dans le système
- `LivreInexistantError` : Livre non présent dans le catalogue
- `LivreIndisponibleError` : Stock épuisé (tous les exemplaires empruntés)
- `QuotaEmpruntDepasseError` : Limite d'emprunts atteinte (4 max)

### Messages Utilisateur
- ✅ **Succès** : Confirmations claires avec icônes
- ⚠️ **Avertissements** : Informations importantes
- ❌ **Erreurs** : Messages détaillés et solutions

---

## 💾 Sauvegarde des Données

### Format TXT (livres.txt)
```
ISBN;Titre;Auteur;Année;Genre;Statut;Stock
```

### Format TXT (membres.txt)
```
ID;Nom;Livres_Empruntés
```

### Format CSV (historique.csv)
```csv
date;isbn;id_membre;action
2025-01-03;978-xxx;M001;emprunt
2025-01-05;978-xxx;M001;retour
```

---

## 🎨 Personnalisation

### Changer la Limite d'Emprunts
Dans `Bibliotheque.py` :
```python
max_emprunts = 4  # Modifier selon vos besoins
```

---

## 🐛 Résolution de Problèmes

### Erreur : FileNotFoundError
**Solution** : Le dossier `data/` est créé automatiquement au lancement.

### Erreur : Module PyQt5 non trouvé
**Solution** :
```bash
pip install PyQt5
```

### Problème d'affichage des graphiques
**Solution** :
```bash
pip install --upgrade matplotlib
```

---

## 🚀 Améliorations Futures

- [ ] 🔍 Recherche avancée avec filtres
- [ ] 📧 Notifications par email pour retards
- [ ] 🔐 Système d'authentification
- [ ] 📱 Version mobile (PyQt for Android)
- [ ] 🌐 API REST pour intégration web
- [ ] 🗄️ Migration vers base de données SQL
- [ ] 📊 Dashboard avec statistiques en temps réel
- [ ] 🎨 Thèmes personnalisables (clair/sombre)

---
