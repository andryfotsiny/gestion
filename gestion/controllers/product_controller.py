# gestion/controllers/product_controller.py
"""
Contrôleur pour la gestion des produits et du stock
"""

from gestion.models.product_model import ProductModel
from gestion.models.category_model import CategoryModel
from gestion.models.vendeur_model import VendeurModel

class ProductController:
    def __init__(self):
        """Initialise le contrôleur produit"""
        self.product_model = ProductModel()
        self.category_model = CategoryModel()
        self.vendeur_model = VendeurModel()

    def create_product(self, name, category_id, purchase_price, selling_price, initial_quantity=0, min_stock_level=5):
        """Crée un nouveau produit"""
        try:
            # Validations
            if not name or not name.strip():
                raise Exception("Le nom du produit est obligatoire")

            if not category_id:
                raise Exception("Veuillez sélectionner une catégorie")

            try:
                purchase_price = float(purchase_price)
                selling_price = float(selling_price)
                initial_quantity = int(initial_quantity) if initial_quantity else 0
                min_stock_level = int(min_stock_level) if min_stock_level else 5
            except ValueError:
                raise Exception("Les prix et quantités doivent être des nombres valides")

            if purchase_price < 0 or selling_price < 0:
                raise Exception("Les prix ne peuvent pas être négatifs")

            if selling_price <= purchase_price:
                raise Exception("Le prix de vente doit être supérieur au prix d'achat")

            if initial_quantity < 0 or min_stock_level < 0:
                raise Exception("Les quantités ne peuvent pas être négatives")

            # Créer le produit
            product_id = self.product_model.create_product(
                name.strip(), category_id, purchase_price, selling_price,
                initial_quantity, min_stock_level
            )

            return True, f"Produit créé avec succès (ID: {product_id})"

        except Exception as e:
            return False, str(e)

    def get_all_products(self):
        """Récupère tous les produits"""
        try:
            return self.product_model.get_all_products()
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des produits: {str(e)}")

    def update_product(self, product_id, name, category_id, purchase_price, selling_price, min_stock_level):
        """Met à jour un produit"""
        try:
            # Validations similaires à create_product
            if not name or not name.strip():
                raise Exception("Le nom du produit est obligatoire")

            try:
                purchase_price = float(purchase_price)
                selling_price = float(selling_price)
                min_stock_level = int(min_stock_level)
            except ValueError:
                raise Exception("Les prix et la quantité minimale doivent être des nombres valides")

            if purchase_price < 0 or selling_price < 0:
                raise Exception("Les prix ne peuvent pas être négatifs")

            if selling_price <= purchase_price:
                raise Exception("Le prix de vente doit être supérieur au prix d'achat")

            # Mettre à jour le produit
            rows_affected = self.product_model.update_product(
                product_id, name.strip(), category_id, purchase_price, selling_price, min_stock_level
            )

            if rows_affected > 0:
                return True, "Produit mis à jour avec succès"
            else:
                return False, "Aucun produit trouvé avec cet ID"

        except Exception as e:
            return False, str(e)

    def add_stock(self, product_id, user_id, quantity, purchase_price, notes=""):
        """Ajoute du stock à un produit"""
        try:
            # Validations
            try:
                quantity = int(quantity)
                purchase_price = float(purchase_price)
            except ValueError:
                raise Exception("La quantité et le prix doivent être des nombres valides")

            if quantity <= 0:
                raise Exception("La quantité doit être positive")

            if purchase_price < 0:
                raise Exception("Le prix ne peut pas être négatif")

            # Ajouter le mouvement de stock
            movement_id = self.product_model.add_stock_movement(
                product_id, user_id, None, 'IN', quantity, purchase_price, notes
            )

            return True, f"Stock ajouté avec succès (Mouvement ID: {movement_id})"

        except Exception as e:
            return False, str(e)

    def sell_product(self, product_id, user_id, vendeur_id, quantity, selling_price, notes=""):
        """Effectue une vente"""
        try:
            # Validations
            try:
                quantity = int(quantity)
                selling_price = float(selling_price)
            except ValueError:
                raise Exception("La quantité et le prix doivent être des nombres valides")

            if quantity <= 0:
                raise Exception("La quantité doit être positive")

            if selling_price < 0:
                raise Exception("Le prix ne peut pas être négatif")

            # Vérifier le stock disponible
            product = self.product_model.get_product_by_id(product_id)
            if not product:
                raise Exception("Produit non trouvé")

            if product['quantity'] < quantity:
                raise Exception(f"Stock insuffisant. Stock disponible: {product['quantity']}")

            # Effectuer la vente
            movement_id = self.product_model.add_stock_movement(
                product_id, user_id, vendeur_id, 'OUT', quantity, selling_price, notes
            )

            return True, f"Vente enregistrée avec succès (Mouvement ID: {movement_id})"

        except Exception as e:
            return False, str(e)

    def get_stock_movements(self, product_id=None, limit=50):
        """Récupère l'historique des mouvements de stock"""
        try:
            return self.product_model.get_stock_movements(product_id, limit)
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des mouvements: {str(e)}")

    def get_low_stock_products(self):
        """Récupère les produits avec un stock faible"""
        try:
            return self.product_model.get_low_stock_products()
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des produits en stock faible: {str(e)}")

    def get_sales_summary(self, start_date=None, end_date=None, vendeur_id=None):
        """Récupère un résumé des ventes"""
        try:
            return self.product_model.get_sales_summary(start_date, end_date, vendeur_id)
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération du résumé: {str(e)}")

    def calculate_profit_margin(self, purchase_price, selling_price):
        """Calcule la marge bénéficiaire"""
        try:
            if purchase_price <= 0:
                return 0
            margin = ((selling_price - purchase_price) / purchase_price) * 100
            return round(margin, 2)
        except:
            return 0