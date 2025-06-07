# gestion/utils/helpers.py
"""
Fonctions utilitaires pour l'application
"""

import re
import os
import shutil
import logging
from datetime import datetime, timedelta
from gestion.config.config import config

def setup_logging():
    """Configure le système de logging"""
    try:
        # Créer le répertoire des logs s'il n'existe pas
        config.ensure_directories()

        # Configuration du logging
        log_filename = os.path.join(config.LOGS_DIR, f"app_{datetime.now().strftime('%Y%m%d')}.log")

        logging.basicConfig(
            level=getattr(logging, config.LOG_CONFIG['level']),
            format=config.LOG_CONFIG['format'],
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

        return logging.getLogger(__name__)

    except Exception as e:
        print(f"Erreur lors de la configuration du logging: {e}")
        return logging.getLogger(__name__)

def validate_email(email):
    """Valide un format d'email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Valide un numéro de téléphone (format Madagascar)"""
    # Retire tous les espaces et tirets
    clean_phone = re.sub(r'[\s-]', '', phone)

    # Vérifie le format : +261, 0, ou directement les chiffres
    patterns = [
        r'^(\+261|0)[0-9]{9}$',  # Format complet
        r'^[0-9]{9}$'            # Sans indicatif
    ]

    return any(re.match(pattern, clean_phone) for pattern in patterns)

def format_currency(amount):
    """Formate un montant en devise locale"""
    try:
        return config.format_currency(float(amount))
    except (ValueError, TypeError):
        return "0 Ar"

def format_date(date_str, input_format="%Y-%m-%d %H:%M:%S", output_format="%d/%m/%Y"):
    """Formate une date"""
    try:
        if isinstance(date_str, str):
            date_obj = datetime.strptime(date_str[:19], input_format)
        else:
            date_obj = date_str
        return date_obj.strftime(output_format)
    except:
        return date_str

def format_datetime(datetime_str, input_format="%Y-%m-%d %H:%M:%S", output_format="%d/%m/%Y %H:%M"):
    """Formate une date et heure"""
    try:
        if isinstance(datetime_str, str):
            date_obj = datetime.strptime(datetime_str[:19], input_format)
        else:
            date_obj = datetime_str
        return date_obj.strftime(output_format)
    except:
        return datetime_str

def calculate_percentage(part, total):
    """Calcule un pourcentage"""
    try:
        if total == 0:
            return 0
        return round((part / total) * 100, 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

def truncate_text(text, max_length=50, suffix="..."):
    """Tronque un texte si il est trop long"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def clean_filename(filename):
    """Nettoie un nom de fichier en retirant les caractères interdits"""
    # Caractères interdits dans les noms de fichiers
    invalid_chars = r'[<>:"/\\|?*]'
    # Remplacer par des underscores
    clean_name = re.sub(invalid_chars, '_', filename)
    # Retirer les espaces en début/fin
    clean_name = clean_name.strip()
    # Limiter la longueur
    return clean_name[:200]

def backup_database(db_path, backup_dir=None):
    """Crée une sauvegarde de la base de données"""
    try:
        if backup_dir is None:
            backup_dir = config.LOGS_DIR

        # Créer le répertoire de sauvegarde
        os.makedirs(backup_dir, exist_ok=True)

        # Nom du fichier de sauvegarde
        backup_filename = config.get_backup_filename()
        backup_path = os.path.join(backup_dir, backup_filename)

        # Copier la base de données
        shutil.copy2(db_path, backup_path)

        # Nettoyer les anciennes sauvegardes
        cleanup_old_backups(backup_dir)

        return backup_path

    except Exception as e:
        raise Exception(f"Erreur lors de la sauvegarde: {str(e)}")

def cleanup_old_backups(backup_dir, max_backups=None):
    """Supprime les anciennes sauvegardes"""
    try:
        if max_backups is None:
            max_backups = config.DB_CONFIG['max_backups']

        # Lister tous les fichiers de sauvegarde
        backup_files = []
        for filename in os.listdir(backup_dir):
            if filename.startswith('inventory_backup_') and filename.endswith('.db'):
                filepath = os.path.join(backup_dir, filename)
                # Obtenir la date de modification
                mtime = os.path.getmtime(filepath)
                backup_files.append((filepath, mtime))

        # Trier par date (plus récent en premier)
        backup_files.sort(key=lambda x: x[1], reverse=True)

        # Supprimer les fichiers excédentaires
        for filepath, _ in backup_files[max_backups:]:
            os.remove(filepath)

    except Exception as e:
        logging.warning(f"Erreur lors du nettoyage des sauvegardes: {e}")

def get_date_range_options():
    """Retourne les options de plage de dates communes"""
    today = datetime.now().date()

    return {
        "Aujourd'hui": (today, today),
        "Hier": (today - timedelta(days=1), today - timedelta(days=1)),
        "7 derniers jours": (today - timedelta(days=7), today),
        "30 derniers jours": (today - timedelta(days=30), today),
        "Ce mois": (today.replace(day=1), today),
        "Mois dernier": get_last_month_range(),
        "Cette année": (today.replace(month=1, day=1), today)
    }

def get_last_month_range():
    """Retourne la plage de dates du mois dernier"""
    today = datetime.now().date()
    first_day_this_month = today.replace(day=1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = last_day_last_month.replace(day=1)
    return (first_day_last_month, last_day_last_month)

def export_to_csv(data, headers, filename):
    """Exporte des données vers un fichier CSV"""
    import csv
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Écrire les en-têtes
            writer.writerow(headers)
            # Écrire les données
            for row in data:
                writer.writerow(row)
        return True
    except Exception as e:
        logging.error(f"Erreur lors de l'export CSV: {e}")
        return False

def import_from_csv(filename):
    """Importe des données depuis un fichier CSV"""
    import csv
    try:
        data = []
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        logging.error(f"Erreur lors de l'import CSV: {e}")
        return []

def validate_positive_number(value, field_name="Valeur"):
    """Valide qu'une valeur est un nombre positif"""
    try:
        num_value = float(value)
        if num_value < 0:
            raise ValueError(f"{field_name} ne peut pas être négatif")
        return num_value
    except ValueError:
        raise ValueError(f"{field_name} doit être un nombre valide")

def validate_positive_integer(value, field_name="Valeur"):
    """Valide qu'une valeur est un entier positif"""
    try:
        int_value = int(value)
        if int_value < 0:
            raise ValueError(f"{field_name} ne peut pas être négatif")
        return int_value
    except ValueError:
        raise ValueError(f"{field_name} doit être un nombre entier valide")

def safe_division(numerator, denominator, default=0):
    """Division sécurisée qui évite la division par zéro"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default

def generate_report_filename(report_type, extension="pdf"):
    """Génère un nom de fichier pour un rapport"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_type = clean_filename(report_type.lower().replace(' ', '_'))
    return f"rapport_{clean_type}_{timestamp}.{extension}"

def center_window(window, width, height):
    """Centre une fenêtre sur l'écran"""
    # Obtenir les dimensions de l'écran
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculer les coordonnées pour centrer
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Appliquer la géométrie
    window.geometry(f"{width}x{height}+{x}+{y}")

def show_loading_cursor(widget):
    """Affiche un curseur de chargement"""
    widget.config(cursor="wait")
    widget.update()

def hide_loading_cursor(widget):
    """Cache le curseur de chargement"""
    widget.config(cursor="")

class ValidationError(Exception):
    """Exception personnalisée pour les erreurs de validation"""
    pass

class BusinessLogicError(Exception):
    """Exception personnalisée pour les erreurs de logique métier"""
    pass

def log_user_action(user_id, action, details=""):
    """Enregistre une action utilisateur dans les logs"""
    logger = logging.getLogger(__name__)
    logger.info(f"Utilisateur {user_id} - {action} - {details}")

def format_file_size(size_bytes):
    """Formate une taille de fichier en bytes vers une unité lisible"""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def get_system_info():
    """Retourne des informations système basiques"""
    import platform
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'python_version': platform.python_version(),
        'app_version': config.APP_VERSION
    }