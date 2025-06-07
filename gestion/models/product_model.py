# gestion/models/product_model.py
"""
Modèle pour la gestion des produits et du stock
"""

from gestion.database.database_manager import DatabaseManager
from datetime import datetime

class ProductModel:
    def __init__(self):
        """Initialise le modèle produit"""
        self.db = DatabaseManager()

    def create_product(self, name, category_id, purchase_price, selling_price, initial_quantity=0, min_stock_level=5):
        """Crée un nouveau produit"""
        try:
            query = """
                INSERT INTO products (name, categories_id, purchase_price, selling_price, quantity, min_stock_level)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            product_id = self.db.execute_insert(query, (name, category_id, purchase_price, selling_price, initial_quantity, min_stock_level))

            # Si une quantité initiale est fournie, créer un mouvement de stock
            if initial_quantity > 0:
                self.add_stock_movement(product_id, 1, None, 'IN', initial_quantity, purchase_price, "Stock initial")

            return product_id

        except Exception as e:
            raise Exception(f"Erreur lors de la création du produit: {str(e)}")

    def get_all_products(self):
        """Récupère tous les produits avec leurs catégories"""
        try:
            query = """
                SELECT p.products_id, p.name, p.purchase_price, p.selling_price, 
                       p.quantity, p.min_stock_level, p.created_at, p.last_updated,
                       c.name as category_name
                FROM products p
                LEFT JOIN categories c ON p.categories_id = c.categories_id
                ORDER BY p.name
            """
            return self.db.execute_query(query)

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des produits: {str(e)}")

    def get_product_by_id(self, product_id):
        """Récupère un produit par son ID"""
        try:
            query = """
                SELECT p.*, c.name as category_name
                FROM products p
                LEFT JOIN categories c ON p.categories_id = c.categories_id
                WHERE p.products_id = ?
            """
            result = self.db.execute_query(query, (product_id,))
            return dict(result[0]) if result else None

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération du produit: {str(e)}")

    def update_product(self, product_id, name, category_id, purchase_price, selling_price, min_stock_level):
        """Met à jour un produit"""
        try:
            query = """
                UPDATE products 
                SET name = ?, categories_id = ?, purchase_price = ?, selling_price = ?, min_stock_level = ?
                WHERE products_id = ?
            """
            return self.db.execute_update(query, (name, category_id, purchase_price, selling_price, min_stock_level, product_id))

        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour du produit: {str(e)}")

    def delete_product(self, product_id):
        """Supprime un produit (vérifie d'abord s'il n'y a pas de mouvements)"""
        try:
            # Vérifier s'il y a des mouvements de stock
            check_query = "SELECT COUNT(*) FROM stock_movements WHERE product_id = ?"
            result = self.db.execute_query(check_query, (product_id,))

            if result[0][0] > 0:
                raise Exception("Impossible de supprimer ce produit car il a des mouvements de stock associés")

            query = "DELETE FROM products WHERE products_id = ?"
            return self.db.execute_update(query, (product_id,))

        except Exception as e:
            raise Exception(f"Erreur lors de la suppression du produit: {str(e)}")

    def add_stock_movement(self, product_id, user_id, vendeur_id, movement_type, quantity, unit_price, notes=""):
        """Ajoute un mouvement de stock"""
        try:
            total_amount = quantity * unit_price

            # Insérer le mouvement
            query = """
                INSERT INTO stock_movements (product_id, user_id, vendeur_id, movement_type, quantity, unit_price, total_amount, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            movement_id = self.db.execute_insert(query, (product_id, user_id, vendeur_id, movement_type, quantity, unit_price, total_amount, notes))

            # Mettre à jour la quantité du produit
            if movement_type == 'IN':
                update_query = "UPDATE products SET quantity = quantity + ? WHERE products_id = ?"
            else:  # OUT
                update_query = "UPDATE products SET quantity = quantity - ? WHERE products_id = ?"

            self.db.execute_update(update_query, (quantity, product_id))

            return movement_id

        except Exception as e:
            raise Exception(f"Erreur lors de l'ajout du mouvement de stock: {str(e)}")

    def get_stock_movements(self, product_id=None, limit=None):
        """Récupère les mouvements de stock"""
        try:
            query = """
                SELECT sm.*, p.name as product_name, u.full_name as user_name, v.name as vendeur_name
                FROM stock_movements sm
                JOIN products p ON sm.product_id = p.products_id
                JOIN users u ON sm.user_id = u.users_id
                LEFT JOIN vendeur v ON sm.vendeur_id = v.vendeur_id
            """
            params = []

            if product_id:
                query += " WHERE sm.product_id = ?"
                params.append(product_id)

            query += " ORDER BY sm.created_at DESC"

            if limit:
                query += " LIMIT ?"
                params.append(limit)

            return self.db.execute_query(query, params if params else None)

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des mouvements: {str(e)}")

    def get_low_stock_products(self):
        """Récupère les produits avec un stock faible"""
        try:
            query = """
                SELECT p.*, c.name as category_name
                FROM products p
                LEFT JOIN categories c ON p.categories_id = c.categories_id
                WHERE p.quantity <= p.min_stock_level
                ORDER BY p.quantity ASC
            """
            return self.db.execute_query(query)

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des produits en stock faible: {str(e)}")

    def get_sales_summary(self, start_date=None, end_date=None, vendeur_id=None):
        """Récupère un résumé des ventes"""
        try:
            query = """
                SELECT 
                    DATE(sm.created_at) as date,
                    p.name as product_name,
                    v.name as vendeur_name,
                    SUM(sm.quantity) as total_quantity,
                    SUM(sm.total_amount) as total_sales,
                    SUM(sm.quantity * p.purchase_price) as total_cost,
                    SUM(sm.total_amount - (sm.quantity * p.purchase_price)) as profit
                FROM stock_movements sm
                JOIN products p ON sm.product_id = p.products_id
                LEFT JOIN vendeur v ON sm.vendeur_id = v.vendeur_id
                WHERE sm.movement_type = 'OUT'
            """
            params = []

            if start_date:
                query += " AND DATE(sm.created_at) >= ?"
                params.append(start_date)

            if end_date:
                query += " AND DATE(sm.created_at) <= ?"
                params.append(end_date)

            if vendeur_id:
                query += " AND sm.vendeur_id = ?"
                params.append(vendeur_id)

            query += " GROUP BY DATE(sm.created_at), sm.product_id, sm.vendeur_id ORDER BY sm.created_at DESC"

            return self.db.execute_query(query, params if params else None)

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération du résumé des ventes: {str(e)}")