# gestion/utils/validators.py
"""
Fonctions de validation des données pour l'application
"""

import re
from datetime import datetime

class ValidationError(Exception):
    """Exception personnalisée pour les erreurs de validation"""
    pass

def validate_required(value, field_name="Champ"):
    """Valide qu'un champ obligatoire n'est pas vide"""
    if not value or (isinstance(value, str) and not value.strip()):
        raise ValidationError(f"{field_name} est obligatoire")
    return value.strip() if isinstance(value, str) else value

def validate_string_length(value, min_length=None, max_length=None, field_name="Champ"):
    """Valide la longueur d'une chaîne"""
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} doit être une chaîne de caractères")

    length = len(value.strip())

    if min_length and length < min_length:
        raise ValidationError(f"{field_name} doit contenir au moins {min_length} caractères")

    if max_length and length > max_length:
        raise ValidationError(f"{field_name} ne peut pas dépasser {max_length} caractères")

    return value.strip()

def validate_positive_number(value, field_name="Valeur", allow_zero=False):
    """Valide qu'une valeur est un nombre positif"""
    try:
        num_value = float(value)

        if allow_zero and num_value < 0:
            raise ValidationError(f"{field_name} ne peut pas être négatif")
        elif not allow_zero and num_value <= 0:
            raise ValidationError(f"{field_name} doit être positif")

        return num_value

    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} doit être un nombre valide")

def validate_positive_integer(value, field_name="Valeur", allow_zero=False):
    """Valide qu'une valeur est un entier positif"""
    try:
        int_value = int(value)

        if allow_zero and int_value < 0:
            raise ValidationError(f"{field_name} ne peut pas être négatif")
        elif not allow_zero and int_value <= 0:
            raise ValidationError(f"{field_name} doit être positif")

        return int_value

    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} doit être un nombre entier valide")

def validate_phone_number(phone, required=False):
    """Valide un numéro de téléphone (format Madagascar)"""
    if not phone or not phone.strip():
        if required:
            raise ValidationError("Le numéro de téléphone est obligatoire")
        return ""

    # Nettoyer le numéro (retirer espaces, tirets, parenthèses)
    clean_phone = re.sub(r'[\s\-\(\)]', '', phone.strip())

    # Patterns valides pour Madagascar
    patterns = [
        r'^\+261[0-9]{9}$',      # +261XXXXXXXXX
        r'^0[0-9]{9}$',          # 0XXXXXXXXX
        r'^[0-9]{9}$',           # XXXXXXXXX (sans indicatif)
        r'^261[0-9]{9}$'         # 261XXXXXXXXX
    ]

    if not any(re.match(pattern, clean_phone) for pattern in patterns):
        raise ValidationError("Format de téléphone invalide (ex: +261 34 12 345 67)")

    return clean_phone

def validate_email(email, required=False):
    """Valide un format d'email"""
    if not email or not email.strip():
        if required:
            raise ValidationError("L'adresse email est obligatoire")
        return ""

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email.strip()):
        raise ValidationError("Format d'email invalide")

    return email.strip().lower()

def validate_price_margin(purchase_price, selling_price):
    """Valide que le prix de vente est supérieur au prix d'achat"""
    try:
        purchase = float(purchase_price)
        selling = float(selling_price)

        if selling <= purchase:
            raise ValidationError("Le prix de vente doit être supérieur au prix d'achat")

        return purchase, selling

    except (ValueError, TypeError):
        raise ValidationError("Les prix doivent être des nombres valides")

def validate_stock_quantity(current_stock, requested_quantity, operation_type):
    """Valide une opération de stock"""
    try:
        current = int(current_stock)
        requested = int(requested_quantity)

        if requested <= 0:
            raise ValidationError("La quantité doit être positive")

        if operation_type == 'OUT' and current < requested:
            raise ValidationError(f"Stock insuffisant. Disponible: {current}, Demandé: {requested}")

        return current, requested

    except (ValueError, TypeError):
        raise ValidationError("Les quantités doivent être des nombres entiers")

def validate_date_range(start_date, end_date):
    """Valide une plage de dates"""
    if start_date and end_date:
        try:
            if isinstance(start_date, str):
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
            else:
                start = start_date

            if isinstance(end_date, str):
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
            else:
                end = end_date

            if start > end:
                raise ValidationError("La date de début doit être antérieure à la date de fin")

            return start, end

        except ValueError:
            raise ValidationError("Format de date invalide (YYYY-MM-DD)")

    return start_date, end_date

def validate_category_name(name):
    """Valide un nom de catégorie"""
    name = validate_required(name, "Nom de la catégorie")
    name = validate_string_length(name, min_length=2, max_length=100, field_name="Nom de la catégorie")

    # Vérifier les caractères interdits
    if re.search(r'[<>:"/\\|?*]', name):
        raise ValidationError("Le nom de catégorie contient des caractères interdits")

    return name

def validate_product_name(name):
    """Valide un nom de produit"""
    name = validate_required(name, "Nom du produit")
    name = validate_string_length(name, min_length=2, max_length=200, field_name="Nom du produit")

    # Vérifier les caractères interdits
    if re.search(r'[<>:"/\\|?*]', name):
        raise ValidationError("Le nom du produit contient des caractères interdits")

    return name

def validate_vendeur_name(name):
    """Valide un nom de vendeur"""
    name = validate_required(name, "Nom du vendeur")
    name = validate_string_length(name, min_length=2, max_length=100, field_name="Nom du vendeur")

    # Vérifier que le nom contient au moins une lettre
    if not re.search(r'[a-zA-ZàâäéèêëïîôöùûüÿçÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÇ]', name):
        raise ValidationError("Le nom doit contenir au moins une lettre")

    return name

def validate_username(username):
    """Valide un nom d'utilisateur"""
    username = validate_required(username, "Nom d'utilisateur")
    username = validate_string_length(username, min_length=3, max_length=50, field_name="Nom d'utilisateur")

    # Vérifier le format (lettres, chiffres, underscore seulement)
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError("Le nom d'utilisateur ne peut contenir que des lettres, chiffres et underscore")

    return username.lower()

def validate_password(password, min_length=4):
    """Valide un mot de passe"""
    password = validate_required(password, "Mot de passe")

    if len(password) < min_length:
        raise ValidationError(f"Le mot de passe doit contenir au moins {min_length} caractères")

    return password

def sanitize_filename(filename):
    """Nettoie un nom de fichier en retirant les caractères interdits"""
    if not filename:
        return "fichier_sans_nom"

    # Remplacer les caractères interdits par des underscores
    clean_name = re.sub(r'[<>:"/\\|?*]', '_', filename)

    # Retirer les espaces en début/fin
    clean_name = clean_name.strip()

    # Remplacer les espaces multiples par un seul underscore
    clean_name = re.sub(r'\s+', '_', clean_name)

    # Limiter la longueur
    if len(clean_name) > 200:
        name, ext = clean_name.rsplit('.', 1) if '.' in clean_name else (clean_name, '')
        clean_name = name[:195] + ('.' + ext if ext else '')

    return clean_name or "fichier_sans_nom"

def validate_file_path(file_path):
    """Valide un chemin de fichier"""
    if not file_path:
        raise ValidationError("Chemin de fichier requis")

    # Vérifier que le chemin n'est pas dangereux
    if '..' in file_path or file_path.startswith('/'):
        raise ValidationError("Chemin de fichier non autorisé")

    return file_path

# Fonctions de validation groupées pour différents contextes

def validate_product_data(name, category_id, purchase_price, selling_price, initial_quantity=0, min_stock_level=5):
    """Valide toutes les données d'un produit"""
    errors = []
    validated_data = {}

    try:
        validated_data['name'] = validate_product_name(name)
    except ValidationError as e:
        errors.append(str(e))

    try:
        validated_data['category_id'] = validate_positive_integer(category_id, "ID de catégorie")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validated_data['purchase_price'] = validate_positive_number(purchase_price, "Prix d'achat")
        validated_data['selling_price'] = validate_positive_number(selling_price, "Prix de vente")

        # Vérifier la marge
        validate_price_margin(validated_data.get('purchase_price', 0),
                            validated_data.get('selling_price', 0))
    except ValidationError as e:
        errors.append(str(e))

    try:
        validated_data['initial_quantity'] = validate_positive_integer(initial_quantity, "Quantité initiale", allow_zero=True)
    except ValidationError as e:
        errors.append(str(e))

    try:
        validated_data['min_stock_level'] = validate_positive_integer(min_stock_level, "Stock minimum", allow_zero=True)
    except ValidationError as e:
        errors.append(str(e))

    if errors:
        raise ValidationError("; ".join(errors))

    return validated_data

def validate_vendeur_data(name, telephone=""):
    """Valide toutes les données d'un vendeur"""
    errors = []
    validated_data = {}

    try:
        validated_data['name'] = validate_vendeur_name(name)
    except ValidationError as e:
        errors.append(str(e))

    try:
        validated_data['telephone'] = validate_phone_number(telephone, required=False)
    except ValidationError as e:
        errors.append(str(e))

    if errors:
        raise ValidationError("; ".join(errors))

    return validated_data