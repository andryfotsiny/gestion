# gestion/controllers/vendeur_controller.py
"""
Contrôleur pour la gestion des vendeurs
"""

from gestion.models.vendeur_model import VendeurModel

class VendeurController:
    def __init__(self):
        """Initialise le contrôleur vendeur"""
        self.vendeur_model = VendeurModel()

    def create_vendeur(self, name, telephone=""):
        """Crée un nouveau vendeur"""
        try:
            # Validations
            if not name or not name.strip():
                raise Exception("Le nom du vendeur est obligatoire")

            if len(name.strip()) < 2:
                raise Exception("Le nom doit contenir au moins 2 caractères")

            if telephone and len(telephone.strip()) < 8:
                raise Exception("Le numéro de téléphone doit contenir au moins 8 chiffres")

            # Créer le vendeur
            vendeur_id = self.vendeur_model.create_vendeur(name.strip(), telephone.strip())

            return True, f"Vendeur créé avec succès (ID: {vendeur_id})"

        except Exception as e:
            return False, str(e)

    def get_all_vendeurs(self, active_only=False):
        """Récupère tous les vendeurs"""
        try:
            return self.vendeur_model.get_all_vendeurs(active_only)
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des vendeurs: {str(e)}")

    def update_vendeur(self, vendeur_id, name, telephone):
        """Met à jour un vendeur"""
        try:
            # Validations
            if not name or not name.strip():
                raise Exception("Le nom du vendeur est obligatoire")

            if len(name.strip()) < 2:
                raise Exception("Le nom doit contenir au moins 2 caractères")

            if telephone and len(telephone.strip()) < 8:
                raise Exception("Le numéro de téléphone doit contenir au moins 8 chiffres")

            # Mettre à jour le vendeur
            rows_affected = self.vendeur_model.update_vendeur(vendeur_id, name.strip(), telephone.strip())

            if rows_affected > 0:
                return True, "Vendeur mis à jour avec succès"
            else:
                return False, "Aucun vendeur trouvé avec cet ID"

        except Exception as e:
            return False, str(e)

    def toggle_vendeur_status(self, vendeur_id):
        """Active/désactive un vendeur"""
        try:
            rows_affected = self.vendeur_model.toggle_vendeur_status(vendeur_id)

            if rows_affected > 0:
                return True, "Statut du vendeur modifié avec succès"
            else:
                return False, "Aucun vendeur trouvé avec cet ID"

        except Exception as e:
            return False, str(e)

    def get_vendeur_sales_stats(self, vendeur_id=None, start_date=None, end_date=None):
        """Récupère les statistiques de vente d'un vendeur"""
        try:
            return self.vendeur_model.get_vendeur_sales_stats(vendeur_id, start_date, end_date)
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des statistiques: {str(e)}")

    def get_active_vendeur(self):
        """Récupère le vendeur actuellement actif"""
        try:
            return self.vendeur_model.get_active_vendeur()
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération du vendeur actif: {str(e)}")