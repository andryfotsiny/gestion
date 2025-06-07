# gestion/models/user_model.py
"""
Modèle pour la gestion des utilisateurs
"""

import hashlib
from gestion.database.database_manager import DatabaseManager

class UserModel:
    def __init__(self):
        """Initialise le modèle utilisateur"""
        self.db = DatabaseManager()

    def authenticate(self, username, password):
        """Authentifie un utilisateur"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            query = """
                SELECT users_id, username, full_name, status 
                FROM users 
                WHERE username = ? AND password_hash = ? AND status = 1
            """
            result = self.db.execute_query(query, (username, password_hash))

            if result:
                user_data = dict(result[0])
                return user_data
            return None

        except Exception as e:
            raise Exception(f"Erreur lors de l'authentification: {str(e)}")

    def create_user(self, username, password, full_name):
        """Crée un nouveau utilisateur"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            query = """
                INSERT INTO users (username, password_hash, full_name, status)
                VALUES (?, ?, ?, 1)
            """
            user_id = self.db.execute_insert(query, (username, password_hash, full_name))
            return user_id

        except Exception as e:
            raise Exception(f"Erreur lors de la création de l'utilisateur: {str(e)}")

    def get_all_users(self):
        """Récupère tous les utilisateurs"""
        try:
            query = """
                SELECT users_id, username, full_name, created_at, status
                FROM users
                ORDER BY created_at DESC
            """
            return self.db.execute_query(query)

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des utilisateurs: {str(e)}")

    def update_user_status(self, user_id, status):
        """Met à jour le statut d'un utilisateur"""
        try:
            query = "UPDATE users SET status = ? WHERE users_id = ?"
            return self.db.execute_update(query, (status, user_id))

        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour du statut: {str(e)}")

    def change_password(self, user_id, new_password):
        """Change le mot de passe d'un utilisateur"""
        try:
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            query = "UPDATE users SET password_hash = ? WHERE users_id = ?"
            return self.db.execute_update(query, (password_hash, user_id))

        except Exception as e:
            raise Exception(f"Erreur lors du changement de mot de passe: {str(e)}")