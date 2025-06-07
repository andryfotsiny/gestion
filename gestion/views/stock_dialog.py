# gestion/views/stock_dialog.py
"""
Boîte de dialogue pour les mouvements de stock (entrée/sortie)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gestion.controllers.product_controller import ProductController
from gestion.models.vendeur_model import VendeurModel

class StockDialog:
    def __init__(self, parent, product_id, user_data, movement_type, callback=None):
        """Initialise la boîte de dialogue"""
        self.parent = parent
        self.product_id = product_id
        self.user_data = user_data
        self.movement_type = movement_type  # 'IN' ou 'OUT'
        self.callback = callback
        self.product_controller = ProductController()
        self.vendeur_model = VendeurModel()

        # Récupérer les informations du produit
        self.product_data = self.product_controller.product_model.get_product_by_id(product_id)
        if not self.product_data:
            messagebox.showerror("Erreur", "Produit non trouvé")
            return

        # Créer la fenêtre
        self.dialog = tk.Toplevel(parent)
        self.setup_dialog()
        self.create_widgets()

    def setup_dialog(self):
        """Configure la boîte de dialogue"""
        title = "Ajouter du stock" if self.movement_type == 'IN' else "Enregistrer une vente"
        self.dialog.title(title)
        self.dialog.geometry("450x500")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg='#f0f0f0')

        # Centrer la fenêtre
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"450x500+{x}+{y}")

    def create_widgets(self):
        """Crée l'interface utilisateur"""
        # Frame principal
        main_frame = tk.Frame(self.dialog, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Titre avec icône
        if self.movement_type == 'IN':
            title_text = "📦 Ajouter du stock"
            title_color = '#27ae60'
        else:
            title_text = "💰 Enregistrer une vente"
            title_color = '#e67e22'

        title_label = tk.Label(
            main_frame,
            text=title_text,
            font=('Segoe UI', 16, 'bold'),
            fg=title_color,
            bg='#f0f0f0'
        )
        title_label.pack(pady=(0, 20))

        # Informations du produit
        product_info_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=1)
        product_info_frame.pack(fill='x', pady=(0, 20))

        info_title = tk.Label(
            product_info_frame,
            text="Informations du produit",
            font=('Segoe UI', 10, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        info_title.pack(pady=(10, 5))

        product_name = tk.Label(
            product_info_frame,
            text=f"Nom: {self.product_data['name']}",
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='white'
        )
        product_name.pack(anchor='w', padx=15, pady=2)

        category_name = tk.Label(
            product_info_frame,
            text=f"Catégorie: {self.product_data['category_name'] or 'N/A'}",
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='white'
        )
        category_name.pack(anchor='w', padx=15, pady=2)

        current_stock = tk.Label(
            product_info_frame,
            text=f"Stock actuel: {self.product_data['quantity']} unités",
            font=('Segoe UI', 9, 'bold'),
            fg='#e74c3c' if self.product_data['quantity'] <= self.product_data['min_stock_level'] else '#27ae60',
            bg='white'
        )
        current_stock.pack(anchor='w', padx=15, pady=(2, 10))

        # Frame pour les champs de saisie
        fields_frame = tk.Frame(main_frame, bg='#f0f0f0')
        fields_frame.pack(fill='x', pady=(0, 20))

        # Quantité
        qty_label = tk.Label(
            fields_frame,
            text="Quantité *",
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='#f0f0f0'
        )
        qty_label.pack(anchor='w', pady=(0, 5))

        self.quantity_entry = tk.Entry(
            fields_frame,
            font=('Segoe UI', 11),
            relief='flat',
            bd=5,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.quantity_entry.pack(fill='x', ipady=10, pady=(0, 15))

        # Prix
        price_label_text = "Prix d'achat unitaire (Ar) *" if self.movement_type == 'IN' else "Prix de vente unitaire (Ar) *"
        price_label = tk.Label(
            fields_frame,
            text=price_label_text,
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='#f0f0f0'
        )
        price_label.pack(anchor='w', pady=(0, 5))

        self.price_entry = tk.Entry(
            fields_frame,
            font=('Segoe UI', 11),
            relief='flat',
            bd=5,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.price_entry.pack(fill='x', ipady=10, pady=(0, 15))

        # Pré-remplir avec le prix par défaut
        default_price = self.product_data['purchase_price'] if self.movement_type == 'IN' else self.product_data['selling_price']
        self.price_entry.insert(0, str(default_price))

        # Vendeur (seulement pour les ventes)
        if self.movement_type == 'OUT':
            vendeur_label = tk.Label(
                fields_frame,
                text="Vendeur",
                font=('Segoe UI', 9),
                fg='#34495e',
                bg='#f0f0f0'
            )
            vendeur_label.pack(anchor='w', pady=(0, 5))

            self.vendeur_combo = ttk.Combobox(
                fields_frame,
                font=('Segoe UI', 10),
                state='readonly'
            )
            self.vendeur_combo.pack(fill='x', ipady=8, pady=(0, 15))
            self.load_vendeurs()

        # Notes
        notes_label = tk.Label(
            fields_frame,
            text="Notes (optionnel)",
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='#f0f0f0'
        )
        notes_label.pack(anchor='w', pady=(0, 5))

        self.notes_text = tk.Text(
            fields_frame,
            font=('Segoe UI', 10),
            height=3,
            relief='flat',
            bd=5,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.notes_text.pack(fill='x', pady=(0, 15))

        # Label pour le total
        self.total_label = tk.Label(
            fields_frame,
            text="",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#f0f0f0'
        )
        self.total_label.pack(pady=(5, 0))

        # Lier les événements pour calculer le total
        self.quantity_entry.bind('<KeyRelease>', self.calculate_total)
        self.price_entry.bind('<KeyRelease>', self.calculate_total)

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
        save_text = "Ajouter le stock" if self.movement_type == 'IN' else "Enregistrer la vente"
        save_color = '#27ae60' if self.movement_type == 'IN' else '#e67e22'

        self.save_btn = tk.Button(
            buttons_frame,
            text=save_text,
            command=self.save_movement,
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg=save_color,
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.save_btn.pack(side='right')

        # Effets hover
        cancel_btn.bind('<Enter>', lambda e: cancel_btn.configure(relief='raised'))
        cancel_btn.bind('<Leave>', lambda e: cancel_btn.configure(relief='solid'))

        # Focus sur le premier champ
        self.quantity_entry.focus()

    def load_vendeurs(self):
        """Charge les vendeurs actifs dans le combobox"""
        try:
            vendeurs = self.vendeur_model.get_all_vendeurs(active_only=True)
            vendeur_list = [f"{vendeur['name']}" for vendeur in vendeurs]
            self.vendeur_combo['values'] = vendeur_list

            # Stocker les IDs pour la correspondance
            self.vendeur_ids = {vendeur['name']: vendeur['vendeur_id'] for vendeur in vendeurs}

            if vendeur_list:
                self.vendeur_combo.current(0)

        except Exception as e:
            print(f"Erreur lors du chargement des vendeurs: {e}")

    def calculate_total(self, event=None):
        """Calcule et affiche le montant total"""
        try:
            quantity = float(self.quantity_entry.get() or 0)
            price = float(self.price_entry.get() or 0)
            total = quantity * price

            if total > 0:
                self.total_label.config(text=f"Total: {total:,.0f} Ar")
            else:
                self.total_label.config(text="")
        except:
            self.total_label.config(text="")

    def save_movement(self):
        """Enregistre le mouvement de stock"""
        try:
            # Récupérer les données du formulaire
            quantity = self.quantity_entry.get().strip()
            price = self.price_entry.get().strip()
            notes = self.notes_text.get("1.0", "end-1c").strip()

            # Validation de base
            if not quantity or not price:
                messagebox.showerror("Erreur", "Veuillez remplir la quantité et le prix")
                return

            # Récupérer l'ID du vendeur si c'est une vente
            vendeur_id = None
            if self.movement_type == 'OUT':
                vendeur_name = self.vendeur_combo.get()
                if vendeur_name:
                    vendeur_id = self.vendeur_ids.get(vendeur_name)

            # Désactiver le bouton pendant l'enregistrement
            self.save_btn.config(state='disabled', text='Enregistrement...')
            self.dialog.update()

            if self.movement_type == 'IN':
                success, message = self.product_controller.add_stock(
                    self.product_id, self.user_data['users_id'], quantity, price, notes
                )
            else:  # OUT
                success, message = self.product_controller.sell_product(
                    self.product_id, self.user_data['users_id'], vendeur_id, quantity, price, notes
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
            save_text = "Ajouter le stock" if self.movement_type == 'IN' else "Enregistrer la vente"
            self.save_btn.config(state='normal', text=save_text)