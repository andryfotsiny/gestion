# gestion/views/category_dialog.py
"""
Boîte de dialogue pour ajouter/modifier une catégorie
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gestion.controllers.category_controller import CategoryController

class CategoryDialog:
    def __init__(self, parent, category_data=None, callback=None):
        """Initialise la boîte de dialogue"""
        self.parent = parent
        self.category_data = category_data
        self.callback = callback
        self.category_controller = CategoryController()

        # Créer la fenêtre
        self.dialog = tk.Toplevel(parent)
        self.setup_dialog()
        self.create_widgets()

        # Si on modifie une catégorie, charger les données
        if category_data:
            self.load_category_data()

    def setup_dialog(self):
        """Configure la boîte de dialogue"""
        title = "Modifier la catégorie" if self.category_data else "Nouvelle catégorie"
        self.dialog.title(title)
        self.dialog.geometry("400x350")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg='#f0f0f0')

        # Centrer la fenêtre
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"400x350+{x}+{y}")

    def create_widgets(self):
        """Crée l'interface utilisateur"""
        # Frame principal
        main_frame = tk.Frame(self.dialog, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Titre
        title_text = "Modifier la catégorie" if self.category_data else "Nouvelle catégorie"
        title_label = tk.Label(
            main_frame,
            text=title_text,
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='#f0f0f0'
        )
        title_label.pack(pady=(0, 25))

        # Frame pour les champs
        fields_frame = tk.Frame(main_frame, bg='#f0f0f0')
        fields_frame.pack(fill='x')

        # Nom de la catégorie
        name_label = tk.Label(
            fields_frame,
            text="Nom de la catégorie *",
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='#f0f0f0'
        )
        name_label.pack(anchor='w', pady=(0, 5))

        self.name_entry = tk.Entry(
            fields_frame,
            font=('Segoe UI', 12),
            relief='flat',
            bd=5,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.name_entry.pack(fill='x', ipady=10, pady=(0, 15))

        # Exemples de catégories
        examples_label = tk.Label(
            fields_frame,
            text="Exemples de catégories :",
            font=('Segoe UI', 9, 'bold'),
            fg='#34495e',
            bg='#f0f0f0'
        )
        examples_label.pack(anchor='w', pady=(10, 5))

        examples_text = "• Boissons (Bières, Sodas, Jus)\n• Alimentaire (Snacks, Conserves)\n• Accessoires (Téléphones, Gadgets)\n• Hygiène (Savons, Produits de beauté)\n• Autres"

        examples_display = tk.Label(
            fields_frame,
            text=examples_text,
            font=('Segoe UI', 9),
            fg='#7f8c8d',
            bg='#f0f0f0',
            justify='left'
        )
        examples_display.pack(anchor='w', pady=(0, 15))

        # Note d'information
        info_frame = tk.Frame(main_frame, bg='#e8f4fd', relief='solid', bd=1)
        info_frame.pack(fill='x', pady=(10, 20))

        info_text = "ℹ️ Les catégories aident à organiser vos produits.\nVous ne pouvez pas supprimer une catégorie qui contient des produits."

        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Segoe UI', 9),
            fg='#2c3e50',
            bg='#e8f4fd',
            justify='center'
        )
        info_label.pack(padx=15, pady=10)

        # Frame pour les boutons
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', pady=(20, 0))

        # Bouton Annuler
        cancel_btn = tk.Button(
            buttons_frame,
            text="Annuler",
            command=self.dialog.destroy,
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='white',
            relief='solid',
            bd=2,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        cancel_btn.pack(side='right', padx=(10, 0))

        # Bouton Enregistrer
        save_text = "Modifier" if self.category_data else "Enregistrer"
        self.save_btn = tk.Button(
            buttons_frame,
            text=save_text,
            command=self.save_category,
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#3498db',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.save_btn.pack(side='right')

        # Effets hover pour les boutons
        cancel_btn.bind('<Enter>', lambda e: cancel_btn.configure(relief='raised'))
        cancel_btn.bind('<Leave>', lambda e: cancel_btn.configure(relief='solid'))

        self.save_btn.bind('<Enter>', lambda e: self.save_btn.configure(bg='#2980b9'))
        self.save_btn.bind('<Leave>', lambda e: self.save_btn.configure(bg='#3498db'))

        # Focus sur le champ de saisie
        self.name_entry.focus()

        # Lier la touche Entrée
        self.dialog.bind('<Return>', lambda e: self.save_category())

    def load_category_data(self):
        """Charge les données de la catégorie pour modification"""
        try:
            # Charger les données dans le champ
            self.name_entry.insert(0, self.category_data['name'])

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données: {str(e)}")

    def save_category(self):
        """Enregistre la catégorie"""
        try:
            # Récupérer les données du formulaire
            name = self.name_entry.get().strip()

            # Validation de base
            if not name:
                messagebox.showerror("Erreur", "Le nom de la catégorie est obligatoire")
                return

            # Désactiver le bouton pendant l'enregistrement
            self.save_btn.config(state='disabled', text='Enregistrement...')
            self.dialog.update()

            if self.category_data:  # Modification
                success, message = self.category_controller.update_category(
                    self.category_data['categories_id'], name
                )
            else:  # Création
                success, message = self.category_controller.create_category(name)

            if success:
                messagebox.showinfo("Succès", message)
                if self.callback:
                    self.callback()
                self.dialog.destroy()
            else:
                messagebox.showerror("Erreur", message)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue: {str(e)}")

        finally:
            # Réactiver le bouton
            save_text = "Modifier" if self.category_data else "Enregistrer"
            self.save_btn.config(state='normal', text=save_text)