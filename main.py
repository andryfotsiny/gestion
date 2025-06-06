# main.py
"""
Point d'entrée principal de l'application de gestion d'inventaire
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Ajouter le chemin du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gestion.database.database_manager import DatabaseManager
from gestion.controllers.auth_controller import AuthController
from gestion.views.login_view import LoginView

class MainApplication:
    def __init__(self):
        """Initialise l'application principale"""
        self.root = tk.Tk()
        self.root.withdraw()  # Cacher la fenêtre principale au début

        # Initialiser la base de données
        self.init_database()

        # Démarrer avec l'écran de connexion
        self.show_login()

    def init_database(self):
        """Initialise la base de données et crée les données par défaut"""
        try:
            db_manager = DatabaseManager()
            db_manager.create_tables()
            db_manager.create_default_admin()
            print("✅ Base de données initialisée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'initialisation de la base de données: {str(e)}")
            sys.exit(1)

    def show_login(self):
        """Affiche l'écran de connexion"""
        login_view = LoginView(self.root, self.on_login_success)

    def on_login_success(self, user_data):
        """Callback appelé après une connexion réussie"""
        from gestion.views.main_view import MainView

        # Fermer la fenêtre de connexion et afficher l'interface principale
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.deiconify()  # Réafficher la fenêtre principale
        main_view = MainView(self.root, user_data)

    def run(self):
        """Lance l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = MainApplication()
        app.run()
    except Exception as e:
        messagebox.showerror("Erreur critique", f"Erreur lors du lancement de l'application: {str(e)}")
        sys.exit(1)