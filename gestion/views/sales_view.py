# gestion/views/sales_view.py
"""
Interface de gestion des ventes avec filtres et statistiques
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from gestion.controllers.product_controller import ProductController
from gestion.models.vendeur_model import VendeurModel

class SalesView:
    def __init__(self, parent_frame, user_data):
        """Initialise la vue des ventes"""
        self.parent_frame = parent_frame
        self.user_data = user_data
        self.product_controller = ProductController()
        self.vendeur_model = VendeurModel()

        self.create_sales_interface()
        self.load_sales_data()

    def create_sales_interface(self):
        """Crée l'interface de gestion des ventes"""
        # Titre
        title_label = tk.Label(
            self.parent_frame,
            text="📈 Gestion des Ventes",
            font=('Segoe UI', 20, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        title_label.pack(pady=(0, 20))

        # Frame de filtres
        self.create_filters_section()

        # Frame de statistiques
        self.create_stats_section()

        # Liste des ventes
        self.create_sales_list()

    def create_filters_section(self):
        """Crée la section des filtres"""
        filters_frame = tk.LabelFrame(
            self.parent_frame,
            text="🔍 Filtres",
            font=('Segoe UI', 10, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1',
            pady=10
        )
        filters_frame.pack(fill='x', pady=(0, 15))

        # Frame interne pour l'organisation
        inner_frame = tk.Frame(filters_frame, bg='#ecf0f1')
        inner_frame.pack(fill='x', padx=10, pady=5)

        # Première ligne de filtres
        row1_frame = tk.Frame(inner_frame, bg='#ecf0f1')
        row1_frame.pack(fill='x', pady=(0, 10))

        # Filtre par date
        date_label = tk.Label(
            row1_frame,
            text="Période :",
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='#ecf0f1'
        )
        date_label.pack(side='left', padx=(0, 10))

        self.date_filter = ttk.Combobox(
            row1_frame,
            font=('Segoe UI', 9),
            state='readonly',
            width=15
        )
        self.date_filter['values'] = [
            "Aujourd'hui",
            "Hier",
            "7 derniers jours",
            "30 derniers jours",
            "Ce mois",
            "Toutes les ventes"
        ]
        self.date_filter.current(2)  # 7 derniers jours par défaut
        self.date_filter.pack(side='left', padx=(0, 20))

        # Filtre par vendeur
        vendeur_label = tk.Label(
            row1_frame,
            text="Vendeur :",
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='#ecf0f1'
        )
        vendeur_label.pack(side='left', padx=(0, 10))

        self.vendeur_filter = ttk.Combobox(
            row1_frame,
            font=('Segoe UI', 9),
            state='readonly',
            width=15
        )
        self.vendeur_filter.pack(side='left', padx=(0, 20))
        self.load_vendeurs_filter()

        # Bouton actualiser
        refresh_btn = tk.Button(
            row1_frame,
            text="🔄 Actualiser",
            command=self.load_sales_data,
            font=('Segoe UI', 9),
            fg='#3498db',
            bg='white',
            relief='solid',
            bd=1,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        refresh_btn.pack(side='left')

        # Lier les événements de changement
        self.date_filter.bind('<<ComboboxSelected>>', lambda e: self.load_sales_data())
        self.vendeur_filter.bind('<<ComboboxSelected>>', lambda e: self.load_sales_data())

    def create_stats_section(self):
        """Crée la section des statistiques"""
        stats_frame = tk.Frame(self.parent_frame, bg='#ecf0f1')
        stats_frame.pack(fill='x', pady=(0, 15))

        # Cartes de statistiques
        self.stats_cards = []
        for i in range(4):
            card = tk.Frame(stats_frame, bg='white', relief='raised', bd=1)
            card.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            stats_frame.grid_columnconfigure(i, weight=1)
            self.stats_cards.append(card)

        # Initialiser les cartes vides
        self.update_stats_display(0, 0, 0, 0)

    def create_sales_list(self):
        """Crée la liste des ventes"""
        # Frame pour la liste
        list_frame = tk.Frame(self.parent_frame, bg='white', relief='raised', bd=1)
        list_frame.pack(fill='both', expand=True)

        # En-tête
        header_frame = tk.Frame(list_frame, bg='#34495e')
        header_frame.pack(fill='x')

        header_label = tk.Label(
            header_frame,
            text="📋 Historique des Ventes",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg='#34495e',
            pady=10
        )
        header_label.pack()

        # Treeview
        columns = ('Date', 'Produit', 'Vendeur', 'Quantité', 'Prix Unit.', 'Total', 'Bénéfice')
        self.sales_tree = ttk.Treeview(list_frame, columns=columns, show='headings', style='Modern.Treeview')

        # Configuration des colonnes
        column_widths = {
            'Date': 100,
            'Produit': 200,
            'Vendeur': 120,
            'Quantité': 80,
            'Prix Unit.': 100,
            'Total': 100,
            'Bénéfice': 100
        }

        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=column_widths.get(col, 100))

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.sales_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.sales_tree.xview)
        self.sales_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Placement
        self.sales_tree.grid(row=1, column=0, sticky='nsew')
        v_scrollbar.grid(row=1, column=1, sticky='ns')
        h_scrollbar.grid(row=2, column=0, sticky='ew')

        list_frame.grid_rowconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

    def load_vendeurs_filter(self):
        """Charge les vendeurs dans le filtre"""
        try:
            vendeurs = self.vendeur_model.get_all_vendeurs()
            vendeur_list = ["Tous les vendeurs"] + [vendeur['name'] for vendeur in vendeurs]
            self.vendeur_filter['values'] = vendeur_list
            self.vendeur_filter.current(0)

            # Stocker les IDs pour la correspondance
            self.vendeur_ids = {vendeur['name']: vendeur['vendeur_id'] for vendeur in vendeurs}

        except Exception as e:
            print(f"Erreur lors du chargement des vendeurs: {e}")

    def get_date_range(self):
        """Retourne la plage de dates selon le filtre sélectionné"""
        filter_value = self.date_filter.get()
        today = datetime.now().date()

        if filter_value == "Aujourd'hui":
            return today, today
        elif filter_value == "Hier":
            yesterday = today - timedelta(days=1)
            return yesterday, yesterday
        elif filter_value == "7 derniers jours":
            start_date = today - timedelta(days=7)
            return start_date, today
        elif filter_value == "30 derniers jours":
            start_date = today - timedelta(days=30)
            return start_date, today
        elif filter_value == "Ce mois":
            start_date = today.replace(day=1)
            return start_date, today
        else:  # Toutes les ventes
            return None, None

    def get_selected_vendeur_id(self):
        """Retourne l'ID du vendeur sélectionné"""
        vendeur_name = self.vendeur_filter.get()
        if vendeur_name == "Tous les vendeurs":
            return None
        return self.vendeur_ids.get(vendeur_name)

    def load_sales_data(self):
        """Charge les données de ventes selon les filtres"""
        try:
            # Obtenir les paramètres de filtre
            start_date, end_date = self.get_date_range()
            vendeur_id = self.get_selected_vendeur_id()

            # Récupérer les mouvements de sortie (ventes)
            movements = self.product_controller.get_stock_movements()

            # Filtrer les ventes seulement
            sales = [m for m in movements if m['movement_type'] == 'OUT']

            # Appliquer les filtres
            filtered_sales = self.apply_filters(sales, start_date, end_date, vendeur_id)

            # Mettre à jour l'affichage
            self.update_sales_display(filtered_sales)
            self.calculate_and_display_stats(filtered_sales)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des ventes: {str(e)}")

    def apply_filters(self, sales, start_date, end_date, vendeur_id):
        """Applique les filtres aux ventes"""
        filtered = sales

        # Filtre par date
        if start_date and end_date:
            filtered = []
            for sale in sales:
                sale_date = datetime.strptime(sale['created_at'][:10], '%Y-%m-%d').date()
                if start_date <= sale_date <= end_date:
                    filtered.append(sale)

        # Filtre par vendeur
        if vendeur_id:
            filtered = [sale for sale in filtered if sale['vendeur_id'] == vendeur_id]

        return filtered

    def update_sales_display(self, sales):
        """Met à jour l'affichage de la liste des ventes"""
        # Vider la liste
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        # Ajouter les ventes
        for sale in sales:
            # Calculer le bénéfice (estimation basée sur la différence de prix)
            # Note: Pour un calcul précis, il faudrait stocker le prix d'achat dans les mouvements
            profit = "N/A"  # À implémenter avec plus de données

            self.sales_tree.insert('', 'end', values=(
                sale['created_at'][:10],  # Date seulement
                sale['product_name'],
                sale['vendeur_name'] or 'N/A',
                sale['quantity'],
                f"{sale['unit_price']:,.0f} Ar",
                f"{sale['total_amount']:,.0f} Ar",
                profit
            ))

    def calculate_and_display_stats(self, sales):
        """Calcule et affiche les statistiques"""
        if not sales:
            self.update_stats_display(0, 0, 0, 0)
            return

        # Calculs
        total_sales = len(sales)
        total_quantity = sum(sale['quantity'] for sale in sales)
        total_amount = sum(sale['total_amount'] for sale in sales)
        avg_sale = total_amount / total_sales if total_sales > 0 else 0

        self.update_stats_display(total_sales, total_quantity, total_amount, avg_sale)

    def update_stats_display(self, total_sales, total_quantity, total_amount, avg_sale):
        """Met à jour l'affichage des statistiques"""
        stats_data = [
            ("📊 Nb Ventes", str(total_sales), "#3498db"),
            ("📦 Quantité", str(total_quantity), "#27ae60"),
            ("💰 CA Total", f"{total_amount:,.0f} Ar", "#e67e22"),
            ("📈 Moy/Vente", f"{avg_sale:,.0f} Ar", "#9b59b6")
        ]

        for i, (card, (title, value, color)) in enumerate(zip(self.stats_cards, stats_data)):
            # Vider la carte
            for widget in card.winfo_children():
                widget.destroy()

            # Titre
            title_label = tk.Label(
                card,
                text=title,
                font=('Segoe UI', 9),
                fg='#7f8c8d',
                bg='white'
            )
            title_label.pack(pady=(10, 5))

            # Valeur
            value_label = tk.Label(
                card,
                text=value,
                font=('Segoe UI', 14, 'bold'),
                fg=color,
                bg='white'
            )
            value_label.pack(pady=(0, 10))