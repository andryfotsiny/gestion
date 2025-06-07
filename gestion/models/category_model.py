# gestion/models/category_model.py
"""
Modèle pour la gestion des catégories de produits
"""

from gestion.database.database_manager import DatabaseManager

class CategoryModel:
    def __init__(self):
        """Initialise le modèle catégorie"""
        self.db = DatabaseManager()

    def create_category(self, name):
        """Crée une nouvelle catégorie"""
        try:
            query = "INSERT INTO categories (name) VALUES (?)"
            category_id = self.db.execute_insert(query, (name,))
            return category_id

        except Exception as e:
            raise Exception(f"Erreur lors de la création de la catégorie: {str(e)}")

    def get_all_categories(self):
        """Récupère toutes les catégories"""
        try:
            query = """
                SELECT c.categories_id, c.name, COUNT(p.products_id) as product_count
                FROM categories c
                LEFT JOIN products p ON c.categories_id = p.categories_id
                GROUP BY c.categories_id, c.name
                ORDER BY c.name
            """
            return self.db.execute_query(query)

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des catégories: {str(e)}")

    def get_category_by_id(self, category_id):
        """Récupère une catégorie par son ID"""
        try:
            query = "SELECT * FROM categories WHERE categories_id = ?"
            result = self.db.execute_query(query, (category_id,))
            return dict(result[0]) if result else None

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de la catégorie: {str(e)}")

    def update_category(self, category_id, name):
        """Met à jour une catégorie"""
        try:
            query = "UPDATE categories SET name = ? WHERE categories_id = ?"
            return self.db.execute_update(query, (name, category_id))

        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour de la catégorie: {str(e)}")

    def delete_category(self, category_id):
        """Supprime une catégorie (vérifie d'abord s'il n'y a pas de produits)"""
        try:
            # Vérifier s'il y a des produits dans cette catégorie
            check_query = "SELECT COUNT(*) FROM products WHERE categories_id = ?"
            result = self.db.execute_query(check_query, (category_id,))

            if result[0][0] > 0:
                raise Exception("Impossible de supprimer cette catégorie car elle contient des produits")

            query = "DELETE FROM categories WHERE categories_id = ?"
            return self.db.execute_update(query, (category_id,))

        except Exception as e:
            raise Exception(f"Erreur lors de la suppression de la catégorie: {str(e)}")