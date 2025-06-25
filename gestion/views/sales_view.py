# gestion/views/sales_view.py
"""
Interface de gestion des ventes avec filtres et statistiques - Version améliorée
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

        # Initialiser les attributs à None pour éviter les erreurs
        self.summary_tree = None
        self.sales_tree = None

        self.create_sales_interface()
        # Charger les données seulement après que l'interface soit créée
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

        # Essayer de créer le résumé des produits
        try:
            self.create_products_summary()
        except Exception as e:
            print(f"⚠️ Impossible de créer le résumé des produits: {e}")
            print("L'application continue sans cette fonctionnalité.")
            self.summary_tree = None

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

        # Nouveau filtre par produit
        product_label = tk.Label(
            row1_frame,
            text="Produit :",
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='#ecf0f1'
        )
        product_label.pack(side='left', padx=(0, 10))

        self.product_filter = ttk.Combobox(
            row1_frame,
            font=('Segoe UI', 9),
            state='readonly',
            width=20
        )
        self.product_filter.pack(side='left', padx=(0, 20))
        self.load_products_filter()

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
        self.product_filter.bind('<<ComboboxSelected>>', lambda e: self.load_sales_data())

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
        # Frame principal pour la liste et le résumé
        main_frame = tk.Frame(self.parent_frame, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, pady=(0, 10))

        # Frame pour la liste des ventes (en haut)
        list_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=1)
        list_frame.pack(fill='both', expand=True, pady=(0, 5))

        # En-tête
        header_frame = tk.Frame(list_frame, bg='#34495e')
        header_frame.pack(fill='x')

        header_label = tk.Label(
            header_frame,
            text="📋 Détail des Ventes",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg='#34495e',
            pady=10
        )
        header_label.pack()

        # Frame pour le treeview et scrollbars
        tree_frame = tk.Frame(list_frame, bg='white')
        tree_frame.pack(fill='both', expand=True)

        # Treeview avec colonnes ajustées pour mieux voir les noms de produits
        columns = ('Date', 'Produit', 'Vendeur', 'Quantité', 'Prix Unit.', 'Total')
        self.sales_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', style='Modern.Treeview')

        # Configuration des colonnes avec plus d'espace pour les produits
        column_widths = {
            'Date': 100,
            'Produit': 300,  # Plus large pour voir les noms complets
            'Vendeur': 120,
            'Quantité': 80,
            'Prix Unit.': 100,
            'Total': 120
        }

        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=column_widths.get(col, 100))

        # Scrollbars pour la liste des ventes
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.sales_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.sales_tree.xview)
        self.sales_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Placement avec pack seulement
        self.sales_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')

        # Frame pour le résumé par produit (en bas)
        summary_frame = tk.LabelFrame(
            main_frame,
            text="📦 Résumé par Produit",
            font=('Segoe UI', 10, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1',
            pady=5
        )
        summary_frame.pack(fill='x', pady=(5, 0))

        # Frame interne pour le résumé
        summary_inner_frame = tk.Frame(summary_frame, bg='#ecf0f1')
        summary_inner_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Treeview pour le résumé
        summary_columns = ('Produit', 'Quantité Totale', 'Nombre de Ventes', 'CA Total', 'Pourcentage CA')
        self.summary_tree = ttk.Treeview(summary_inner_frame, columns=summary_columns, show='headings', height=8)

        # Configuration des colonnes du résumé
        summary_widths = {
            'Produit': 250,
            'Quantité Totale': 120,
            'Nombre de Ventes': 120,
            'CA Total': 120,
            'Pourcentage CA': 100
        }

        for col in summary_columns:
            self.summary_tree.heading(col, text=col)
            self.summary_tree.column(col, width=summary_widths.get(col, 100))

        # Scrollbar pour le résumé
        summary_scrollbar = ttk.Scrollbar(summary_inner_frame, orient='vertical', command=self.summary_tree.yview)
        self.summary_tree.configure(yscrollcommand=summary_scrollbar.set)

        # Placement du résumé avec pack seulement
        self.summary_tree.pack(side='left', fill='both', expand=True)
        summary_scrollbar.pack(side='right', fill='y')



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

    def load_products_filter(self):
        """Charge les produits dans le filtre"""
        try:
            # Récupérer tous les produits qui ont été vendus
            movements = self.product_controller.get_stock_movements()
            sales = [m for m in movements if m['movement_type'] == 'OUT']

            # Extraire les noms de produits uniques
            product_names = []
            for sale in sales:
                try:
                    # Gérer les objets Row SQLite et les dictionnaires
                    if hasattr(sale, 'keys'):  # sqlite3.Row a une méthode keys()
                        product_name = sale['product_name'] if 'product_name' in sale.keys() else None
                    else:
                        product_name = sale.get('product_name')

                    if product_name and product_name not in product_names:
                        product_names.append(product_name)
                except Exception as e:
                    print(f"Erreur lors de l'extraction du nom de produit: {e}")
                    continue

            product_names.sort()
            product_list = ["Tous les produits"] + product_names
            self.product_filter['values'] = product_list
            self.product_filter.current(0)

        except Exception as e:
            print(f"Erreur lors du chargement des produits: {e}")
            # Valeurs par défaut en cas d'erreur
            self.product_filter['values'] = ["Tous les produits"]
            self.product_filter.current(0)

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

    def get_selected_product_name(self):
        """Retourne le nom du produit sélectionné"""
        product_name = self.product_filter.get()
        if product_name == "Tous les produits":
            return None
        return product_name

    def load_sales_data(self):
        """Charge les données de ventes selon les filtres"""
        try:
            # Obtenir les paramètres de filtre
            start_date, end_date = self.get_date_range()
            vendeur_id = self.get_selected_vendeur_id()
            product_name = self.get_selected_product_name()

            # Récupérer les mouvements de sortie (ventes)
            movements = self.product_controller.get_stock_movements()

            # Filtrer les ventes seulement
            sales = [m for m in movements if m['movement_type'] == 'OUT']

            # Appliquer les filtres
            filtered_sales = self.apply_filters(sales, start_date, end_date, vendeur_id, product_name)

            # Mettre à jour l'affichage
            self.update_sales_display(filtered_sales)
            self.update_products_summary(filtered_sales)
            self.calculate_and_display_stats(filtered_sales)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des ventes: {str(e)}")
            print(f"Erreur détaillée: {e}")  # Pour le débogage

    def apply_filters(self, sales, start_date, end_date, vendeur_id, product_name):
        """Applique les filtres aux ventes"""
        filtered = sales

        # Filtre par date
        if start_date and end_date:
            filtered = []
            for sale in sales:
                try:
                    # Gérer les objets Row SQLite et les dictionnaires
                    if hasattr(sale, 'keys'):
                        created_at = sale['created_at']
                    else:
                        created_at = sale.get('created_at', '')

                    sale_date = datetime.strptime(created_at[:10], '%Y-%m-%d').date()
                    if start_date <= sale_date <= end_date:
                        filtered.append(sale)
                except Exception as e:
                    print(f"Erreur lors du filtrage par date: {e}")
                    continue

        # Filtre par vendeur
        if vendeur_id:
            temp_filtered = []
            for sale in filtered:
                try:
                    if hasattr(sale, 'keys'):
                        sale_vendeur_id = sale['vendeur_id']
                    else:
                        sale_vendeur_id = sale.get('vendeur_id')

                    if sale_vendeur_id == vendeur_id:
                        temp_filtered.append(sale)
                except Exception as e:
                    print(f"Erreur lors du filtrage par vendeur: {e}")
                    continue
            filtered = temp_filtered

        # Filtre par produit
        if product_name:
            temp_filtered = []
            for sale in filtered:
                try:
                    if hasattr(sale, 'keys'):
                        sale_product_name = sale['product_name'] if 'product_name' in sale.keys() else None
                    else:
                        sale_product_name = sale.get('product_name')

                    if sale_product_name == product_name:
                        temp_filtered.append(sale)
                except Exception as e:
                    print(f"Erreur lors du filtrage par produit: {e}")
                    continue
            filtered = temp_filtered

        return filtered

    def update_sales_display(self, sales):
        """Met à jour l'affichage de la liste des ventes"""
        # Vérifier si sales_tree existe
        if not hasattr(self, 'sales_tree') or self.sales_tree is None:
            print("⚠️ sales_tree n'existe pas encore")
            return

        # Vider la liste
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        # Trier les ventes par date (plus récentes en premier)
        sorted_sales = sorted(sales, key=lambda x: x['created_at'], reverse=True)

        # Ajouter les ventes
        for sale in sorted_sales:
            # Gérer les objets Row SQLite et les dictionnaires
            try:
                # Si c'est un objet Row SQLite, accéder aux colonnes par nom
                if hasattr(sale, 'keys'):  # sqlite3.Row a une méthode keys()
                    product_name = sale['product_name'] if 'product_name' in sale.keys() else 'Produit inconnu'
                    vendeur_name = sale['vendeur_name'] if 'vendeur_name' in sale.keys() else 'N/A'
                    created_at = sale['created_at']
                    quantity = sale['quantity']
                    unit_price = sale['unit_price']
                    total_amount = sale['total_amount']
                else:
                    # Si c'est un dictionnaire
                    product_name = sale.get('product_name', 'Produit inconnu')
                    vendeur_name = sale.get('vendeur_name', 'N/A')
                    created_at = sale.get('created_at', '')
                    quantity = sale.get('quantity', 0)
                    unit_price = sale.get('unit_price', 0)
                    total_amount = sale.get('total_amount', 0)

                self.sales_tree.insert('', 'end', values=(
                    created_at[:10] if created_at else '',  # Date seulement
                    product_name,  # Nom du produit mis en évidence
                    vendeur_name,
                    quantity,
                    f"{unit_price:,.0f} Ar",
                    f"{total_amount:,.0f} Ar"
                ))
            except Exception as e:
                print(f"Erreur lors de l'affichage d'une vente: {e}")
                print(f"Type de sale: {type(sale)}")
                if hasattr(sale, 'keys'):
                    print(f"Colonnes disponibles: {list(sale.keys())}")
                continue

    def update_products_summary(self, sales):
        """Met à jour le résumé par produit"""
        # Vérifier si summary_tree existe
        if not hasattr(self, 'summary_tree') or self.summary_tree is None:
            print("⚠️ summary_tree n'existe pas encore")
            return

        # Vider le résumé
        for item in self.summary_tree.get_children():
            self.summary_tree.delete(item)

        if not sales:
            return

        # Regrouper par produit
        products_summary = {}
        total_ca = 0  # Pour calculer les pourcentages

        for sale in sales:
            try:
                # Gérer les objets Row SQLite et les dictionnaires
                if hasattr(sale, 'keys'):  # sqlite3.Row a une méthode keys()
                    product_name = sale['product_name'] if 'product_name' in sale.keys() else 'Produit inconnu'
                    quantity = sale['quantity']
                    total_amount = sale['total_amount']
                else:
                    product_name = sale.get('product_name', 'Produit inconnu')
                    quantity = sale.get('quantity', 0)
                    total_amount = sale.get('total_amount', 0)

                if product_name not in products_summary:
                    products_summary[product_name] = {
                        'total_quantity': 0,
                        'sales_count': 0,
                        'total_amount': 0
                    }

                products_summary[product_name]['total_quantity'] += quantity
                products_summary[product_name]['sales_count'] += 1
                products_summary[product_name]['total_amount'] += total_amount
                total_ca += total_amount

            except Exception as e:
                print(f"Erreur lors du traitement d'une vente pour le résumé: {e}")
                continue

        # Trier par CA total décroissant
        sorted_products = sorted(products_summary.items(),
                               key=lambda x: x[1]['total_amount'], reverse=True)

        # Ajouter au treeview avec pourcentage
        for product_name, data in sorted_products:
            percentage = (data['total_amount'] / total_ca * 100) if total_ca > 0 else 0

            self.summary_tree.insert('', 'end', values=(
                product_name,
                f"{data['total_quantity']:,}",
                data['sales_count'],
                f"{data['total_amount']:,.0f} Ar",
                f"{percentage:.1f}%"
            ))

        # Ajouter une ligne de total
        if sorted_products:
            total_quantity = sum(data['total_quantity'] for _, data in products_summary.items())
            total_sales_count = sum(data['sales_count'] for _, data in products_summary.items())

            # Ligne de séparation (vide)
            self.summary_tree.insert('', 'end', values=('', '', '', '', ''))

            # Ligne de total
            self.summary_tree.insert('', 'end', values=(
                f"🔢 TOTAL ({len(products_summary)} produits)",
                f"{total_quantity:,}",
                total_sales_count,
                f"{total_ca:,.0f} Ar",
                "100.0%"
            ))

    def calculate_and_display_stats(self, sales):
        """Calcule et affiche les statistiques"""
        if not sales:
            self.update_stats_display(0, 0, 0, 0)
            return

        # Calculs avec gestion des objets Row SQLite
        total_sales = len(sales)
        total_quantity = 0
        total_amount = 0

        for sale in sales:
            try:
                if hasattr(sale, 'keys'):
                    quantity = sale['quantity']
                    amount = sale['total_amount']
                else:
                    quantity = sale.get('quantity', 0)
                    amount = sale.get('total_amount', 0)

                total_quantity += quantity
                total_amount += amount
            except Exception as e:
                print(f"Erreur lors du calcul des statistiques: {e}")
                continue

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