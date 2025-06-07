# gestion/views/main_view.py
"""
Interface principale de l'application avec design moderne
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gestion.controllers.product_controller import ProductController
from gestion.controllers.auth_controller import AuthController
from gestion.models.category_model import CategoryModel
from gestion.models.vendeur_model import VendeurModel
from gestion.views.sales_view import SalesView
from gestion.views.reports_view import ReportsView
from gestion.views.vendeur_dialog import VendeurDialog
from gestion.views.category_dialog import CategoryDialog

class MainView:
    def __init__(self, parent, user_data):
        """Initialise l'interface principale"""
        self.parent = parent
        self.user_data = user_data
        self.product_controller = ProductController()
        self.auth_controller = AuthController()
        self.category_model = CategoryModel()
        self.vendeur_model = VendeurModel()

        self.setup_window()
        self.create_menu()
        self.create_main_interface()
        self.load_dashboard()

    def setup_window(self):
        """Configure la fenêtre principale"""
        self.parent.title(f"Gestion d'Inventaire - {self.user_data['full_name']}")
        self.parent.geometry("1200x700")
        self.parent.configure(bg='#ecf0f1')

        # Centrer la fenêtre
        self.parent.update_idletasks()
        x = (self.parent.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.parent.winfo_screenheight() // 2) - (700 // 2)
        self.parent.geometry(f"1200x700+{x}+{y}")

        # Style moderne pour les widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configuration des styles personnalisés
        self.configure_styles()

    def configure_styles(self):
        """Configure les styles personnalisés"""
        # Style pour les boutons outline
        self.style.configure(
            'Outline.TButton',
            relief='flat',
            borderwidth=2,
            focuscolor='none'
        )

        # Style pour les Treeview
        self.style.configure(
            'Modern.Treeview',
            background='white',
            foreground='#2c3e50',
            rowheight=25,
            fieldbackground='white'
        )

        self.style.configure(
            'Modern.Treeview.Heading',
            background='#34495e',
            foreground='white',
            font=('Segoe UI', 9, 'bold')
        )

    def create_menu(self):
        """Crée le menu principal moderne"""
        # Frame du menu avec style moderne
        menu_frame = tk.Frame(self.parent, bg='#2c3e50', height=60)
        menu_frame.pack(fill='x', side='top')
        menu_frame.pack_propagate(False)

        # Logo/Titre de l'application
        logo_frame = tk.Frame(menu_frame, bg='#2c3e50')
        logo_frame.pack(side='left', padx=20, pady=15)

        app_title = tk.Label(
            logo_frame,
            text="🏪 INVENTAIRE",
            font=('Segoe UI', 14, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        app_title.pack(side='left')

        # Boutons de navigation
        nav_frame = tk.Frame(menu_frame, bg='#2c3e50')
        nav_frame.pack(side='left', padx=50, pady=10)

        # Définir les boutons de navigation
        nav_buttons = [
            ("📊 Tableau de bord", self.load_dashboard),
            ("📦 Produits", self.load_products),
            ("📈 Ventes", self.load_sales),
            ("👥 Vendeurs", self.load_vendeurs),
            ("📑 Rapports", self.load_reports)
        ]

        self.nav_buttons = {}
        for text, command in nav_buttons:
            btn = tk.Button(
                nav_frame,
                text=text,
                command=command,
                font=('Segoe UI', 9),
                fg='white',
                bg='#34495e',
                relief='flat',
                bd=0,
                padx=15,
                pady=8,
                cursor='hand2'
            )
            btn.pack(side='left', padx=5)

            # Effets hover
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#3498db'))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg='#34495e'))

            self.nav_buttons[text] = btn

        # Section utilisateur
        user_frame = tk.Frame(menu_frame, bg='#2c3e50')
        user_frame.pack(side='right', padx=20, pady=15)

        user_label = tk.Label(
            user_frame,
            text=f"👤 {self.user_data['full_name']}",
            font=('Segoe UI', 9),
            fg='white',
            bg='#2c3e50'
        )
        user_label.pack(side='left', padx=(0, 15))

        logout_btn = tk.Button(
            user_frame,
            text="🚪 Déconnexion",
            command=self.logout,
            font=('Segoe UI', 9),
            fg='white',
            bg='#e74c3c',
            relief='flat',
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2'
        )
        logout_btn.pack(side='right')

        # Effet hover pour le bouton de déconnexion
        logout_btn.bind('<Enter>', lambda e: logout_btn.configure(bg='#c0392b'))
        logout_btn.bind('<Leave>', lambda e: logout_btn.configure(bg='#e74c3c'))

    def create_main_interface(self):
        """Crée l'interface principale"""
        # Frame principal pour le contenu
        self.main_frame = tk.Frame(self.parent, bg='#ecf0f1')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Variable pour garder une référence au contenu actuel
        self.current_content = None

    def clear_content(self):
        """Vide le contenu principal"""
        if self.current_content:
            self.current_content.destroy()

    def set_active_nav_button(self, active_text):
        """Met en surbrillance le bouton de navigation actif"""
        for text, btn in self.nav_buttons.items():
            if text == active_text:
                btn.configure(bg='#3498db')
            else:
                btn.configure(bg='#34495e')

    def load_dashboard(self):
        """Charge le tableau de bord"""
        self.clear_content()
        self.set_active_nav_button("📊 Tableau de bord")

        self.current_content = tk.Frame(self.main_frame, bg='#ecf0f1')
        self.current_content.pack(fill='both', expand=True)

        # Titre de la section
        title_label = tk.Label(
            self.current_content,
            text="📊 Tableau de bord",
            font=('Segoe UI', 20, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        title_label.pack(pady=(0, 20))

        # Frame pour les cartes de statistiques
        stats_frame = tk.Frame(self.current_content, bg='#ecf0f1')
        stats_frame.pack(fill='x', pady=(0, 20))

        try:
            # Récupérer les statistiques
            products = self.product_controller.get_all_products()
            low_stock = self.product_controller.get_low_stock_products()
            recent_movements = self.product_controller.get_stock_movements(limit=10)

            # Calculer les statistiques
            total_products = len(products)
            low_stock_count = len(low_stock)
            total_stock_value = sum(p['quantity'] * p['purchase_price'] for p in products)

            # Cartes de statistiques
            stats_data = [
                ("📦 Total Produits", str(total_products), "#3498db"),
                ("⚠️ Stock Faible", str(low_stock_count), "#e74c3c"),
                ("💰 Valeur Stock", f"{total_stock_value:,.0f} Ar", "#27ae60"),
                ("📊 Mouvements", str(len(recent_movements)), "#f39c12")
            ]

            for i, (title, value, color) in enumerate(stats_data):
                self.create_stat_card(stats_frame, title, value, color, i)

            # Section des produits en stock faible
            if low_stock:
                self.create_low_stock_section()

            # Section des mouvements récents
            if recent_movements:
                self.create_recent_movements_section(recent_movements)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement du tableau de bord: {str(e)}")

    def create_stat_card(self, parent, title, value, color, index):
        """Crée une carte de statistique"""
        card = tk.Frame(parent, bg='white', relief='raised', bd=1)
        card.grid(row=0, column=index, padx=10, pady=10, sticky='ew')
        parent.grid_columnconfigure(index, weight=1)

        # Titre de la carte
        title_label = tk.Label(
            card,
            text=title,
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='white'
        )
        title_label.pack(pady=(15, 5))

        # Valeur
        value_label = tk.Label(
            card,
            text=value,
            font=('Segoe UI', 16, 'bold'),
            fg=color,
            bg='white'
        )
        value_label.pack(pady=(0, 15))

    def create_low_stock_section(self):
        """Crée la section des produits en stock faible"""
        # Titre de section
        section_title = tk.Label(
            self.current_content,
            text="⚠️ Produits en stock faible",
            font=('Segoe UI', 14, 'bold'),
            fg='#e74c3c',
            bg='#ecf0f1'
        )
        section_title.pack(pady=(20, 10), anchor='w')

        # Frame pour la liste
        list_frame = tk.Frame(self.current_content, bg='white')
        list_frame.pack(fill='both', expand=True)

        # Treeview pour afficher les produits
        columns = ('Nom', 'Stock Actuel', 'Stock Min', 'Catégorie')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings', style='Modern.Treeview')

        # Configuration des colonnes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Placement
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Charger les données
        try:
            low_stock_products = self.product_controller.get_low_stock_products()
            for product in low_stock_products:
                tree.insert('', 'end', values=(
                    product['name'],
                    product['quantity'],
                    product['min_stock_level'],
                    product['category_name'] or 'N/A'
                ))
        except Exception as e:
            print(f"Erreur lors du chargement des produits en stock faible: {e}")

    def create_recent_movements_section(self, movements):
        """Crée la section des mouvements récents"""
        # Titre de section
        section_title = tk.Label(
            self.current_content,
            text="📊 Mouvements récents",
            font=('Segoe UI', 14, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        section_title.pack(pady=(20, 10), anchor='w')

        # Frame pour la liste
        movements_frame = tk.Frame(self.current_content, bg='white')
        movements_frame.pack(fill='x', pady=(0, 20))

        # En-têtes
        headers = ['Produit', 'Type', 'Quantité', 'Prix', 'Date']
        for i, header in enumerate(headers):
            label = tk.Label(
                movements_frame,
                text=header,
                font=('Segoe UI', 9, 'bold'),
                bg='#34495e',
                fg='white',
                pady=8
            )
            label.grid(row=0, column=i, sticky='ew')
            movements_frame.grid_columnconfigure(i, weight=1)

        # Données des mouvements
        for row, movement in enumerate(movements[:5], 1):  # Limiter à 5 mouvements
            data = [
                movement['product_name'][:20] + '...' if len(movement['product_name']) > 20 else movement['product_name'],
                '📥 Entrée' if movement['movement_type'] == 'IN' else '📤 Sortie',
                str(movement['quantity']),
                f"{movement['unit_price']:,.0f} Ar",
                movement['created_at'][:10]  # Date seulement
            ]

            for col, value in enumerate(data):
                bg_color = '#f8f9fa' if row % 2 == 0 else 'white'
                label = tk.Label(
                    movements_frame,
                    text=value,
                    font=('Segoe UI', 8),
                    bg=bg_color,
                    fg='#2c3e50',
                    pady=5
                )
                label.grid(row=row, column=col, sticky='ew')

    def load_products(self):
        """Charge la gestion des produits"""
        self.clear_content()
        self.set_active_nav_button("📦 Produits")

        self.current_content = tk.Frame(self.main_frame, bg='#ecf0f1')
        self.current_content.pack(fill='both', expand=True)

        # Titre
        title_label = tk.Label(
            self.current_content,
            text="📦 Gestion des Produits",
            font=('Segoe UI', 20, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        title_label.pack(pady=(0, 20))

        # Barre d'outils
        toolbar_frame = tk.Frame(self.current_content, bg='#ecf0f1')
        toolbar_frame.pack(fill='x', pady=(0, 15))

        # Boutons d'action avec style outline
        btn_add = tk.Button(
            toolbar_frame,
            text="+ Nouveau Produit",
            command=self.show_add_product_dialog,
            font=('Segoe UI', 9),
            fg='#27ae60',
            bg='white',
            relief='solid',
            bd=2,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_add.pack(side='left', padx=(0, 10))

        btn_stock = tk.Button(
            toolbar_frame,
            text="📦 Ajouter Stock",
            command=self.show_add_stock_dialog,
            font=('Segoe UI', 9),
            fg='#3498db',
            bg='white',
            relief='solid',
            bd=2,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_stock.pack(side='left', padx=(0, 10))

        btn_sell = tk.Button(
            toolbar_frame,
            text="💰 Vendre",
            command=self.show_sell_dialog,
            font=('Segoe UI', 9),
            fg='#e67e22',
            bg='white',
            relief='solid',
            bd=2,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_sell.pack(side='left')

        # Effets hover pour les boutons
        for btn in [btn_add, btn_stock, btn_sell]:
            btn.bind('<Enter>', lambda e, b=btn: b.configure(relief='raised'))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(relief='solid'))

        # Liste des produits
        self.create_products_list()

    def create_products_list(self):
        """Crée la liste des produits"""
        # Frame pour la liste
        list_frame = tk.Frame(self.current_content, bg='white', relief='raised', bd=1)
        list_frame.pack(fill='both', expand=True)

        # Treeview
        columns = ('ID', 'Nom', 'Catégorie', 'Prix Achat', 'Prix Vente', 'Stock', 'Stock Min')
        self.products_tree = ttk.Treeview(list_frame, columns=columns, show='headings', style='Modern.Treeview')

        # Configuration des colonnes
        column_widths = {'ID': 50, 'Nom': 200, 'Catégorie': 120, 'Prix Achat': 100, 'Prix Vente': 100, 'Stock': 80, 'Stock Min': 80}

        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=column_widths.get(col, 100))

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.products_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.products_tree.xview)
        self.products_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Placement
        self.products_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # Charger les données
        self.refresh_products_list()

    def refresh_products_list(self):
        """Actualise la liste des produits"""
        try:
            # Vider la liste
            for item in self.products_tree.get_children():
                self.products_tree.delete(item)

            # Charger les produits
            products = self.product_controller.get_all_products()

            for product in products:
                # Colorer les lignes selon le stock
                tags = []
                if product['quantity'] <= product['min_stock_level']:
                    tags = ['low_stock']

                self.products_tree.insert('', 'end', values=(
                    product['products_id'],
                    product['name'],
                    product['category_name'] or 'N/A',
                    f"{product['purchase_price']:,.0f} Ar",
                    f"{product['selling_price']:,.0f} Ar",
                    product['quantity'],
                    product['min_stock_level']
                ), tags=tags)

            # Configuration des tags
            self.products_tree.tag_configure('low_stock', background='#ffebee', foreground='#c62828')

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des produits: {str(e)}")

    def show_add_product_dialog(self):
        """Affiche la boîte de dialogue d'ajout de produit"""
        from gestion.views.product_dialog import ProductDialog
        dialog = ProductDialog(self.parent, self.category_model, callback=self.refresh_products_list)

    def show_add_stock_dialog(self):
        """Affiche la boîte de dialogue d'ajout de stock"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit")
            return

        from gestion.views.stock_dialog import StockDialog
        product_id = self.products_tree.item(selected[0])['values'][0]
        dialog = StockDialog(self.parent, product_id, self.user_data, 'IN', callback=self.refresh_products_list)

    def show_sell_dialog(self):
        """Affiche la boîte de dialogue de vente"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit")
            return

        from gestion.views.stock_dialog import StockDialog
        product_id = self.products_tree.item(selected[0])['values'][0]
        dialog = StockDialog(self.parent, product_id, self.user_data, 'OUT', callback=self.refresh_products_list)

    def load_sales(self):
        """Charge la gestion des ventes"""
        self.clear_content()
        self.set_active_nav_button("📈 Ventes")

        self.current_content = tk.Frame(self.main_frame, bg='#ecf0f1')
        self.current_content.pack(fill='both', expand=True)

        # Charger SEULEMENT la vue des ventes
        sales_view = SalesView(self.current_content, self.user_data)

    def load_vendeurs(self):
        """Charge la gestion des vendeurs"""
        self.clear_content()
        self.set_active_nav_button("👥 Vendeurs")

        self.current_content = tk.Frame(self.main_frame, bg='#ecf0f1')
        self.current_content.pack(fill='both', expand=True)

        # Titre
        title_label = tk.Label(
            self.current_content,
            text="👥 Gestion des Vendeurs",
            font=('Segoe UI', 20, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        title_label.pack(pady=(0, 20))

        # Barre d'outils
        toolbar_frame = tk.Frame(self.current_content, bg='#ecf0f1')
        toolbar_frame.pack(fill='x', pady=(0, 15))

        btn_add_vendeur = tk.Button(
            toolbar_frame,
            text="+ Nouveau Vendeur",
            command=self.show_add_vendeur_dialog,
            font=('Segoe UI', 9),
            fg='#27ae60',
            bg='white',
            relief='solid',
            bd=2,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_add_vendeur.pack(side='left', padx=(0, 10))

        btn_edit_vendeur = tk.Button(
            toolbar_frame,
            text="✏️ Modifier",
            command=self.show_edit_vendeur_dialog,
            font=('Segoe UI', 9),
            fg='#3498db',
            bg='white',
            relief='solid',
            bd=2,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_edit_vendeur.pack(side='left', padx=(0, 10))

        btn_toggle_vendeur = tk.Button(
            toolbar_frame,
            text="🔄 Activer/Désactiver",
            command=self.toggle_vendeur_status,
            font=('Segoe UI', 9),
            fg='#f39c12',
            bg='white',
            relief='solid',
            bd=2,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_toggle_vendeur.pack(side='left')

        # Effets hover pour les boutons
        for btn in [btn_add_vendeur, btn_edit_vendeur, btn_toggle_vendeur]:
            btn.bind('<Enter>', lambda e, b=btn: b.configure(relief='raised'))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(relief='solid'))

        # Liste des vendeurs
        self.create_vendeurs_list()

    def create_vendeurs_list(self):
        """Crée la liste des vendeurs"""
        # Frame pour la liste
        list_frame = tk.Frame(self.current_content, bg='white', relief='raised', bd=1)
        list_frame.pack(fill='both', expand=True)

        # Treeview
        columns = ('ID', 'Nom', 'Téléphone', 'Statut', 'Date création')
        self.vendeurs_tree = ttk.Treeview(list_frame, columns=columns, show='headings', style='Modern.Treeview')

        # Configuration des colonnes
        column_widths = {'ID': 50, 'Nom': 200, 'Téléphone': 150, 'Statut': 100, 'Date création': 120}

        for col in columns:
            self.vendeurs_tree.heading(col, text=col)
            self.vendeurs_tree.column(col, width=column_widths.get(col, 100))

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.vendeurs_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.vendeurs_tree.xview)
        self.vendeurs_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Placement
        self.vendeurs_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # Charger les données
        self.refresh_vendeurs_list()

    def refresh_vendeurs_list(self):
        """Actualise la liste des vendeurs"""
        try:
            # Vider la liste
            for item in self.vendeurs_tree.get_children():
                self.vendeurs_tree.delete(item)

            # Charger les vendeurs
            vendeurs = self.vendeur_model.get_all_vendeurs()

            for vendeur in vendeurs:
                # Statut avec émoji
                statut = "✅ Actif" if vendeur['is_active'] else "❌ Inactif"

                # Couleur selon le statut
                tags = []
                if not vendeur['is_active']:
                    tags = ['inactive']

                self.vendeurs_tree.insert('', 'end', values=(
                    vendeur['vendeur_id'],
                    vendeur['name'],
                    vendeur['telephone'] or 'N/A',
                    statut,
                    vendeur['created_at'][:10]  # Date seulement
                ), tags=tags)

            # Configuration des tags
            self.vendeurs_tree.tag_configure('inactive', background='#f8f9fa', foreground='#6c757d')

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des vendeurs: {str(e)}")

    def show_add_vendeur_dialog(self):
        """Affiche la boîte de dialogue d'ajout de vendeur"""
        dialog = VendeurDialog(self.parent, callback=self.refresh_vendeurs_list)

    def show_edit_vendeur_dialog(self):
        """Affiche la boîte de dialogue de modification de vendeur"""
        selected = self.vendeurs_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un vendeur")
            return

        # Récupérer les données du vendeur sélectionné
        vendeur_id = self.vendeurs_tree.item(selected[0])['values'][0]
        try:
            vendeur_data = self.vendeur_model.get_vendeur_by_id(vendeur_id)
            if vendeur_data:
                dialog = VendeurDialog(self.parent, vendeur_data, callback=self.refresh_vendeurs_list)
            else:
                messagebox.showerror("Erreur", "Vendeur non trouvé")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération du vendeur: {str(e)}")

    def toggle_vendeur_status(self):
        """Active/désactive un vendeur"""
        selected = self.vendeurs_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un vendeur")
            return

        vendeur_id = self.vendeurs_tree.item(selected[0])['values'][0]
        vendeur_name = self.vendeurs_tree.item(selected[0])['values'][1]

        if messagebox.askyesno("Confirmation", f"Changer le statut du vendeur '{vendeur_name}' ?"):
            try:
                from gestion.controllers.vendeur_controller import VendeurController
                vendeur_controller = VendeurController()
                success, message = vendeur_controller.toggle_vendeur_status(vendeur_id)

                if success:
                    messagebox.showinfo("Succès", message)
                    self.refresh_vendeurs_list()
                else:
                    messagebox.showerror("Erreur", message)

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du changement de statut: {str(e)}")

    def load_reports(self):
        """Charge les rapports"""
        self.clear_content()
        self.set_active_nav_button("📑 Rapports")

        self.current_content = tk.Frame(self.main_frame, bg='#ecf0f1')
        self.current_content.pack(fill='both', expand=True)

        # Charger SEULEMENT la vue des rapports
        reports_view = ReportsView(self.current_content, self.user_data)

    def logout(self):
        """Déconnecte l'utilisateur"""
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment vous déconnecter ?"):
            self.auth_controller.logout()
            self.parent.quit()