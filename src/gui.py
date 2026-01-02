from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
from Livre import Livre
from Bibliotheque import Bibliotheque
from Membre import Membre
from Exception import MembreInexistantError, LivreInexistantError, LivreIndisponibleError, QuotaEmpruntDepasseError
import Visualisation

# Créer le dossier data s'il n'existe pas
if not os.path.exists("data"):
    os.makedirs("data")

# Créer les fichiers s'ils n'existent pas
if not os.path.exists("data/livres.txt"):
    open("data/livres.txt", "w").close()
if not os.path.exists("data/membres.txt"):
    open("data/membres.txt", "w").close()
if not os.path.exists("data/historique.csv"):
    with open("data/historique.csv", "w") as h:
        h.write("date;isbn;id_membre;action\n")

biblio = Bibliotheque()
try:
    biblio.charger_livres_txt()
except FileNotFoundError:
    pass  # Fichier vide, pas de problème

class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                background: #2d2d44;
                border: 2px solid #3d3d5c;
                border-radius: 10px;
                padding: 12px 15px;
                color: #ffffff;
                font-size: 14px;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border: 2px solid #00d4ff;
                background: #34345a;
            }
            QLineEdit:hover {
                border: 2px solid #4d4d7c;
            }
        """)

class ModernButton(QPushButton):
    def __init__(self, text, icon=None, primary=True):
        super().__init__(text)
        if icon:
            self.setIcon(QIcon.fromTheme(icon))
        
        if primary:
            style = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #00d4ff, stop:1 #0099cc);
                    border: none;
                    border-radius: 12px;
                    padding: 14px 28px;
                    color: #ffffff;
                    font-size: 15px;
                    font-weight: bold;
                    font-family: 'Segoe UI';
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #00e5ff, stop:1 #00aadd);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #00b8d4, stop:1 #007799);
                }
            """
        else:
            style = """
                QPushButton {
                    background: #2d2d44;
                    border: 2px solid #00d4ff;
                    border-radius: 12px;
                    padding: 14px 28px;
                    color: #00d4ff;
                    font-size: 15px;
                    font-weight: bold;
                    font-family: 'Segoe UI';
                }
                QPushButton:hover {
                    background: #34345a;
                    border: 2px solid #00e5ff;
                }
                QPushButton:pressed {
                    background: #1d1d34;
                }
            """
        
        self.setStyleSheet(style)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(50)

class ModernCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: #1e1e2e;
                border-radius: 15px;
                border: 1px solid #2d2d44;
            }
        """)
        self.setGraphicsEffect(self.create_shadow())
    
    def create_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 100))
        return shadow

class BibliothequeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bibliothèque Moderne Pro")
        self.setGeometry(100, 100, 1200, 800)
        
        # Style global
        self.setStyleSheet("""
            QMainWindow {
                background: #0f0f1e;
            }
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabBar::tab {
                background: #1e1e2e;
                color: #888888;
                padding: 15px 30px;
                margin-right: 5px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
            QTabBar::tab:selected {
                background: #2d2d44;
                color: #00d4ff;
            }
            QTabBar::tab:hover {
                background: #25253e;
                color: #00d4ff;
            }
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI';
            }
            QTextEdit {
                background: #1e1e2e;
                border: 2px solid #2d2d44;
                border-radius: 10px;
                padding: 15px;
                color: #ffffff;
                font-size: 13px;
                font-family: 'Consolas';
            }
            QScrollBar:vertical {
                background: #1e1e2e;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #00d4ff;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #00e5ff;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("📚 Système de Gestion de Bibliothèque")
        header.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #ffffff;
            padding: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #1e1e2e, stop:1 #0f0f1e);
            border-radius: 15px;
        """)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        self.create_livres_tab()
        self.create_membres_tab()
        self.create_emprunts_tab()
        self.create_stats_tab()
    
    def create_livres_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Card pour le formulaire
        card = ModernCard()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("➕ Ajouter un Nouveau Livre")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #00d4ff; margin-bottom: 10px;")
        card_layout.addWidget(title)
        
        # Form layout
        form = QGridLayout()
        form.setSpacing(15)
        
        labels = ["📖 ISBN", "📝 Titre", "✍️ Auteur", "📅 Année", "🎭 Genre", "🔢 Quantité"]
        self.livre_entries = []
        
        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold; color: #aaaaaa;")
            entry = ModernLineEdit(f"Entrez {label_text.split()[-1].lower()}")
            
            form.addWidget(label, i, 0, Qt.AlignLeft)
            form.addWidget(entry, i, 1)
            self.livre_entries.append(entry)
        
        card_layout.addLayout(form)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        btn_ajouter = ModernButton("➕ Ajouter le Livre", primary=True)
        btn_ajouter.clicked.connect(self.ajouter_livre)
        
        btn_lister = ModernButton("📋 Afficher Tous les Livres", primary=False)
        btn_lister.clicked.connect(self.afficher_livres)
        
        btn_layout.addWidget(btn_ajouter)
        btn_layout.addWidget(btn_lister)
        card_layout.addLayout(btn_layout)
        
        layout.addWidget(card)
        
        # Zone d'affichage
        display_label = QLabel("📚 Liste des Livres")
        display_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #00d4ff; margin-top: 10px;")
        layout.addWidget(display_label)
        
        self.affichage_livres = QTextEdit()
        self.affichage_livres.setReadOnly(True)
        self.affichage_livres.setMinimumHeight(200)
        layout.addWidget(self.affichage_livres)
        
        self.tabs.addTab(tab, "Livres")
    
    def create_membres_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        card = ModernCard()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("👤 Enregistrer un Nouveau Membre")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #00d4ff; margin-bottom: 10px;")
        card_layout.addWidget(title)
        
        form = QGridLayout()
        form.setSpacing(15)
        
        label_id = QLabel("🆔 ID Membre")
        label_id.setStyleSheet("font-size: 14px; font-weight: bold; color: #aaaaaa;")
        self.entry_id_membre = ModernLineEdit("Entrez l'identifiant unique")
        
        label_nom = QLabel("👤 Nom Complet")
        label_nom.setStyleSheet("font-size: 14px; font-weight: bold; color: #aaaaaa;")
        self.entry_nom_membre = ModernLineEdit("Entrez le nom complet")
        
        form.addWidget(label_id, 0, 0)
        form.addWidget(self.entry_id_membre, 0, 1)
        form.addWidget(label_nom, 1, 0)
        form.addWidget(self.entry_nom_membre, 1, 1)
        
        card_layout.addLayout(form)
        
        btn_ajouter = ModernButton("➕ Enregistrer le Membre", primary=True)
        btn_ajouter.clicked.connect(self.ajouter_membre)
        card_layout.addWidget(btn_ajouter)
        
        layout.addWidget(card)
        layout.addStretch()
        
        self.tabs.addTab(tab, " Membres")
    
    def create_emprunts_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Card Emprunter
        card1 = ModernCard()
        card1_layout = QVBoxLayout(card1)
        card1_layout.setSpacing(15)
        card1_layout.setContentsMargins(30, 30, 30, 30)
        
        title1 = QLabel("📤 Emprunter un Livre")
        title1.setStyleSheet("font-size: 22px; font-weight: bold; color: #00d4ff;")
        card1_layout.addWidget(title1)
        
        form1 = QGridLayout()
        form1.setSpacing(15)
        
        label1 = QLabel("🆔 ID Membre")
        label1.setStyleSheet("font-size: 14px; font-weight: bold; color: #aaaaaa;")
        self.entry_id_emprunt = ModernLineEdit("ID du membre")
        
        label2 = QLabel("📚 Titre du Livre")
        label2.setStyleSheet("font-size: 14px; font-weight: bold; color: #aaaaaa;")
        self.entry_titre_emprunt = ModernLineEdit("Titre du livre à emprunter")
        
        form1.addWidget(label1, 0, 0)
        form1.addWidget(self.entry_id_emprunt, 0, 1)
        form1.addWidget(label2, 1, 0)
        form1.addWidget(self.entry_titre_emprunt, 1, 1)
        
        card1_layout.addLayout(form1)
        
        btn_emprunter = ModernButton("📤 Emprunter", primary=True)
        btn_emprunter.clicked.connect(self.emprunter_livre)
        card1_layout.addWidget(btn_emprunter)
        
        layout.addWidget(card1)
        
        # Card Retourner
        card2 = ModernCard()
        card2_layout = QVBoxLayout(card2)
        card2_layout.setSpacing(15)
        card2_layout.setContentsMargins(30, 30, 30, 30)
        
        title2 = QLabel("📥 Retourner un Livre")
        title2.setStyleSheet("font-size: 22px; font-weight: bold; color: #00d4ff;")
        card2_layout.addWidget(title2)
        
        form2 = QGridLayout()
        form2.setSpacing(15)
        
        label3 = QLabel("🆔 ID Membre")
        label3.setStyleSheet("font-size: 14px; font-weight: bold; color: #aaaaaa;")
        self.entry_id_retour = ModernLineEdit("ID du membre")
        
        label4 = QLabel("📚 Titre du Livre")
        label4.setStyleSheet("font-size: 14px; font-weight: bold; color: #aaaaaa;")
        self.entry_titre_retour = ModernLineEdit("Titre du livre à retourner")
        
        form2.addWidget(label3, 0, 0)
        form2.addWidget(self.entry_id_retour, 0, 1)
        form2.addWidget(label4, 1, 0)
        form2.addWidget(self.entry_titre_retour, 1, 1)
        
        card2_layout.addLayout(form2)
        
        btn_retourner = ModernButton("📥 Retourner", primary=True)
        btn_retourner.clicked.connect(self.rendre_livre)
        card2_layout.addWidget(btn_retourner)
        
        layout.addWidget(card2)
        layout.addStretch()
        
        self.tabs.addTab(tab, "Emprunts")
    
    def create_stats_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(30)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("📊 Statistiques et Analyses")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #ffffff; text-align: center;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Grid de cartes
        grid = QGridLayout()
        grid.setSpacing(25)
        
        stats = [
            ("📊 Répartition par Genre", "Visualisez la distribution des livres par genre", self.stat_genre),
            ("🏆 Top 10 Auteurs", "Découvrez les auteurs les plus présents", self.stat_top),
            ("📈 Courbe d'Activité", "Analysez l'évolution des emprunts", self.stat_activite)
        ]
        
        for i, (titre, desc, func) in enumerate(stats):
            card = ModernCard()
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(15)
            card_layout.setContentsMargins(25, 25, 25, 25)
            
            card_title = QLabel(titre)
            card_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00d4ff;")
            card_layout.addWidget(card_title)
            
            card_desc = QLabel(desc)
            card_desc.setStyleSheet("font-size: 13px; color: #aaaaaa;")
            card_desc.setWordWrap(True)
            card_layout.addWidget(card_desc)
            
            card_layout.addStretch()
            
            btn = ModernButton("Afficher", primary=True)
            btn.clicked.connect(func)
            card_layout.addWidget(btn)
            
            grid.addWidget(card, i // 2, i % 2)
        
        layout.addLayout(grid)
        layout.addStretch()
        
        self.tabs.addTab(tab, "Statistiques")
    
    def afficher_livres(self):
        self.affichage_livres.setText(str(biblio))
    
    def ajouter_livre(self):
        try:
            isbn = self.livre_entries[0].text()
            titre = self.livre_entries[1].text()
            auteur = self.livre_entries[2].text()
            annee = int(self.livre_entries[3].text())
            genre = self.livre_entries[4].text()
            quantite = int(self.livre_entries[5].text())
            
            livre = Livre(isbn, titre, auteur, annee, genre)
            biblio.ajouter_livre(livre, quantite)
            
            for entry in self.livre_entries:
                entry.clear()
            
            self.afficher_livres()
            QMessageBox.information(self, "Succès", "📚 Livre ajouté avec succès !")
        except ValueError:
            QMessageBox.critical(self, "Erreur", "L'année ou la quantité n'est pas un entier valide.")
    
    def ajouter_membre(self):
        id_membre = self.entry_id_membre.text()
        nom = self.entry_nom_membre.text()
        
        if id_membre and nom:
            membre = Membre(id_membre, nom)
            biblio.ajouter_membre(membre)
            
            self.entry_id_membre.clear()
            self.entry_nom_membre.clear()
            
            QMessageBox.information(self, "Succès", "👤 Membre ajouté avec succès !")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
    
    def emprunter_livre(self):
        id_membre = self.entry_id_emprunt.text()
        titre = self.entry_titre_emprunt.text()
        
        self.entry_id_emprunt.clear()
        self.entry_titre_emprunt.clear()
        
        try:
            biblio.emprunter_livre(id_membre, titre)
            self.afficher_livres()
            QMessageBox.information(self, "Succès", f"✅ Livre '{titre}' emprunté avec succès !")
        except (MembreInexistantError, LivreInexistantError, LivreIndisponibleError, QuotaEmpruntDepasseError) as e:
            QMessageBox.critical(self, "Erreur", str(e))
    
    def rendre_livre(self):
        id_membre = self.entry_id_retour.text()
        titre = self.entry_titre_retour.text()
        
        self.entry_id_retour.clear()
        self.entry_titre_retour.clear()
        
        try:
            biblio.retourner_livre(id_membre, titre)
            self.afficher_livres()
            QMessageBox.information(self, "Succès", f"🔄 Livre '{titre}' retourné avec succès !")
        except (MembreInexistantError, LivreInexistantError) as e:
            QMessageBox.critical(self, "Erreur", str(e))
    
    def stat_genre(self):
        Visualisation.diagramme_genre(biblio)
    
    def stat_top(self):
        Visualisation.top_diagramme(biblio)
    
    def stat_activite(self):
        Visualisation.courbe_activite()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = BibliothequeApp()
    window.show()
    sys.exit(app.exec_())