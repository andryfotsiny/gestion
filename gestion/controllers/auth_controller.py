# gestion/controllers/auth_controller.py
# gestion/controllers/auth_controller.py
"""
Contrôleur pour la gestion de l'authentification
"""

from gestion.models.user_model import UserModel
from tkinter import messagebox

class AuthController:
    def __init__(self):
        """Initialise le contrôleur d'authentification"""
        self.user_model = UserModel()
        self.current_user = None

    def login(self, username, password):
        """Tente de connecter un utilisateur"""
        try:
            if not username or not password:
                raise Exception("Veuillez saisir un nom d'utilisateur et un mot de passe")

            user_data = self.user_model.authenticate(username, password)

            if user_data:
                self.current_user = user_data
                return True, user_data
            else:
                return False, "Nom d'utilisateur ou mot de passe incorrect"

        except Exception as e:
            return False, str(e)

    def logout(self):
        """Déconnecte l'utilisateur actuel"""
        self.current_user = None

    def is_authenticated(self):
        """Vérifie si un utilisateur est connecté"""
        return self.current_user is not None

    def get_current_user(self):
        """Retourne l'utilisateur actuellement connecté"""
        return self.current_user

    def create_user(self, username, password, full_name, confirm_password):
        """Crée un nouveau compte utilisateur"""
        try:
            # Validations
            if not all([username, password, full_name, confirm_password]):
                raise Exception("Tous les champs sont obligatoires")

            if password != confirm_password:
                raise Exception("Les mots de passe ne correspondent pas")

            if len(password) < 4:
                raise Exception("Le mot de passe doit contenir au moins 4 caractères")

            if len(username) < 3:
                raise Exception("Le nom d'utilisateur doit contenir au moins 3 caractères")

            # Créer l'utilisateur
            user_id = self.user_model.create_user(username, password, full_name)
            return True, f"Utilisateur créé avec succès (ID: {user_id})"

        except Exception as e:
            return False, str(e)

    def change_password(self, current_password, new_password, confirm_password):
        """Change le mot de passe de l'utilisateur connecté"""
        try:
            if not self.current_user:
                raise Exception("Aucun utilisateur connecté")

            # Vérifier le mot de passe actuel
            success, _ = self.login(self.current_user['username'], current_password)
            if not success:
                raise Exception("Mot de passe actuel incorrect")

            # Validations
            if new_password != confirm_password:
                raise Exception("Les nouveaux mots de passe ne correspondent pas")

            if len(new_password) < 4:
                raise Exception("Le nouveau mot de passe doit contenir au moins 4 caractères")

            # Changer le mot de passe
            self.user_model.change_password(self.current_user['users_id'], new_password)
            return True, "Mot de passe changé avec succès"

        except Exception as e:
            return False, str(e)