# gestion/controllers/category_controller.py
"""
Contrôleur pour la gestion des catégories
"""

from gestion.models.category_model import CategoryModel

class CategoryController:
    def __init__(self):
        """Initialise le contrôleur catégorie"""
        self.category_model = CategoryModel()

    def create_category(self, name):
        """Crée une nouvelle catégorie"""
        try:
            # Validations
            if not name or not name.strip():
                raise Exception("Le nom de la catégorie est obligatoire")

            if len(name.strip()) < 2:
                raise Exception("Le nom doit contenir au moins 2 caractères")

            if len(name.strip()) > 100:
                raise Exception("Le nom ne peut pas dépasser 100 caractères")

            # Créer la catégorie
            category_id = self.category_model.create_category(name.strip())

            return True, f"Catégorie créée avec succès (ID: {category_id})"

        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return False, "Cette catégorie existe déjà"
            return False, str(e)

    def get_all_categories(self):
        """Récupère toutes les catégories"""
        try:
            return self.category_model.get_all_categories()
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des catégories: {str(e)}")

    def get_category_by_id(self, category_id):
        """Récupère une catégorie par son ID"""
        try:
            return self.category_model.get_category_by_id(category_id)
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de la catégorie: {str(e)}")

    def update_category(self, category_id, name):
        """Met à jour une catégorie"""
        try:
            # Validations
            if not name or not name.strip():
                raise Exception("Le nom de la catégorie est obligatoire")

            if len(name.strip()) < 2:
                raise Exception("Le nom doit contenir au moins 2 caractères")

            if len(name.strip()) > 100:
                raise Exception("Le nom ne peut pas dépasser 100 caractères")

            # Mettre à jour la catégorie
            rows_affected = self.category_model.update_category(category_id, name.strip())

            if rows_affected > 0:
                return True, "Catégorie mise à jour avec succès"
            else:
                return False, "Aucune catégorie trouvée avec cet ID"

        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return False, "Cette catégorie existe déjà"
            return False, str(e)

    def delete_category(self, category_id):
        """Supprime une catégorie"""
        try:
            rows_affected = self.category_model.delete_category(category_id)

            if rows_affected > 0:
                return True, "Catégorie supprimée avec succès"
            else:
                return False, "Aucune catégorie trouvée avec cet ID"

        except Exception as e:
            return False, str(e)