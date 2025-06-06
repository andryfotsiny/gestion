# create_project.py
"""
Script de création automatique de la structure du projet COMPLÈTE
Commande à exécuter: python create_project.py
Crée tous les dossiers et fichiers vides nécessaires
"""

import os

def create_project_structure():
    """Crée toute la structure de fichiers et dossiers du projet"""

    # Structure des dossiers
    folders = [
        "gestion",
        "gestion/models",
        "gestion/views",
        "gestion/controllers",
        "gestion/database",
        "gestion/config",
        "gestion/utils",
        "gestion/assets",
        "gestion/assets/icons",
        "logs"
    ]

    # Liste de tous les fichiers à créer (vides)
    files_to_create = [
        # Fichier principal
        "main.py",

        # Fichiers __init__.py pour les packages Python
        "gestion/__init__.py",
        "gestion/models/__init__.py",
        "gestion/views/__init__.py",
        "gestion/controllers/__init__.py",
        "gestion/database/__init__.py",
        "gestion/config/__init__.py",
        "gestion/utils/__init__.py",

        # Base de données
        "gestion/database/database_manager.py",

        # Modèles
        "gestion/models/user_model.py",
        "gestion/models/product_model.py",
        "gestion/models/vendeur_model.py",
        "gestion/models/category_model.py",

        # Contrôleurs
        "gestion/controllers/auth_controller.py",
        "gestion/controllers/product_controller.py",
        "gestion/controllers/vendeur_controller.py",
        "gestion/controllers/category_controller.py",

        # Vues
        "gestion/views/login_view.py",
        "gestion/views/main_view.py",
        "gestion/views/product_dialog.py",
        "gestion/views/stock_dialog.py",
        "gestion/views/vendeur_dialog.py",
        "gestion/views/category_dialog.py",
        "gestion/views/sales_view.py",
        "gestion/views/reports_view.py",

        # Configuration et utilitaires
        "gestion/config/config.py",
        "gestion/utils/helpers.py",
        "gestion/utils/validators.py",
        "gestion/utils/exporters.py",

        # Fichiers de documentation
        "README.md",
        "requirements.txt",
        ".gitignore"
    ]

    print("🚀 Création de la structure du projet...")

    # Créer les dossiers
    print("\n📁 Création des dossiers...")
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"   ✅ {folder}/")

    # Créer tous les fichiers vides
    print("\n📄 Création des fichiers...")
    for file_path in files_to_create:
        try:
            # Créer le dossier parent si nécessaire
            parent_dir = os.path.dirname(file_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            # Créer le fichier vide
            with open(file_path, 'w', encoding='utf-8') as f:
                if file_path.endswith('.py'):
                    # Ajouter juste un commentaire avec le chemin du fichier
                    f.write(f"# {file_path}\n")
                elif file_path == "README.md":
                    f.write("# Gestion d'Inventaire\n\nApplication de gestion d'inventaire et de ventes\n")
                elif file_path == "requirements.txt":
                    f.write("# Dépendances Python\n# Aucune dépendance externe requise - utilise uniquement les modules standards\n")
                elif file_path == ".gitignore":
                    f.write("__pycache__/\n*.pyc\n*.pyo\n*.db\nlogs/\n.env\n")
                else:
                    f.write("")

            print(f"   ✅ {file_path}")

        except Exception as e:
            print(f"   ❌ Erreur lors de la création de {file_path}: {e}")

    print("\n📊 Structure du projet créée:")
    print_project_structure()

def print_project_structure():
    """Affiche la structure du projet créé"""
    def print_tree(directory, prefix="", is_last=True):
        """Affiche l'arbre des fichiers et dossiers"""
        items = []
        if os.path.exists(directory):
            items = sorted(os.listdir(directory))

        for i, item in enumerate(items):
            if item.startswith('.') and item not in ['.gitignore']:
                continue

            path = os.path.join(directory, item)
            is_last_item = i == len(items) - 1

            current_prefix = "└── " if is_last_item else "├── "
            print(f"{prefix}{current_prefix}{item}")

            if os.path.isdir(path):
                extension = "    " if is_last_item else "│   "
                print_tree(path, prefix + extension, is_last_item)

    print(".")
    print_tree(".")

if __name__ == "__main__":
    create_project_structure()
    print("\n🎉 Projet créé avec succès!")
    print("\n📋 Prochaines étapes:")
    print("1. Complétez le code dans les fichiers créés")
    print("2. Lancez l'application avec: python main.py")
    print("3. Identifiant par défaut: admin / mot de passe: admin")

    print("\n📝 Fichiers principaux à compléter en priorité:")
    priority_files = [
        "main.py",
        "gestion/database/database_manager.py",
        "gestion/models/user_model.py",
        "gestion/controllers/auth_controller.py",
        "gestion/views/login_view.py",
        "gestion/views/main_view.py"
    ]

    for file in priority_files:
        print(f"   • {file}")