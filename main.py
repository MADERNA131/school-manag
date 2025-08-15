import os

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.filechooser import FileChooserIconView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
# from kivy.lang.builder import load_all_kv_files
from kivymd.uix.screenmanager import MDScreenManager
#from kivymd.uix.snackbar import Snackbar
# from kivy.uix.image import AsyncImage
from plyer import filechooser

import screens

#Window.size=(360, 640)

"""reglement d'oerdre interieur et pourquoi choisir notre universite"""

def change_password():
    print("Changement de mot de passe")

def manage_notifications():
    print("Gestion des notifications")

def download_certificate():
    print("Téléchargement du certificat")


#def quitter_app():
    #if platform in ("win", "linux", "macosx"):
       # Window.close()
    #else:
        #sys.exit()


class MonApp(MDApp):
    classe_etudiant = ""# Pour stocker la classe après login
    #afficher_paiements = ""
    def on_start(self):
        width = Window.width
        height = Window.height
        print(f"Taille écran détectée : {width} x {height}")
        """        if width <= 480:
            Snackbar(text="Bienvenue.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
          #  print("Mobile view")
        elif width <= 800:
            Snackbar(text="Bienvenue.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
          #  print("Tablette")
        else:
            Snackbar(text="Bienvenue.", bg_color=(0, 0.5, 0.8, 1), duration=2,
                     snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, ).open()
           # print("Desktop")
"""
    def __init__(self):
        super().__init__()
        self.dialog = None
        self.menu = None
        self.file_dialog = None

    def build(self):
        kv_path = os.path.join(os.path.dirname(__file__), "screens")
        self.load_all_kv_files(kv_path)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.material_style = "M3"
        sm = MDScreenManager()
        sm.add_widget(screens.SplashScreen(name='splash'))
        sm.add_widget(screens.HomeScreen(name='home'))
        #sm.add_widget(screens.NouveauScreen(name='nouv_etud'))
        sm.add_widget(screens.LoginScreen(name='etud_login'))
        sm.add_widget(screens.EtudScreen(name='etud_dashboard'))
        #sm.add_widget(screens.CoursScreen(name="etud_cours"))
        sm.add_widget(screens.ComptesScreen(name="compte"))
        #sm.add_widget(screens.SuggestionScreen(name="suggestion"))
        #sm.add_widget(screens.BordereauScreen(name="paiement"))
        #sm.add_widget(screens.AbsenceScreen(name="absence"))
        #sm.add_widget(screens.EtuEmplScreen(name="etud_emploi"))
        #sm.add_widget(screens.EtudNoteScreen(name="etud_note"))
        #sm.add_widget(screens.EtudCalendScreen(name="etud_calendrier"))
        #sm.add_widget(screens.EtudAnnonceScreen(name="etud_annonce"))
        #sm.add_widget(screens.EtudBibliothequeScreen(name="etud_bibliotheque"))
        #sm.add_widget(screens.EtudSupportScreen(name="etud_support"))
        #sm.add_widget(screens.EtudCamScreen(name="mes_enseignats"))
        #sm.add_widget(screens.EtudReglementScreen(name="reglements"))
        #sm.add_widget(screens.EnsDashScreen(name="ens_dash"))
        #sm.add_widget(screens.ProfDashScreen(name="prof_dashboard"))
        #sm.add_widget(screens.ProfCoursScreen(name="ens_cours"))
        #sm.add_widget(screens.ProfNoteScreen(name="ens_notes"))
        #sm.add_widget(screens.ProfAnnonceScreen(name="ens_annonces"))
        #sm.add_widget(screens.ProfEmploiScreen(name="ens_emploi"))
        #sm.add_widget(screens.ProfCompteScreen(name="ens_compte"))
        #sm.add_widget(screens.ProfEtudAbsenScreen(name="ens_absences"))
        #sm.add_widget(screens.AjouterNoteScreen(name="ajouter_note"))
        # sm.add_widget(screens.AdminDashboardScreen(name="admin_dash"))
        # sm.add_widget(screens.AdminEmploiScreen(name="admin_emploi"))
        # sm.add_widget(screens.AjoutPaiemScreen(name="ajout_paiement"))
        # sm.add_widget(screens.GererUtilScreen(name="gestion_utilisateur"))
        # sm.add_widget(screens.AjouterScreen(name="ajouter_utilisateur"))
        return sm
    #Dots-vertical(menu) pour ouvrir d'autres screen
    def open_menu(self, button):
        menu_items = [
            {
                "text": "Comptes",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Comptes": self.open_compte(),
                "icon": "account",
            },
            {
                "text": "Suggestion",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Suggestion": self.open_suggestion(),
            },
            {
                "text": "Centre d'aide",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Centre d'aide": self.show_help_dialog(),
            },
            {
                "text": "A propos ",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="A propos": self.show_info(),
            },
        ]
        self.menu = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=3,
            max_height=dp(180)
        )
        self.menu.open()
    #bouton retour de nouveau etudiants screen pour home
    def back_button3(self):
        self.root.current="home"
    #ouvrir compte screen sur DropDownMenu
    def open_compte(self):
        self.root.current="compte"
    #ouvrir suggestion screen sur DropDownMenu
    def open_suggestion(self):
        self.root.current="suggestion"
    #comptes bouton retour
    def retour(self):
        self.root.current = "etud_dashboard"
    #signaler absence bouton retour
    def back_button(self):
        self.root.current = "etud_dashboard"
        #emploi du temp admin return button
    def back_button1(self):
        self.root.current = "etud_dashboard"
        # emploi du temp etudiant return button
    def back_button2(self):
        self.root.current = "etud_dashboard"
        #note etudiant return button
    def back_button4(self):
        self.root.current = "etud_dashboard"
        #annonce generale return button
    def back_button5(self):
        self.root.current = "etud_dashboard"
        #mes support return button
    def back_button6(self):
        self.root.current = "etud_dashboard"
        #exercice & tp return button
    def back_button7(self):
        self.root.current = "etud_dashboard"
        #forum etudiants box return button
    def back_button8(self):
        self.root.current = "etud_dashboard"
        #mes camarades return button
    def back_button13(self):
        self.root.current = "etud_dashboard"
    #admin dash return button
    def back_button9(self):
        self.root.current = "etud_login"
    #historique back button
    def back_button10(self):
        self.root.current = "etud_dashboard"
        #ajouter utilisateur return button
    def back_button12(self):
        self.root.current = "gestion_utilisateur"
    # absence signalee return button
    def back_button_ens(self):
        self.root.current = "prof_dashboard"
    #compte screen back button
    def back_button_enscom(self):
        self.root.current = "prof_dashboard"
        # emploi du temps enseignant return screen
    def back_button_ensemp(self):
        self.root.current = "prof_dashboard"
    def back_button_enscours(self):
        self.root.current = "prof_dashboard"
        #ens gerer notre return button
    def back_button_ensgrnt(self):
        self.root.current = "prof_dashboard"
    def back_button_ntrt(self):
        self.root.current = "ens_notes"
    #dialog pour signaler si vous voulez vous deconnecte
    def logout_confirmation(self):
        self.dialog = MDDialog(
            title="Déconnexion",
            text="Voulez-vous vraiment vous déconnecter ?",
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    theme_text_color="Primary",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="DÉCONNEXION",
                    theme_text_color="Error",
                    on_release=lambda x: self.logout()
                ),
            ],
        )
        self.dialog.open()
#se deconnecte
    def logout(self):
        self.dialog.dismiss()
        print("Utilisateur déconnecté")
# besoin d'aide
    def show_help_dialog(self):
        if self.menu:
            self.menu.dismiss()

        dialog = MDDialog(
            title="Aide",
            text="Ceci est la section d'aide.\n\nPour toute question, contactez-nous à support@example.com.\n\nou appel-nous sur +243993422064",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss(),
                ),
            ],
        )
        dialog.open()
#version & a propos de l'app
    def show_info(self):
        pass
    #attach_file1 pour attache preuve du bordereau
    def attach_file(self):
        content = MDBoxLayout(orientation='vertical')
        result = FileChooserIconView(filters=['*.pdf', '*.jpg'])
        content.add_widget(result)

        self.file_dialog = MDDialog(
            title="Sélectionnez le bordereau",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="Annuler"),
                MDFlatButton(text="Valider", on_release=lambda x: self.kv_file(result.path))
            ]
        )
        self.file_dialog.open()

    def open_politique(self):
        pass
    def edit_profile(self):
        filechooser.open_file(on_selection=self.selected)
    def selected(self, selection):
        if selection:
            photo_path = selection[0]
            # Ici tu peux uploader sur cloud et sauvegarder URL dans la DB
            self.root.ids.profile_image.source = photo_path  # Affiche localement

#quitter app cote prof dashboard
    def quitter_app(self):
        def fermer_dialogue(_):
            self.dialog.dismiss()

        def quitter(_):
            self.stop()

        self.dialog = MDDialog(
            title="Quitter l'application",
            text="Êtes-vous sûr de vouloir quitter ?",
            buttons=[
                MDFlatButton(text="Annuler", on_release=fermer_dialogue),
                MDFlatButton(text="Quitter", on_release=quitter),
            ]
        )
        self.dialog.open()


MonApp().run()