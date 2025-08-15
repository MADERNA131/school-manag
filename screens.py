import sqlite3
# from kivy.app import App
from kivy.clock import Clock
#from kivy.core.window import Window
from kivy.metrics import dp
#from kivy.uix.label import Label
from kivymd.app import MDApp
#from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
#from kivymd.uix.textfield import MDTextField


#page d'accueil1
class SplashScreen(MDScreen):
    def on_enter(self, *args):
        Clock.schedule_once(self.switch_to_main, 8)
    def switch_to_main(self, _):
        self.manager.current = "home"

#page d'accueil2
class HomeScreen(MDScreen):
    pass

#login pour etudient
class LoginScreen(MDScreen):
    def try_login(self, matricule, password):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT role, classe, nom FROM utilisateurs WHERE matricule=? AND mot_de_passe=?", (matricule, password))
        result = c.fetchone()
        conn.close()

        if result:
            role, classe, nom = result  #[0]
            app = MDApp.get_running_app()
            app.role = role
            app.nom = nom
            app.classe_etudiant = classe  if role == "etudiant" else None # <-- sauvegarde ici
            app.matricule_connecte = matricule  # <--- Ajoute ceci
            #self.manager.current = "etud_dashboard"
            if role == "etudiant":
                self.manager.current = "etud_dashboard"
            elif role == "enseignant":
                self.manager.current = "prof_dashboard"
            #Snackbar(text="Connexion reussi.")
            elif role == "admin":
                self.manager.current = "admin_dash"
            #Snackbar(text="Connexion reussi.")
        else:
            Snackbar(text="Matricule ou mot de passe incorrect.", bg_color=(0, 0.5, 0.8, 1), duration=2,snackbar_x="10dp",snackbar_y="10dp",size_hint_x=0.9,).open()
        # Vider les champs après tentative de connexion
        self.ids.matricule.text = ""
        self.ids.password.text = ""
        #mot de passe oublier button
    @staticmethod
    def forget_password():
        Snackbar(text="Cette fonctionalite n'est pas disponible.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                 snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()

class NouveauScreen(MDScreen):
    def envoyer_demander(self):
        nom = self.ids.nom.text
        prenom = self.ids.prenom.text
        sexe = self.ids.sexe.text
        date = self.ids.date.text
        nationalite = self.ids.nationalite.text
        adresse = self.ids.adresse.text
        annee = self.ids.annee.text
        choix = self.ids.choix.text
        commentaire = self.ids.commentaire.text

        if all([nom, prenom, sexe, date, nationalite, adresse, annee, choix, commentaire]):
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO nouv_etudiants (nom, prenom, sexe, date, nationalite, adresse, annee, choix, commentaire) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (nom, prenom, sexe, date, nationalite, adresse, annee, choix, commentaire))
            conn.commit()
            conn.close()
            #self.dialog_success("Absence envoyée avec succès.")
            Snackbar(text="Votre demande a ete envoyee avec succes.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
        else:
            #self.dialog_error("Veuillez remplir tous les champs.")
            Snackbar(text="Veullez remplir tous les champs.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
        self.ids.nom.text = ""
        self.ids.prenom.text = ""
        self.ids.sexe.text = ""
        self.ids.date.text = ""
        self.ids.nationalite.text = ""
        self.ids.adresse.text = ""
        self.ids.annee.text = ""
        self.ids.choix.text = ""
        self.ids.commentaire.text = ""


class EtudScreen(MDScreen):
    pass

class CoursScreen(MDScreen):
    def on_enter(self):
        self.afficher_mes_cours()
    def afficher_mes_cours(self):
        app = MDApp.get_running_app()
        classe = app.classe_etudiant
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT nom, professeur, heure FROM cours WHERE classe=?", (classe,))
        cours = c.fetchall()
        conn.close()

        box = self.ids.mes_cours_box
        box.clear_widgets()

        if not cours:
            #box.add_widget(MDLabel(text="Aucun cours trouvé.", halign="center"))
            Snackbar(text="Aucune cours trouve.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
            return

        for nom, prof, heure in cours:
            card = MDCard(
                orientation="vertical",
                size_hint_y=None,
                height="100dp",
                padding="10dp",
                radius=[10],
                elevation=3,
                md_bg_color=(0.95, 0.95, 1, 1)
            )
            card.add_widget(MDLabel(text=f"Cours : {nom}", halign="center"))
            card.add_widget(MDLabel(text=f"Professeur : {prof}", halign="center"))
            card.add_widget(MDLabel(text=f"Heure : {heure}", halign="center"))
            box.add_widget(card)

class ComptesScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        matricule = app.matricule_connecte

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT nom, faculte, email, matricule, telephone, classe, date_naissance FROM utilisateurs WHERE matricule=?", (matricule,))
        result = c.fetchone()
        conn.close()

        if result:
            self.ids.nom.text = f"{result[0]}"
            self.ids.faculte.text = f"{result[1]}"
            self.ids.email.text = f"{result[2]}"
            self.ids.matricule.text = f"{result[3]}"
            self.ids.telephone.text = f"{result[4]}"
            self.ids.classe.text = f"{result[5]}"
            self.ids.date.text = f"{result[6]}"


class SuggestionScreen(MDScreen):
    pass

class BordereauScreen(MDScreen):
    def on_enter(self):
        self.afficher_paiements()

    def afficher_paiements(self):
        self.ids.historique_box.clear_widgets()
        app = MDApp.get_running_app()
        matricule = app.matricule_connecte  # doit être défini après login

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT matricule, montant, devise, methode, reference, date FROM paiements WHERE matricule=?", (matricule,))
        rows = c.fetchall()
        #conn.close()

        for paiement in rows:
            matricule, montant, devise, methode, reference, date = paiement
            card = MDCard(
                orientation="vertical",
                padding="10dp",
                size_hint_y=None,
                height="150dp",
                md_bg_color=app.theme_cls.primary_color,
            )
            card.add_widget(MDLabel(text=f"Matricule : {matricule}", halign="center"))
            card.add_widget(MDLabel(text=f"Montant : {montant} {devise}", halign="center"))
            card.add_widget(MDLabel(text=f"Méthode : {methode}", halign="center"))
            card.add_widget(MDLabel(text=f"Réf : {reference}", halign="center"))
            card.add_widget(MDLabel(text=f"Date : {date}", halign="center"))
            self.ids.historique_box.add_widget(card)

        # Afficher total en FC
        c.execute("SELECT SUM(montant) FROM paiements WHERE matricule=? AND devise='fc'", (matricule,))
        total_fc = c.fetchone()[0] or 0
        #total en USD
        c.execute("SELECT SUM(montant) FROM paiements WHERE matricule=? AND devise='usd'", (matricule,))
        total_usd = c.fetchone()[0] or 0

        total_card = MDCard(
            orientation="vertical",
            padding="12dp",
            size_hint_y=None,
            height="100dp",
            md_bg_color=app.theme_cls.primary_light
        )
        total_card.add_widget(MDLabel(
            text=f"Total en FC : {total_fc} FC",
            halign="center",
            font_style="Subtitle1"
        ))
        total_card.add_widget(MDLabel(
            text=f"Total en USD : {total_usd} USD",
            halign="center",
            font_style="Subtitle1"
        ))

        self.ids.historique_box.add_widget(total_card)
        if not rows:
            self.ids.historique_box.add_widget(
                MDLabel(
                    text="Aucun historique de paiement trouvé.",
                    halign="center",
                    theme_text_color="Hint",
                    font_style="Subtitle1"
                )
            )

        conn.close()

class AbsenceScreen(MDScreen):
    def envoyer_absence(self):
        app = MDApp.get_running_app()
        nom = self.ids.nom_field.text
        cours = self.ids.cours_field.text
        professeur = self.ids.professeur_field.text
        date = self.ids.date_field.text
        heure = self.ids.heure_field.text
        motif = self.ids.motif_field.text
        classe = self.ids.classe_field.text
        matricule = app.matricule_connecte  # récupéré du login

        if all([nom, cours, professeur, date, heure, motif]):
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO absence (matricule, nom, classe, cours, professeur, date, heure, motif) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (matricule, nom, classe, cours, professeur, date, heure, motif))
            conn.commit()
            conn.close()
            #self.dialog_success("Absence envoyée avec succès.")
            Snackbar(text="Absence envoyee avec succes.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
        else:
            #self.dialog_error("Veuillez remplir tous les champs.")
            Snackbar(text="Veullez remplir tous les champs.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
        self.ids.nom_field.text = ""
        self.ids.cours_field.text = ""
        self.ids.professeur_field.text = ""
        self.ids.date_field.text = ""
        self.ids.heure_field.text = ""
        self.ids.motif_field.text = ""
        self.ids.classe_field.text = ""


class EtuEmplScreen(MDScreen):
    def on_enter(self):
        self.afficher_emploi()
    def afficher_emploi(self):
        app = MDApp.get_running_app()
        classe = app.classe_etudiant
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        # Récupérer l'emploi du temps pour cette classe
        c.execute("SELECT jour, heure, cours, salle, professeur FROM emploi_temp WHERE classe=?",
                  (classe,))
        resultats = c.fetchall()
        conn.close()

        box = self.ids.emploi_box
        box.clear_widgets()

        if not resultats:
            #box.add_widget(MDLabel(text="Aucun emploi du temps disponible.", halign="center"))
            Snackbar(text="Aucune emploi du temps disponible.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
            return
        couleurs_jour = {
            "Lundi": (0.9, 0.9, 1, 1),
            "Mardi": (0.9, 1, 0.9, 1),
            "Mercredi": (1, 0.95, 0.8, 1),
            "Jeudi": (1, 0.85, 0.85, 1),
            "Vendredi": (0.8, 1, 1, 1),
            "Samedi": (0.95, 0.9, 1, 1),
            "Dimanche": (1, 1, 1, 1)
        }

        for jour, heure, cours, salle, professeur in resultats:
            couleur = couleurs_jour.get(jour)  # couleur par défaut = blanc
            card = MDCard(size_hint_y=None, height="150dp", padding="10dp", orientation="vertical", radius=[10],
                          elevation=4, md_bg_color=couleur)
            card.add_widget(MDLabel(text=f"[b]{jour}[/b]", markup=True, halign="center"))
            card.add_widget(MDLabel(text=f"Cours: {cours}", halign="center"))
            card.add_widget(MDLabel(text=f"Heure: {heure}", halign="center"))
            card.add_widget(MDLabel(text=f"Salle: {salle}", halign="center"))
            card.add_widget(MDLabel(text=f"Prof: {professeur}", halign="center"))
            box.add_widget(card)

"""    def on_enter(self):
        self.afficher_emploi()

    def afficher_emploi(self):
        app = MDApp.get_running_app()
        classe = app.classe_etudiant
        emploi_box = self.ids.emploi_box
        emploi_box.clear_widgets()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT jour, cours FROM emploi_du_temps WHERE classe = ?", (classe,))
            emplois = cursor.fetchall()
        except sqlite3.Error as e:
            emplois = []
            print("Erreur SQLite:", e)

        conn.close()

        if emplois:
            for jour, cours in emplois:
                card = MDCard(size_hint=(.9, None), height="100dp", orientation="vertical", padding=10)
                card.add_widget(MDLabel(text=f"{jour} : {cours}", halign="center",font_style="H5"))
                emploi_box.add_widget(card)
        else:
            card = MDCard(size_hint=(.9, None), height="100dp", orientation="vertical", padding=10)
            card.add_widget(MDLabel(text="Aucun emploi du temps trouvé.", halign="center"))
            emploi_box.add_widget(card)

"""
class AdminEmploiScreen(MDScreen):
    def ajouter_cours(self, jour, heure, matiere, classe):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO emploi_du_temps (jour, heure, matiere, classe) VALUES (?, ?, ?, ?)",
                  (jour, heure, matiere, classe))
        conn.commit()
        conn.close()
        Snackbar(text="Cours ajouté avec succès !").open()
        self.ids.jour.text = ""
        self.ids.heure.text = ""
        self.ids.matiere.text = ""
        self.ids.classe.text = ""

class EtudNoteScreen(MDScreen):
    def on_enter(self):
        self.note_box()

    def note_box(self):
        app = MDApp.get_running_app()
        matricule = app.matricule_connecte
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT cours, note, semestre, annee, commentaire FROM notes WHERE matricule=?", (matricule,))
        resultats = c.fetchall()
        #conn.close()

        box = self.ids.note_box
        box.clear_widgets()

        if resultats:
            for cours, note, semestre, annee, commentaire in resultats:
                card = MDCard(orientation="vertical", padding=10, size_hint_y=None, height="120dp", md_bg_color=(0.95, 0.95, 1, 1), elevation=4)
                card.add_widget(MDLabel(text=f"Cours : {cours}", halign="center", bold=True))
                card.add_widget(MDLabel(text=f"Note : {note}", halign="center", bold=True))
                card.add_widget(MDLabel(text=f"Semestre : {semestre} | Année : {annee}", halign="center", bold=True))
                card.add_widget(MDLabel(text=f"Commentaire : {commentaire}", halign="center", bold=True))
                box.add_widget(card)
        else:
            Snackbar(text="Aucune note disponible.", bg_color=(0, 0.5, 0.8, 1), duration=1,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()

            # Afficher total en FC
        c.execute("SELECT SUM(note) FROM notes WHERE matricule=?", (matricule,))
        total = c.fetchone()[0] or 0

        total_card = MDCard(
            orientation="vertical",
            padding="12dp",
            size_hint_y=None,
            height="80dp",
            md_bg_color=app.theme_cls.primary_light
        )
        total_card.add_widget(MDLabel(
            text=f"Total : {total} points",
            halign="center",
            font_style="Subtitle1"
        ))
        self.ids.note_box.add_widget(total_card)
        conn.close()

            #box.add_widget(MDLabel(text="Aucune note disponible.", halign="center"))

class EtudCalendScreen(MDScreen):
    def on_enter(self):
        self.calendrier_box()
    def calendrier_box(self):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT titre, description FROM calendrier ")
        resultats = c.fetchall()
        conn.close()

        box = self.ids.calendrier_box
        box.clear_widgets()

        if not resultats:
            #box.add_widget(MDLabel(text="Aucun événement à venir.", halign="center"))
            Snackbar(text="Aucune evenement a venir.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
            return

        for titre, description in resultats:
            card = MDCard(orientation="vertical", padding=10, size_hint_y=None, height="100dp", md_bg_color=(1, 0.85, 0.85, 1))
            card.add_widget(MDLabel(text=f"{titre}", bold=True, halign="center"))
            #card.add_widget(MDLabel(text=f"Date: {date}", halign="left"))
            card.add_widget(MDLabel(text=f"{description}", halign="center"))
            box.add_widget(card)


class EtudAnnonceScreen(MDScreen):
    def on_enter(self):
        self.annonce_box()

    def annonce_box(self):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT titre, first, second, third, date FROM communiques ORDER BY id DESC")
        resultats = c.fetchall()
        conn.close()

        box = self.ids.annonce_box
        box.clear_widgets()

        if not resultats:
            box.add_widget(MDLabel(
                text="Aucune annonce disponible.",
                halign="center",
                theme_text_color="Hint"
            ))
            return

        for titre, first, second, third, date in resultats:
            card = MDCard(
                orientation="vertical",
                padding="10dp",
                spacing="10dp",
                size_hint_y=None,
                height="300dp",
                md_bg_color=(0.3, 0.6, 1, 1),
            )
            card.add_widget(MDLabel(text=f"{titre}", halign="center", bold=True))
            card.add_widget(MDLabel(text=f"{first or ''}", halign="left"))
            card.add_widget(MDLabel(text=f"{second or ''}", halign="left"))
            card.add_widget(MDLabel(text=f"{third or ''}", halign="left"))
            card.add_widget(MDLabel(text=f"Publier le {date}", halign="right"))
            self.ids.annonce_box.add_widget(card)


class EtudBibliothequeScreen(MDScreen):
    pass

class EtudSupportScreen(MDScreen):
    pass

class EtudCamScreen(MDScreen):
    def on_pre_enter(self):
        self.camarades_box()

    def camarades_box(self):
        app = MDApp.get_running_app()
        classe = app.classe_etudiant  # Stocké après login
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT nom, matricule, telephone, email FROM utilisateurs WHERE classe=? AND role='etudiant'", (classe,))
        camarades = c.fetchall()
        conn.close()

        box = self.ids.camarades_box
        box.clear_widgets()

        if not camarades:
            #box.add_widget(MDLabel(text="Aucun camarade trouvé.", halign="center"))
            Snackbar(text="Aucun camarade trouve.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
            return

        for nom, matricule, telephone, email in camarades:
            card = MDCard(orientation="vertical", padding=10, size_hint_y=None, height="100dp",
                          md_bg_color=(0.9, 1, 0.9, 1))
            card.add_widget(MDLabel(text=f"Nom: {nom}", halign="center", bold=True))
            card.add_widget(MDLabel(text=f"Matricule: {matricule}", halign="center",bold=True ))
            card.add_widget(MDLabel(text=f"Telephone: {telephone}", halign="center", bold=True))
            card.add_widget(MDLabel(text=f"Email: {email}", halign="center", bold=True ))
            box.add_widget(card)


class EtudReglementScreen(MDScreen):
    pass

class EnsDashScreen(MDScreen):
    pass

class ProfDashScreen(MDScreen):
    pass

class ProfEtudAbsenScreen(MDScreen):
    #professeur_nom = "Dr. Kouadio"  # À remplacer dynamiquement selon l'utilisateur connecté
    def on_enter(self):
        self.afficher_absences()

    def afficher_absences(self):
        app = MDApp.get_running_app()
        nom = app.nom  # Stocké après login
        self.ids.absence_box.clear_widgets()
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT id, matricule, nom, classe, cours, date, motif FROM absence WHERE professeur = ?",
                  (nom,))
        absences = c.fetchall()
        conn.close()

        if not absences:
            #self.ids.absence_box.add_widget(MDLabel(text="Aucune absence signalée", halign="center"))
            Snackbar(text="Aucune absence signalée.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
            return

        for id_, matricule, nom, classe, cours, date, motif in absences:
            card = MDCard(orientation="vertical", padding=10, size_hint_y=None, height=dp(190),
                          md_bg_color=(0.95, 0.95, 1, 1))
            card.add_widget(MDLabel(text=f"Nom: {nom}", halign="left"))
            card.add_widget(MDLabel(text=f"Matricule: {matricule}", halign="left"))
            card.add_widget(MDLabel(text=f"Classe: {classe}", halign="left"))
            card.add_widget(MDLabel(text=f"Cours: {cours}", halign="left"))
            card.add_widget(MDLabel(text=f"Date: {date}", halign="left"))
            card.add_widget(MDLabel(text=f"Justification: {motif}", halign="left"))
            btn = MDRaisedButton(
                text="Supprimer",
                md_bg_color=(1, 0, 0, 1),
                on_release=lambda x, abs_id=id_: self.supprimer_absence(abs_id)
            )
            card.add_widget(btn)
            self.ids.absence_box.add_widget(card)

    def supprimer_absence(self, absence_id):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("DELETE FROM absence WHERE id=?", (absence_id,))
        conn.commit()
        conn.close()
        self.afficher_absences()

class ProfCoursScreen(MDScreen):
    def on_enter(self):
        self.afficher_mes_cours()
    def afficher_mes_cours(self):
        app = MDApp.get_running_app()
        nom = app.nom
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT cours, classe, heure FROM ens_cours WHERE nom=?", (nom,))
        cours = c.fetchall()
        conn.close()

        box = self.ids.mes_cours_box
        box.clear_widgets()

        if not cours:
            #box.add_widget(MDLabel(text="Aucun cours trouvé.", halign="center"))
            Snackbar(text="Aucune cours trouve.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
            return

        for cours, classe, heure in cours:
            card = MDCard(
                orientation="vertical",
                size_hint_y=None,
                height="100dp",
                padding="10dp",
                radius=[10],
                elevation=3,
                md_bg_color=(0.95, 0.95, 1, 1)
            )
            card.add_widget(MDLabel(text=f"Cours : {cours}", halign="center"))
            card.add_widget(MDLabel(text=f"Classe : {classe}", halign="center"))
            card.add_widget(MDLabel(text=f"Heure : {heure}", halign="center"))
            box.add_widget(card)


class ProfNoteScreen(MDScreen):
    def on_enter(self):
        self.rechercher_etudiants("")

    def rechercher_etudiants(self, query):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT id, nom, matricule, classe, faculte, cours, note, semestre, annee, commentaire FROM notes WHERE nom LIKE ? OR matricule LIKE ? OR classe LIKE ? ORDER BY id DESC",
            (f"%{query}%", f"%{query}%",f"%{query}%"))
        etudiants = c.fetchall()
        conn.close()

        box = self.ids.etudiants_box
        box.clear_widgets()

        for note_id, nom, matricule, classe, faculte, cours, note, semestre, annee, commentaire in etudiants:
            card = MDCard(orientation="vertical", padding=10, spacing=10, size_hint_y=None, height=dp(180),
                          md_bg_color=(0.3, 0.6, 1, 1))
            card.add_widget(MDLabel(text=f"Nom: {nom}", halign="center"))
            card.add_widget(MDLabel(text=f"Matricule: {matricule}", halign="center"))
            card.add_widget(MDLabel(text=f"Classe: {classe}", halign="center"))
            card.add_widget(MDLabel(text=f"Faculté: {faculte}", halign="center"))
            card.add_widget(MDLabel(text=f"Cours: {cours}", halign="center"))
            card.add_widget(MDLabel(text=f"Note: {note}", halign="center"))
            card.add_widget(MDLabel(text=f"Semestre: {semestre}", halign="center"))
            card.add_widget(MDLabel(text=f"Annee: {annee}", halign="center"))
            card.add_widget(MDLabel(text=f"Commentaire: {commentaire}", halign="center"))
            btn = MDRaisedButton(text="Supprimer", md_bg_color=(1, 0, 0, 1),
                                 on_release=lambda x, nid=note_id: self.supprimer_note(nid))
            card.add_widget(btn)
            box.add_widget(card)

    def supprimer_note(self, note_id):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("DELETE FROM notes WHERE id=?", (note_id,))
        conn.commit()
        conn.close()
        self.rechercher_etudiants("")

class AjouterNoteScreen(MDScreen):
    def ajouter_note(self):
        nom = self.ids.nom.text.strip()
        matricule = self.ids.matricule.text.strip()
        classe = self.ids.classe.text.strip()
        faculte = self.ids.faculte.text.strip()
        cours = self.ids.cours.text.strip()
        note = self.ids.note.text.strip()
        commentaire = self.ids.commentaire.text.strip()
        semestre = self.ids.semestre.text.strip()
        annee = self.ids.annee.text.strip()

        #if not nom or not matricule or not  or not classe or not faculte or not role:
            #Snackbar(text="Nom, matricule et mot de passe sont obligatoires.").open()
            #return
        if all([nom, matricule, classe, faculte, cours, note, semestre, annee, commentaire]):
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("""
                INSERT INTO notes (nom, matricule, classe, faculte, cours, note, semestre, annee, commentaire)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (nom, matricule, classe, faculte, cours, note, semestre, annee, commentaire))
            conn.commit()
            conn.close()
            Snackbar(text="Note ajouté avec succès !").open()
        else:
            Snackbar(text="tous les champs sont obligatoires !").open()
        #self.dialogue.dismiss()
        #self.afficher_utilisateurs()  # Recharge la liste si besoin
        self.ids.nom.text=""
        self.ids.matricule.text=""
        self.ids.classe.text=""
        self.ids.cours.text=""
        self.ids.faculte.text=""
        self.ids.note.text=""
        self.ids.commentaire.text=""
        self.ids.semestre.text=""
        self.ids.annee.text=""

class ProfAnnonceScreen(MDScreen):
    pass

class ProfEmploiScreen(MDScreen):
    def on_enter(self):
        self.afficher_emploi()
    def afficher_emploi(self):
        app = MDApp.get_running_app()
        nom = app.nom
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        # Récupérer l'emploi du temps pour cette classe
        c.execute("SELECT jour, heure, cours, salle, classe FROM emploi_ens WHERE nom=?",
                  (nom,))
        resultats = c.fetchall()
        conn.close()

        box = self.ids.emploi_box
        box.clear_widgets()

        if not resultats:
            #box.add_widget(MDLabel(text="Aucun emploi du temps disponible.", halign="center"))
            Snackbar(text="Aucune emploi du temps disponible.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
            return
        couleurs_jour = {
            "Lundi": (0.9, 0.9, 1, 1),
            "Mardi": (0.9, 1, 0.9, 1),
            "Mercredi": (1, 0.95, 0.8, 1),
            "Jeudi": (1, 0.85, 0.85, 1),
            "Vendredi": (0.8, 1, 1, 1),
            "Samedi": (0.95, 0.9, 1, 1),
            "Dimanche": (1, 1, 1, 1)
        }

        for jour, heure, cours, salle, classe in resultats:
            couleur = couleurs_jour.get(jour)  # couleur par défaut = blanc
            card = MDCard(size_hint_y=None, height="150dp", padding="10dp", orientation="vertical", radius=[10],
                          elevation=4, md_bg_color=couleur)
            card.add_widget(MDLabel(text=f"[b]{jour}[/b]", markup=True, halign="center"))
            card.add_widget(MDLabel(text=f"Cours: {cours}", halign="center"))
            card.add_widget(MDLabel(text=f"Heure: {heure}", halign="center"))
            card.add_widget(MDLabel(text=f"Salle: {salle}", halign="center"))
            card.add_widget(MDLabel(text=f"Classe: {classe}", halign="center"))
            box.add_widget(card)


class ProfCompteScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        matricule = app.matricule_connecte

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT nom, faculte, email, matricule, telephone FROM utilisateurs WHERE matricule=?", (matricule,))
        result = c.fetchone()
        conn.close()

        if result:
            self.ids.nom.text = f"{result[0]}"
            self.ids.faculte.text = f"{result[1]}"
            self.ids.email.text = f"{result[2]}"
            self.ids.matricule.text = f"{result[3]}"
            self.ids.telephone.text = f"{result[4]}"

class AdminDashboardScreen(MDScreen):
    def on_pre_enter(self):
        self.update_stats()

    def update_stats(self):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM utilisateurs WHERE role='etudiant'")
        nb_etudiants = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM utilisateurs WHERE role='enseignant'")
        nb_enseignants = c.fetchone()[0]

        #c.execute("SELECT COUNT(*) FROM annonces")
        #nb_annonces = c.fetchone()[0]

        conn.close()

        self.ids.nb_etudiants.text = str(nb_etudiants)
        self.ids.nb_enseignants.text = str(nb_enseignants)
        #self.ids.nb_annonces.text = str(nb_annonces)
#    def on_enter(self):
       # self.ids.nb_etud.text = "Étudiants : 250"
 #       self.ids.nb_ens.text = "Enseignants : 35"
     #   self.ids.annonces.text = "- Réunion lundi\n- Résultats disponibles"

class AjoutPaiemScreen(MDScreen):
    def ajouter_paiement(self):
        matricule = self.ids.matricule.text.strip()
        montant = self.ids.montant.text.strip()
        devise = self.ids.devise.text.strip()
        methode = self.ids.methode.text.strip()
        reference = self.ids.reference.text.strip()
        date = self.ids.date.text.strip()

        if not (matricule and montant and devise and methode and reference and date):
            Snackbar(text="Veuillez remplir tous les champs sont obligatoires.").open()
            return

        try:
            montant_val = float(montant)
        except ValueError:
            Snackbar(text="Montant invalide.").open()
            return

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO paiements (matricule, montant, date, methode, reference, devise) VALUES (?, ?, ?, ?, ?, ?)",
                  (matricule, montant_val, date, methode, reference, devise))
        conn.commit()
        conn.close()
        Snackbar(text="Paiement ajouté avec succès.").open()
        self.ids.matricule.text = ""
        self.ids.montant.text = ""
        self.ids.devise.text = ""
        self.ids.methode.text = ""
        self.ids.reference.text = ""
        self.ids.date.text = ""

class GererUtilScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.dialogue_confirm = None

    def _init_(self, **kwargs):
        super().__init__(**kwargs)    #self.dialogue = None
        self.dialogue_confirm = None

    def on_enter(self):
        self.rechercher_utilisateur("")

    def rechercher_utilisateur(self, query):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT nom, matricule, classe, faculte, email, telephone, role FROM utilisateurs WHERE nom LIKE ? OR matricule LIKE ?",
            (f"%{query}%", f"%{query}%"))
        utilisateurs = c.fetchall()
        conn.close()

        box = self.ids.utilisateurs_box
        box.clear_widgets()

        for nom, matricule, classe, faculte, email, telephone, role in utilisateurs:
            card = MDCard(orientation="vertical", padding=10, size_hint_y=None, height=dp(160), md_bg_color=(0.3, 0.6, 1, 1))
            card.add_widget(MDLabel(text=f"Nom: {nom}", halign="left"))
            card.add_widget(MDLabel(text=f"Matricule: {matricule}", halign="left"))
            card.add_widget(MDLabel(text=f"Classe: {classe}", halign="left"))
            card.add_widget(MDLabel(text=f"Faculté: {faculte}", halign="left"))
            card.add_widget(MDLabel(text=f"Email: {email}", halign="left"))
            card.add_widget(MDLabel(text=f"Téléphone: {telephone}", halign="left"))
            card.add_widget(MDLabel(text=f"Role: {role}", halign="left"))
            btn = MDRaisedButton(text="Supprimer", md_bg_color=(1, 0, 0, 1),
                                 on_release=lambda x, m=matricule: self.confirmer_suppression_utilisateur(m))
            card.add_widget(btn)
            box.add_widget(card)

    def confirmer_suppression_utilisateur(self, matricule):
        self.dialogue_confirm = MDDialog(
            title="Confirmation",
            text=f"Supprimer {matricule} ?",
            buttons=[
                MDFlatButton(text="Annuler", on_release=lambda x: self.dialogue_confirm.dismiss()),
                MDRaisedButton(
                    text="Supprimer",
                    md_bg_color=(0.2, 0.2, 0.4, 1),
                    on_release=lambda x: self.supprimer_utilisateur(matricule)
                ),
            ],
        )
        self.dialogue_confirm.open()

    def supprimer_utilisateur(self, matricule):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("DELETE FROM utilisateurs WHERE matricule=?", (matricule,))
        conn.commit()
        conn.close()
        self.dialogue_confirm.dismiss()
        self.rechercher_utilisateur("")


class AjouterScreen(MDScreen):
    def ajouter_utilisateur(self):
        nom = self.ids.nom.text.strip()
        matricule = self.ids.matricule.text.strip()
        mot_de_passe = self.ids.mot_de_passe.text.strip()
        classe = self.ids.classe.text.strip()
        faculte = self.ids.faculte.text.strip()
        email = self.ids.email.text.strip()
        telephone = self.ids.telephone.text.strip()
        role = self.ids.role.text.strip()

        if not nom or not matricule or not mot_de_passe or not classe or not faculte or not role:
            Snackbar(text="Nom, matricule et mot de passe sont obligatoires.").open()
            return

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO utilisateurs (nom, matricule, mot_de_passe, classe, faculte, email, telephone, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, matricule, mot_de_passe, classe, faculte, email, telephone, role))
        conn.commit()
        conn.close()

        Snackbar(text="Utilisateur ajouté avec succès !").open()
        #self.dialogue.dismiss()
        #self.afficher_utilisateurs()  # Recharge la liste si besoin
        self.ids.nom.text=""
        self.ids.montant.text=""
        self.ids.mdp.text=""
        self.ids.classe.text=""
        self.ids.faculte.text=""
        self.ids.email.text=""
        self.ids.matricule.text=""
        self.ids.montant.text=""




