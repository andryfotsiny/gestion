# gestion/models/vendeur_model.py
"""
Modèle pour la gestion des vendeurs
"""

from gestion.database.database_manager import DatabaseManager

class VendeurModel:
    def __init__(self):
        """Initialise le modèle vendeur"""
        self.db = DatabaseManager()

    def create_vendeur(self, name, telephone=""):
        """Crée un nouveau vendeur"""
        try:
            query = """
                INSERT INTO vendeur (name, telephone, is_active)
                VALUES (?, ?, 1)
            """
            vendeur_id = self.db.execute_insert(query, (name, telephone))
            return vendeur_id

        except Exception as e:
            raise Exception(f"Erreur lors de la création du vendeur: {str(e)}")

    def get_all_vendeurs(self, active_only=False):
        """Récupère tous les vendeurs"""
        try:
            query = """
                SELECT vendeur_id, name, telephone, is_active, created_at
                FROM vendeur
            """
            if active_only:
                query += " WHERE is_active = 1"

            query += " ORDER BY name"

            return self.db.execute_query(query)

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des vendeurs: {str(e)}")

    def get_vendeur_by_id(self, vendeur_id):
        """Récupère un vendeur par son ID"""
        try:
            query = "SELECT * FROM vendeur WHERE vendeur_id = ?"
            result = self.db.execute_query(query, (vendeur_id,))
            return dict(result[0]) if result else None

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération du vendeur: {str(e)}")

    def update_vendeur(self, vendeur_id, name, telephone):
        """Met à jour un vendeur"""
        try:
            query = """
                UPDATE vendeur 
                SET name = ?, telephone = ?
                WHERE vendeur_id = ?
            """
            return self.db.execute_update(query, (name, telephone, vendeur_id))

        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour du vendeur: {str(e)}")

    def toggle_vendeur_status(self, vendeur_id):
        """Active/désactive un vendeur"""
        try:
            # Récupérer le statut actuel
            query = "SELECT is_active FROM vendeur WHERE vendeur_id = ?"
            result = self.db.execute_query(query, (vendeur_id,))

            if not result:
                raise Exception("Vendeur non trouvé")

            current_status = result[0][0]
            new_status = 0 if current_status else 1

            # Mettre à jour le statut
            update_query = "UPDATE vendeur SET is_active = ? WHERE vendeur_id = ?"
            return self.db.execute_update(update_query, (new_status, vendeur_id))

        except Exception as e:
            raise Exception(f"Erreur lors du changement de statut du vendeur: {str(e)}")

    def get_vendeur_sales_stats(self, vendeur_id=None, start_date=None, end_date=None):
        """Récupère les statistiques de vente d'un vendeur"""
        try:
            query = """
                SELECT 
                    v.name as vendeur_name,
                    COUNT(sm.stock_id) as total_transactions,
                    SUM(sm.quantity) as total_quantity_sold,
                    SUM(sm.total_amount) as total_sales,
                    SUM(sm.quantity * p.purchase_price) as total_cost,
                    SUM(sm.total_amount - (sm.quantity * p.purchase_price)) as total_profit
                FROM vendeur v
                LEFT JOIN stock_movements sm ON v.vendeur_id = sm.vendeur_id AND sm.movement_type = 'OUT'
                LEFT JOIN products p ON sm.product_id = p.products_id
            """
            params = []

            where_conditions = []

            if vendeur_id:
                where_conditions.append("v.vendeur_id = ?")
                params.append(vendeur_id)

            if start_date:
                where_conditions.append("DATE(sm.created_at) >= ?")
                params.append(start_date)

            if end_date:
                where_conditions.append("DATE(sm.created_at) <= ?")
                params.append(end_date)

            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)

            query += " GROUP BY v.vendeur_id, v.name ORDER BY total_sales DESC"

            return self.db.execute_query(query, params if params else None)

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des statistiques: {str(e)}")

    def get_active_vendeur(self):
        """Récupère le vendeur actuellement actif (le dernier utilisé)"""
        try:
            query = """
                SELECT DISTINCT v.*
                FROM vendeur v
                JOIN stock_movements sm ON v.vendeur_id = sm.vendeur_id
                WHERE v.is_active = 1
                ORDER BY sm.created_at DESC
                LIMIT 1
            """
            result = self.db.execute_query(query)
            return dict(result[0]) if result else None

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération du vendeur actif: {str(e)}")