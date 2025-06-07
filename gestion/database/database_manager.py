# gestion/database/database_manager.py
"""
Gestionnaire de base de données SQLite pour l'application de gestion d'inventaire
"""

import sqlite3
import hashlib
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="gestion/database/inventory.db"):
        """Initialise le gestionnaire de base de données"""
        self.db_path = db_path
        # Créer le dossier de base de données s'il n'existe pas
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_connection()

    def init_connection(self):
        """Initialise la connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise Exception(f"Erreur de connexion à la base de données: {str(e)}")

    def create_tables(self):
        """Crée toutes les tables nécessaires"""
        tables_sql = [
            # Table des utilisateurs
            """
            CREATE TABLE IF NOT EXISTS users (
                users_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status BOOLEAN DEFAULT 1
            )
            """,

            # Table des catégories
            """
            CREATE TABLE IF NOT EXISTS categories (
                categories_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) UNIQUE NOT NULL
            )
            """,

            # Table des vendeurs
            """
            CREATE TABLE IF NOT EXISTS vendeur (
                vendeur_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                telephone VARCHAR(20),
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # Table des produits
            """
            CREATE TABLE IF NOT EXISTS products (
                products_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                categories_id INTEGER,
                purchase_price DECIMAL(10,2) NOT NULL,
                selling_price DECIMAL(10,2) NOT NULL,
                quantity INTEGER DEFAULT 0,
                min_stock_level INTEGER DEFAULT 5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (categories_id) REFERENCES categories(categories_id)
            )
            """,

            # Table des mouvements de stock
            """
            CREATE TABLE IF NOT EXISTS stock_movements (
                stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                vendeur_id INTEGER,
                movement_type VARCHAR(20) NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(products_id),
                FOREIGN KEY (user_id) REFERENCES users(users_id),
                FOREIGN KEY (vendeur_id) REFERENCES vendeur(vendeur_id)
            )
            """
        ]

        # Index pour optimiser les performances
        indexes_sql = [
            "CREATE INDEX IF NOT EXISTS idx_products_category ON products(categories_id)",
            "CREATE INDEX IF NOT EXISTS idx_stock_movements_product ON stock_movements(product_id)",
            "CREATE INDEX IF NOT EXISTS idx_stock_movements_user ON stock_movements(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_stock_movements_date ON stock_movements(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)"
        ]

        # Trigger pour mettre à jour le timestamp
        trigger_sql = """
        CREATE TRIGGER IF NOT EXISTS update_product_timestamp
            AFTER UPDATE ON products
            BEGIN
                UPDATE products SET last_updated = CURRENT_TIMESTAMP 
                WHERE products_id = NEW.products_id;
            END
        """

        try:
            # Créer les tables
            for sql in tables_sql:
                self.cursor.execute(sql)

            # Créer les index
            for sql in indexes_sql:
                self.cursor.execute(sql)

            # Créer le trigger
            self.cursor.execute(trigger_sql)

            self.connection.commit()
            print("✅ Tables créées avec succès")

        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erreur lors de la création des tables: {str(e)}")

    def create_default_admin(self):
        """Crée un utilisateur administrateur par défaut"""
        try:
            # Vérifier si l'admin existe déjà
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", ("admin",))
            if self.cursor.fetchone()[0] > 0:
                return

            # Créer l'administrateur par défaut
            password_hash = hashlib.sha256("admin".encode()).hexdigest()
            self.cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, status)
                VALUES (?, ?, ?, ?)
            """, ("admin", password_hash, "Administrateur", 1))

            # Créer des catégories par défaut
            default_categories = ["Boissons", "Alimentaire", "Accessoires", "Autres"]
            for category in default_categories:
                self.cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category,))

            self.connection.commit()
            print("✅ Données par défaut créées")

        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erreur lors de la création des données par défaut: {str(e)}")

    def execute_query(self, query, params=None):
        """Exécute une requête SQL"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erreur lors de l'exécution de la requête: {str(e)}")

    def execute_insert(self, query, params=None):
        """Exécute une requête d'insertion et retourne l'ID"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erreur lors de l'insertion: {str(e)}")

    def execute_update(self, query, params=None):
        """Exécute une requête de mise à jour"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erreur lors de la mise à jour: {str(e)}")

    def close(self):
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()

    def __del__(self):
        """Destructeur pour fermer automatiquement la connexion"""
        self.close()