# gestion/views/vendeur_dialog.py
"""
Boîte de dialogue pour ajouter/modifier un vendeur
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gestion.controllers.vendeur_controller import VendeurController

class VendeurDialog:
    def __init__(self, parent, vendeur_data=None, callback=None):
        """Initialise la boîte de dialogue"""
        self.parent = parent
        self.vendeur_data = vendeur_data
        self.callback = callback
        self.vendeur_controller = VendeurController()

        # Créer la fenêtre
        self.dialog = tk.Toplevel(parent)
        self.setup_dialog()
        self.create_widgets()

        # Si on modifie un vendeur, charger les données
        if vendeur_data:
            self.load_vendeur_data()

    def setup_dialog(self):
        """Configure la boîte de dialogue"""
        title = "Modifier le vendeur" if self.vendeur_data else "Nouveau vendeur"
        self.dialog.title(title)
        self.dialog.geometry("450x500")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg='#f0f0f0')

        # Centrer la fenêtre
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"450x500+{x}+{y}")

    def create_widgets(self):
        """Crée l'interface utilisateur"""
        # Frame principal
        main_frame = tk.Frame(self.dialog, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Titre
        title_text = "Modifier le vendeur" if self.vendeur_data else "Nouveau vendeur"
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

        # Nom du vendeur
        self.create_field(fields_frame, "Nom du vendeur *", 0)
        self.name_entry = tk.Entry(
            fields_frame,
            font=('Segoe UI', 12),
            relief='flat',
            bd=5,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 20), ipady=10)

        # Téléphone
        self.create_field(fields_frame, "Numéro de téléphone", 2)
        self.phone_entry = tk.Entry(
            fields_frame,
            font=('Segoe UI', 12),
            relief='flat',
            bd=5,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.phone_entry.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(0, 20), ipady=10)

        # Note d'information
        info_text = """
ℹ️ Informations sur les vendeurs :

• Le vendeur sera automatiquement activé après création
• Vous pouvez modifier le statut depuis la liste des vendeurs
• Le numéro de téléphone est optionnel mais recommandé
• Les vendeurs inactifs n'apparaissent pas dans les ventes
        """

        info_frame = tk.Frame(main_frame, bg='#e8f4fd', relief='solid', bd=1)
        info_frame.pack(fill='x', pady=(10, 20))

        info_label = tk.Label(
            info_frame,
            text=info_text.strip(),
            font=('Segoe UI', 9),
            fg='#2c3e50',
            bg='#e8f4fd',
            justify='left'
        )
        info_label.pack(padx=15, pady=15)

        # Configuration des colonnes
        fields_frame.grid_columnconfigure(0, weight=1)

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
        save_text = "Modifier" if self.vendeur_data else "Enregistrer"
        self.save_btn = tk.Button(
            buttons_frame,
            text=save_text,
            command=self.save_vendeur,
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

    def create_field(self, parent, label_text, row):
        """Crée un label de champ"""
        label = tk.Label(
            parent,
            text=label_text,
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='#f0f0f0'
        )
        label.grid(row=row, column=0, sticky='w', pady=(0, 5))

    def load_vendeur_data(self):
        """Charge les données du vendeur pour modification"""
        try:
            # Charger les données dans les champs
            self.name_entry.insert(0, self.vendeur_data['name'])
            if self.vendeur_data['telephone']:
                self.phone_entry.insert(0, self.vendeur_data['telephone'])

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données: {str(e)}")

    def save_vendeur(self):
        """Enregistre le vendeur"""
        try:
            # Récupérer les données du formulaire
            name = self.name_entry.get().strip()
            telephone = self.phone_entry.get().strip()

            # Validation de base
            if not name:
                messagebox.showerror("Erreur", "Le nom du vendeur est obligatoire")
                return

            # Désactiver le bouton pendant l'enregistrement
            self.save_btn.config(state='disabled', text='Enregistrement...')
            self.dialog.update()

            if self.vendeur_data:  # Modification
                success, message = self.vendeur_controller.update_vendeur(
                    self.vendeur_data['vendeur_id'], name, telephone
                )
            else:  # Création
                success, message = self.vendeur_controller.create_vendeur(name, telephone)

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
            save_text = "Modifier" if self.vendeur_data else "Enregistrer"
            self.save_btn.config(state='normal', text=save_text)