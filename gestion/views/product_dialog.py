# gestion/views/product_dialog.py
"""
Boîte de dialogue pour ajouter/modifier un produit
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gestion.controllers.product_controller import ProductController

class ProductDialog:
    def __init__(self, parent, category_model, product_data=None, callback=None):
        """Initialise la boîte de dialogue"""
        self.parent = parent
        self.category_model = category_model
        self.product_data = product_data
        self.callback = callback
        self.product_controller = ProductController()

        # Créer la fenêtre
        self.dialog = tk.Toplevel(parent)
        self.setup_dialog()
        self.create_widgets()

        # Si on modifie un produit, charger les données
        if product_data:
            self.load_product_data()

    def setup_dialog(self):
        """Configure la boîte de dialogue"""
        title = "Modifier le produit" if self.product_data else "Nouveau produit"
        self.dialog.title(title)
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg='#f0f0f0')

        # Centrer la fenêtre
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")

    def create_widgets(self):
        """Crée l'interface utilisateur"""
        # Frame principal
        main_frame = tk.Frame(self.dialog, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Titre
        title_text = "Modifier le produit" if self.product_data else "Nouveau produit"
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

        # Nom du produit
        self.create_field(fields_frame, "Nom du produit *", 0)
        self.name_entry = tk.Entry(
            fields_frame,
            font=('Segoe UI', 10),
            relief='flat',
            bd=5,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 15), ipady=8)

        # Catégorie
        self.create_field(fields_frame, "Catégorie *", 2)
        self.category_combo = ttk.Combobox(
            fields_frame,
            font=('Segoe UI', 10),
            state='readonly'
        )
        self.category_combo.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(0, 15), ipady=8)
        self.load_categories()

        # Prix d'achat et prix de vente sur la même ligne
        self.create_field(fields_frame, "Prix d'achat (Ar) *", 4)
        self.purchase_price_entry = tk.Entry(
            fields_frame,
            font=('Segoe UI', 10),
            relief='flat',
            bd=5,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.purchase_price_entry.grid(row=5, column=0, sticky='ew', pady=(0, 15), padx=(0, 10), ipady=8)

        self.create_field(fields_frame, "Prix de vente (Ar) *", 4, column=1)
        self.selling_price_entry = tk.Entry(
            fields_frame,
            font=('Segoe UI', 10),
            relief='flat',
            bd=5,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.selling_price_entry.grid(row=5, column=1, sticky='ew', pady=(0, 15), ipady=8)

        # Label pour la marge
        self.margin_label = tk.Label(
            fields_frame,
            text="",
            font=('Segoe UI', 9, 'italic'),
            fg='#27ae60',
            bg='#f0f0f0'
        )
        self.margin_label.grid(row=6, column=0, columnspan=2, sticky='w', pady=(0, 15))

        # Lier les événements pour calculer la marge
        self.purchase_price_entry.bind('<KeyRelease>', self.calculate_margin)
        self.selling_price_entry.bind('<KeyRelease>', self.calculate_margin)

        # Quantité initiale et stock minimum
        self.create_field(fields_frame, "Quantité initiale", 7)
        self.initial_quantity_entry = tk.Entry(
            fields_frame,
            font=('Segoe UI', 10),
            relief='flat',
            bd=5,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.initial_quantity_entry.grid(row=8, column=0, sticky='ew', pady=(0, 15), padx=(0, 10), ipady=8)
        self.initial_quantity_entry.insert(0, "0")

        self.create_field(fields_frame, "Stock minimum", 7, column=1)
        self.min_stock_entry = tk.Entry(
            fields_frame,
            font=('Segoe UI', 10),
            relief='flat',
            bd=5,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.min_stock_entry.grid(row=8, column=1, sticky='ew', pady=(0, 15), ipady=8)
        self.min_stock_entry.insert(0, "5")

        # Configuration des colonnes
        fields_frame.grid_columnconfigure(0, weight=1)
        fields_frame.grid_columnconfigure(1, weight=1)

        # Frame pour les boutons
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', pady=(30, 0))

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
        save_text = "Modifier" if self.product_data else "Enregistrer"
        self.save_btn = tk.Button(
            buttons_frame,
            text=save_text,
            command=self.save_product,
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#27ae60',
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

        self.save_btn.bind('<Enter>', lambda e: self.save_btn.configure(bg='#229954'))
        self.save_btn.bind('<Leave>', lambda e: self.save_btn.configure(bg='#27ae60'))

        # Focus sur le premier champ
        self.name_entry.focus()

    def create_field(self, parent, label_text, row, column=0):
        """Crée un label de champ"""
        label = tk.Label(
            parent,
            text=label_text,
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='#f0f0f0'
        )
        label.grid(row=row, column=column, sticky='w', pady=(0, 5))

        if column == 1:
            label.grid(padx=(10, 0))

    def load_categories(self):
        """Charge les catégories dans le combobox"""
        try:
            categories = self.category_model.get_all_categories()
            category_list = [f"{cat['name']}" for cat in categories]
            self.category_combo['values'] = category_list

            # Stocker les IDs pour la correspondance
            self.category_ids = {cat['name']: cat['categories_id'] for cat in categories}

            if category_list:
                self.category_combo.current(0)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des catégories: {str(e)}")

    def calculate_margin(self, event=None):
        """Calcule et affiche la marge bénéficiaire"""
        try:
            purchase_price = float(self.purchase_price_entry.get() or 0)
            selling_price = float(self.selling_price_entry.get() or 0)

            if purchase_price > 0:
                margin = self.product_controller.calculate_profit_margin(purchase_price, selling_price)
                profit = selling_price - purchase_price
                self.margin_label.config(
                    text=f"Marge: {margin}% | Bénéfice: {profit:,.0f} Ar",
                    fg='#27ae60' if margin > 0 else '#e74c3c'
                )
            else:
                self.margin_label.config(text="")
        except:
            self.margin_label.config(text="")

    def load_product_data(self):
        """Charge les données du produit pour modification"""
        try:
            # Charger les données dans les champs
            self.name_entry.insert(0, self.product_data['name'])
            self.purchase_price_entry.insert(0, str(self.product_data['purchase_price']))
            self.selling_price_entry.insert(0, str(self.product_data['selling_price']))
            self.min_stock_entry.delete(0, 'end')
            self.min_stock_entry.insert(0, str(self.product_data['min_stock_level']))

            # Sélectionner la catégorie
            if self.product_data['category_name']:
                category_values = list(self.category_combo['values'])
                if self.product_data['category_name'] in category_values:
                    self.category_combo.current(category_values.index(self.product_data['category_name']))

            # Calculer la marge
            self.calculate_margin()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données: {str(e)}")

    def save_product(self):
        """Enregistre le produit"""
        try:
            # Récupérer les données du formulaire
            name = self.name_entry.get().strip()
            category_name = self.category_combo.get()
            purchase_price = self.purchase_price_entry.get().strip()
            selling_price = self.selling_price_entry.get().strip()
            initial_quantity = self.initial_quantity_entry.get().strip() or "0"
            min_stock_level = self.min_stock_entry.get().strip() or "5"

            # Validation de base
            if not all([name, category_name, purchase_price, selling_price]):
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
                return

            # Obtenir l'ID de la catégorie
            category_id = self.category_ids.get(category_name)
            if not category_id:
                messagebox.showerror("Erreur", "Catégorie invalide")
                return

            # Désactiver le bouton pendant l'enregistrement
            self.save_btn.config(state='disabled', text='Enregistrement...')
            self.dialog.update()

            if self.product_data:  # Modification
                success, message = self.product_controller.update_product(
                    self.product_data['products_id'],
                    name, category_id, purchase_price, selling_price, min_stock_level
                )
            else:  # Création
                success, message = self.product_controller.create_product(
                    name, category_id, purchase_price, selling_price, initial_quantity, min_stock_level
                )

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
            save_text = "Modifier" if self.product_data else "Enregistrer"
            self.save_btn.config(state='normal', text=save_text)