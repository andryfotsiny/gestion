# main.py (version debug)
import tkinter as tk
from tkinter import messagebox
import sys
import os

print("🚀 Démarrage de l'application...")

# Ajouter le chemin du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("📦 Import des modules...")
    from gestion.database.database_manager import DatabaseManager
    print("✅ DatabaseManager importé")

    from gestion.controllers.auth_controller import AuthController
    print("✅ AuthController importé")

    from gestion.views.login_view import LoginView
    print("✅ LoginView importé")

except Exception as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)

class MainApplication:
    def __init__(self):
        print("🔧 Initialisation de l'application...")
        self.root = tk.Tk()
        print("✅ Fenêtre principale créée")

        self.root.withdraw()  # Cacher la fenêtre principale au début
        print("👁️ Fenêtre principale cachée")

        # Initialiser la base de données
        self.init_database()

        # Démarrer avec l'écran de connexion
        self.show_login()

    def init_database(self):
        print("🗄️ Initialisation de la base de données...")
        try:
            db_manager = DatabaseManager()
            db_manager.create_tables()
            db_manager.create_default_admin()
            print("✅ Base de données initialisée avec succès")
        except Exception as e:
            print(f"❌ Erreur base de données: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'initialisation de la base de données: {str(e)}")
            sys.exit(1)

    def show_login(self):
        print("🔐 Affichage de l'écran de connexion...")
        try:
            login_view = LoginView(self.root, self.on_login_success)
            print("✅ Écran de connexion créé")
        except Exception as e:
            print(f"❌ Erreur création login: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la création de l'interface de connexion: {str(e)}")

    def on_login_success(self, user_data):
        print(f"✅ Connexion réussie pour: {user_data['full_name']}")
        try:
            from gestion.views.main_view import MainView

            # Fermer la fenêtre de connexion et afficher l'interface principale
            for widget in self.root.winfo_children():
                widget.destroy()

            self.root.deiconify()  # Réafficher la fenêtre principale
            main_view = MainView(self.root, user_data)
            print("✅ Interface principale chargée")
        except Exception as e:
            print(f"❌ Erreur interface principale: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du chargement de l'interface principale: {str(e)}")

    def run(self):
        print("🎯 Lancement de la boucle principale...")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = MainApplication()
        app.run()
    except Exception as e:
        print(f"💥 Erreur critique: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("Erreur critique", f"Erreur lors du lancement de l'application: {str(e)}")
        sys.exit(1)