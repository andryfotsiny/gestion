# gestion/config/config.py
"""
Configuration de l'application
"""

import os
from datetime import datetime

class Config:
    """Configuration principale de l'application"""

    # Base de données
    DATABASE_PATH = "gestion/database/inventory.db"

    # Répertoires
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGS_DIR = os.path.join(BASE_DIR, "..", "logs")

    # Application
    APP_NAME = "Gestion d'Inventaire"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "Votre Entreprise"

    # Interface utilisateur
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 700
    WINDOW_MIN_WIDTH = 800
    WINDOW_MIN_HEIGHT = 600

    # Couleurs de l'interface
    COLORS = {
        'primary': '#3498db',
        'secondary': '#2c3e50',
        'success': '#27ae60',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#343a40',
        'background': '#ecf0f1',
        'white': '#ffffff'
    }

    # Polices
    FONTS = {
        'default': ('Segoe UI', 10),
        'title': ('Segoe UI', 16, 'bold'),
        'subtitle': ('Segoe UI', 12, 'bold'),
        'small': ('Segoe UI', 8),
        'button': ('Segoe UI', 9)
    }

    # Paramètres de la base de données
    DB_CONFIG = {
        'backup_interval': 24,  # heures
        'max_backups': 7,
        'auto_vacuum': True
    }

    # Logs
    LOG_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(levelname)s - %(message)s',
        'max_size': 10,  # MB
        'backup_count': 5
    }

    # Devises
    CURRENCY = {
        'symbol': 'Ar',
        'name': 'Ariary',
        'format': '{:,.0f} Ar'
    }

    # Pagination
    PAGINATION = {
        'items_per_page': 50,
        'max_items_per_page': 200
    }

    # Validation
    VALIDATION = {
        'min_password_length': 4,
        'min_username_length': 3,
        'max_product_name_length': 200,
        'max_category_name_length': 100
    }

    @classmethod
    def ensure_directories(cls):
        """Crée les répertoires nécessaires s'ils n'existent pas"""
        directories = [
            cls.LOGS_DIR,
            os.path.dirname(cls.DATABASE_PATH)
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    @classmethod
    def get_backup_filename(cls):
        """Génère un nom de fichier de sauvegarde avec timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"inventory_backup_{timestamp}.db"

    @classmethod
    def format_currency(cls, amount):
        """Formate un montant selon la devise configurée"""
        return cls.CURRENCY['format'].format(amount)

# Configuration pour le développement
class DevelopmentConfig(Config):
    """Configuration pour l'environnement de développement"""
    DEBUG = True
    LOG_CONFIG = {
        'level': 'DEBUG',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'max_size': 5,  # MB
        'backup_count': 3
    }

# Configuration pour la production
class ProductionConfig(Config):
    """Configuration pour l'environnement de production"""
    DEBUG = False
    LOG_CONFIG = {
        'level': 'WARNING',
        'format': '%(asctime)s - %(levelname)s - %(message)s',
        'max_size': 20,  # MB
        'backup_count': 10
    }

# Configuration active
config = DevelopmentConfig()