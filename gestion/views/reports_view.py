# gestion/views/reports_view.py
"""
Interface de génération de rapports et statistiques
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import csv
import os
from gestion.controllers.product_controller import ProductController
from gestion.models.vendeur_model import VendeurModel

class ReportsView:
    def __init__(self, parent_frame, user_data):
        """Initialise la vue des rapports"""
        self.parent_frame = parent_frame
        self.user_data = user_data
        self.product_controller = ProductController()
        self.vendeur_model = VendeurModel()

        self.create_reports_interface()

    def create_reports_interface(self):
        """Crée l'interface de génération de rapports"""
        # Titre
        title_label = tk.Label(
            self.parent_frame,
            text="📑 Rapports et Statistiques",
            font=('Segoe UI', 20, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        title_label.pack(pady=(0, 20))

        # Frame principal avec deux colonnes
        main_container = tk.Frame(self.parent_frame, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True)

        # Colonne gauche - Types de rapports
        self.create_reports_types(main_container)

        # Colonne droite - Aperçu et paramètres
        self.create_preview_section(main_container)

    def create_reports_types(self, parent):
        """Crée la section des types de rapports"""
        left_frame = tk.Frame(parent, bg='#ecf0f1')
        left_frame.pack(side='left', fill='y', padx=(0, 10))

        # Titre
        types_title = tk.Label(
            left_frame,
            text="📋 Types de Rapports",
            font=('Segoe UI', 14, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        types_title.pack(pady=(0, 15))

        # Liste des types de rapports
        reports_data = [
            {
                'title': '📊 Rapport de Ventes',
                'desc': 'Analyse des ventes par période',
                'icon': '📈',
                'action': self.generate_sales_report
            },
            {
                'title': '👥 Rapport par Vendeur',
                'desc': 'Performance de chaque vendeur',
                'icon': '🏆',
                'action': self.generate_vendeur_report
            },
            {
                'title': '📦 Rapport de Stock',
                'desc': 'État actuel du stock',
                'icon': '📋',
                'action': self.generate_stock_report
            },
            {
                'title': '💰 Rapport Financier',
                'desc': 'Chiffre d\'affaires et bénéfices',
                'icon': '💵',
                'action': self.generate_financial_report
            },
            {
                'title': '📈 Mouvements de Stock',
                'desc': 'Historique des entrées/sorties',
                'icon': '🔄',
                'action': self.generate_movements_report
            },
            {
                'title': '⚠️ Alertes Stock',
                'desc': 'Produits en rupture ou faible stock',
                'icon': '🚨',
                'action': self.generate_alerts_report
            }
        ]

        # Créer les cartes de rapports
        for report in reports_data:
            self.create_report_card(left_frame, report)

    def create_report_card(self, parent, report_data):
        """Crée une carte pour un type de rapport"""
        card = tk.Frame(parent, bg='white', relief='raised', bd=1, cursor='hand2')
        card.pack(fill='x', pady=5)

        # Frame interne avec padding
        inner_frame = tk.Frame(card, bg='white')
        inner_frame.pack(fill='both', expand=True, padx=15, pady=10)

        # En-tête avec icône et titre
        header_frame = tk.Frame(inner_frame, bg='white')
        header_frame.pack(fill='x')

        icon_title = tk.Label(
            header_frame,
            text=f"{report_data['icon']} {report_data['title']}",
            font=('Segoe UI', 11, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        icon_title.pack(anchor='w')

        # Description
        desc_label = tk.Label(
            inner_frame,
            text=report_data['desc'],
            font=('Segoe UI', 9),
            fg='#7f8c8d',
            bg='white'
        )
        desc_label.pack(anchor='w', pady=(2, 0))

        # Lier le clic
        def on_click(event, action=report_data['action']):
            self.select_report_type(action, report_data['title'])

        for widget in [card, inner_frame, header_frame, icon_title, desc_label]:
            widget.bind('<Button-1>', on_click)
            widget.bind('<Enter>', lambda e, c=card: c.configure(bg='#f8f9fa'))
            widget.bind('<Leave>', lambda e, c=card: c.configure(bg='white'))

    def create_preview_section(self, parent):
        """Crée la section d'aperçu et paramètres"""
        right_frame = tk.Frame(parent, bg='#ecf0f1')
        right_frame.pack(side='right', fill='both', expand=True)

        # Titre
        preview_title = tk.Label(
            right_frame,
            text="⚙️ Paramètres du Rapport",
            font=('Segoe UI', 14, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        preview_title.pack(pady=(0, 15))

        # Frame de paramètres
        params_frame = tk.LabelFrame(
            right_frame,
            text="Paramètres",
            font=('Segoe UI', 10, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1',
            pady=10
        )
        params_frame.pack(fill='x', pady=(0, 15))

        # Paramètres de période
        period_frame = tk.Frame(params_frame, bg='#ecf0f1')
        period_frame.pack(fill='x', padx=10, pady=5)

        period_label = tk.Label(
            period_frame,
            text="Période :",
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='#ecf0f1'
        )
        period_label.pack(side='left', padx=(0, 10))

        self.period_combo = ttk.Combobox(
            period_frame,
            font=('Segoe UI', 9),
            state='readonly',
            width=20
        )
        self.period_combo['values'] = [
            "Aujourd'hui",
            "Hier",
            "7 derniers jours",
            "30 derniers jours",
            "Ce mois",
            "Mois dernier",
            "Cette année",
            "Période personnalisée"
        ]
        self.period_combo.current(2)  # 7 derniers jours par défaut
        self.period_combo.pack(side='left')

        # Format de sortie
        format_frame = tk.Frame(params_frame, bg='#ecf0f1')
        format_frame.pack(fill='x', padx=10, pady=5)

        format_label = tk.Label(
            format_frame,
            text="Format :",
            font=('Segoe UI', 9),
            fg='#34495e',
            bg='#ecf0f1'
        )
        format_label.pack(side='left', padx=(0, 10))

        self.format_combo = ttk.Combobox(
            format_frame,
            font=('Segoe UI', 9),
            state='readonly',
            width=15
        )
        self.format_combo['values'] = ["CSV", "Texte", "Affichage"]
        self.format_combo.current(0)  # CSV par défaut
        self.format_combo.pack(side='left')

        # Boutons d'action
        actions_frame = tk.Frame(right_frame, bg='#ecf0f1')
        actions_frame.pack(fill='x', pady=10)

        # Bouton Générer
        self.generate_btn = tk.Button(
            actions_frame,
            text="📊 Générer le Rapport",
            command=self.generate_selected_report,
            font=('Segoe UI', 11, 'bold'),
            fg='white',
            bg='#27ae60',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            state='disabled'
        )
        self.generate_btn.pack(side='left', padx=(0, 10))

        # Bouton Aperçu
        preview_btn = tk.Button(
            actions_frame,
            text="👁️ Aperçu",
            command=self.show_preview,
            font=('Segoe UI', 10),
            fg='#3498db',
            bg='white',
            relief='solid',
            bd=2,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        preview_btn.pack(side='left')

        # Zone d'aperçu
        preview_frame = tk.LabelFrame(
            right_frame,
            text="Aperçu",
            font=('Segoe UI', 10, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        preview_frame.pack(fill='both', expand=True, pady=(15, 0))

        # Zone de texte pour l'aperçu
        self.preview_text = tk.Text(
            preview_frame,
            font=('Courier New', 9),
            bg='white',
            fg='#2c3e50',
            relief='flat',
            wrap='none'
        )

        # Scrollbars pour l'aperçu
        preview_v_scroll = ttk.Scrollbar(preview_frame, orient='vertical', command=self.preview_text.yview)
        preview_h_scroll = ttk.Scrollbar(preview_frame, orient='horizontal', command=self.preview_text.xview)
        self.preview_text.configure(yscrollcommand=preview_v_scroll.set, xscrollcommand=preview_h_scroll.set)

        # Placement
        self.preview_text.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        preview_v_scroll.grid(row=0, column=1, sticky='ns')
        preview_h_scroll.grid(row=1, column=0, sticky='ew')

        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)

        # Variables pour le rapport sélectionné
        self.selected_report = None
        self.selected_report_title = ""

    def select_report_type(self, action, title):
        """Sélectionne un type de rapport"""
        self.selected_report = action
        self.selected_report_title = title
        self.generate_btn.config(state='normal')

        # Mettre à jour l'aperçu
        self.show_preview()

    def show_preview(self):
        """Affiche un aperçu du rapport"""
        if not self.selected_report:
            self.preview_text.delete(1.0, 'end')
            self.preview_text.insert(1.0, "Sélectionnez un type de rapport pour voir l'aperçu...")
            return

        try:
            # Générer un aperçu limité
            preview_data = self.generate_preview_data()

            # Afficher dans la zone d'aperçu
            self.preview_text.delete(1.0, 'end')
            self.preview_text.insert(1.0, preview_data)

        except Exception as e:
            self.preview_text.delete(1.0, 'end')
            self.preview_text.insert(1.0, f"Erreur lors de la génération de l'aperçu:\n{str(e)}")

    def generate_preview_data(self):
        """Génère des données d'aperçu pour le rapport sélectionné"""
        period = self.get_selected_period()

        preview = f"=== APERÇU DU RAPPORT ===\n"
        preview += f"Type: {self.selected_report_title}\n"
        preview += f"Période: {period[0]} à {period[1]}\n"
        preview += f"Généré le: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        preview += "=" * 50 + "\n\n"

        if "Ventes" in self.selected_report_title:
            preview += "Date       | Produit           | Vendeur    | Quantité | Total\n"
            preview += "-" * 60 + "\n"
            preview += "05/12/2024 | Bière Heineken    | Jean       | 10       | 100,000 Ar\n"
            preview += "05/12/2024 | Coca-Cola 1.5L    | Marie      | 5        | 25,000 Ar\n"
            preview += "..." + "\n"

        elif "Vendeur" in self.selected_report_title:
            preview += "Vendeur    | Nb Ventes | Quantité | CA Total    | Performance\n"
            preview += "-" * 55 + "\n"
            preview += "Jean       | 25        | 150      | 500,000 Ar  | Excellent\n"
            preview += "Marie      | 18        | 95       | 280,000 Ar  | Bon\n"
            preview += "..." + "\n"

        elif "Stock" in self.selected_report_title:
            preview += "Produit           | Catégorie | Stock | Stock Min | Statut\n"
            preview += "-" * 55 + "\n"
            preview += "Bière Heineken    | Boissons  | 45    | 10        | OK\n"
            preview += "Coca-Cola 1.5L    | Boissons  | 3     | 5         | FAIBLE\n"
            preview += "..." + "\n"

        preview += "\n[Aperçu limité - Le rapport complet contiendra toutes les données]"

        return preview

    def get_selected_period(self):
        """Retourne la période sélectionnée"""
        period_text = self.period_combo.get()
        today = datetime.now().date()

        if period_text == "Aujourd'hui":
            return today, today
        elif period_text == "Hier":
            yesterday = today - timedelta(days=1)
            return yesterday, yesterday
        elif period_text == "7 derniers jours":
            start = today - timedelta(days=7)
            return start, today
        elif period_text == "30 derniers jours":
            start = today - timedelta(days=30)
            return start, today
        elif period_text == "Ce mois":
            start = today.replace(day=1)
            return start, today
        else:
            return today - timedelta(days=30), today

    def generate_selected_report(self):
        """Génère le rapport sélectionné"""
        if not self.selected_report:
            messagebox.showwarning("Attention", "Veuillez sélectionner un type de rapport")
            return

        try:
            # Exécuter la fonction de génération du rapport
            self.selected_report()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération du rapport: {str(e)}")

    def generate_sales_report(self):
        """Génère le rapport de ventes avec vraies données"""
        try:
            # Récupérer les paramètres de génération
            start_date, end_date = self.get_selected_period()
            format_type = self.format_combo.get().lower()

            # Validation du format
            if format_type not in ['csv', 'txt', 'json', 'html']:
                messagebox.showerror("Erreur", "Format non supporté. Choisissez CSV, TXT, JSON ou HTML.")
                return

            # Récupérer les données de ventes réelles
            all_movements = self.product_controller.get_stock_movements()

            # Filtrer pour ne garder que les ventes (mouvement OUT)
            sales_data = [movement for movement in all_movements if movement['movement_type'] == 'OUT']

            # Appliquer les filtres de date si spécifiés
            if start_date and end_date:
                filtered_sales = []
                for sale in sales_data:
                    try:
                        # Extraire la date du mouvement
                        sale_date_str = sale['created_at'][:10]  # Format YYYY-MM-DD
                        from datetime import datetime
                        sale_date = datetime.strptime(sale_date_str, '%Y-%m-%d').date()

                        # Vérifier si la vente est dans la plage
                        if start_date <= sale_date <= end_date:
                            filtered_sales.append(sale)
                    except:
                        # En cas d'erreur de parsing de date, inclure la vente
                        filtered_sales.append(sale)

                sales_data = filtered_sales

            # Vérifier qu'il y a des données à exporter
            if not sales_data:
                messagebox.showwarning("Aucune donnée",
                                     "Aucune vente trouvée pour la période sélectionnée.")
                return

            # Préparer les données pour l'export
            formatted_sales_data = []
            total_ca = 0
            total_quantity = 0

            for sale in sales_data:
                # Calculer le total pour les statistiques
                total_ca += float(sale.get('total_amount', 0))
                total_quantity += int(sale.get('quantity', 0))

                # Formater les données pour l'export
                formatted_sale = {
                    'created_at': sale.get('created_at', ''),
                    'product_name': sale.get('product_name', 'N/A'),
                    'vendeur_name': sale.get('vendeur_name', 'N/A'),
                    'quantity': sale.get('quantity', 0),
                    'unit_price': sale.get('unit_price', 0),
                    'total_amount': sale.get('total_amount', 0),
                    'notes': sale.get('notes', '')
                }
                formatted_sales_data.append(formatted_sale)

            # Utiliser l'exporteur spécialisé
            from gestion.utils.exporters import sales_exporter

            # Générer un nom de fichier avec timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"rapport_ventes_{timestamp}"

            # Exporter selon le format choisi
            filename = sales_exporter.export_sales_report(
                formatted_sales_data,
                format_type,
                base_filename
            )

            # Afficher les statistiques dans un message de succès
            avg_sale = total_ca / len(sales_data) if sales_data else 0
            success_message = f"""📊 Rapport généré avec succès !
    
    📁 Fichier: {filename}
    📅 Période: {start_date} au {end_date}
    📈 Statistiques:
       • Nombre de ventes: {len(sales_data)}
       • Quantité totale: {total_quantity}
       • CA total: {total_ca:,.0f} Ar
       • Vente moyenne: {avg_sale:,.0f} Ar"""

            messagebox.showinfo("Succès", success_message)

            # Ouvrir le fichier automatiquement selon l'OS
            try:
                import os
                import platform

                if platform.system() == "Windows":
                    os.startfile(filename)
                elif platform.system() == "Darwin":  # macOS
                    os.system(f"open '{filename}'")
                else:  # Linux
                    os.system(f"xdg-open '{filename}'")

            except Exception as open_error:
                # Si l'ouverture automatique échoue, juste informer l'utilisateur
                messagebox.showinfo("Information",
                                  f"Rapport sauvegardé: {filename}\n"
                                  f"Vous pouvez l'ouvrir manuellement.")

        except ImportError as e:
            messagebox.showerror("Erreur",
                               f"Module manquant pour l'export: {str(e)}\n"
                               f"Vérifiez que le fichier exporters.py existe.")

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Erreur détaillée: {error_details}")  # Pour debug

            messagebox.showerror("Erreur",
                               f"Erreur lors de la génération du rapport:\n{str(e)}\n\n"
                               f"Vérifiez que tous les fichiers sont présents.")

    def generate_vendeur_report(self):
        """Génère le rapport de performance des vendeurs"""
        try:
            # Récupérer les paramètres
            start_date, end_date = self.get_selected_period()
            format_type = self.format_combo.get().lower()

            # Récupérer les statistiques des vendeurs
            vendor_stats = self.vendeur_model.get_vendeur_sales_stats(
                vendeur_id=None,
                start_date=start_date,
                end_date=end_date
            )

            if not vendor_stats:
                messagebox.showwarning("Aucune donnée",
                                     "Aucune donnée de vendeur trouvée pour la période.")
                return

            # Utiliser l'exporteur
            from gestion.utils.exporters import sales_exporter
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = sales_exporter.export_vendor_performance(
                vendor_stats,
                format_type,
                f"performance_vendeurs_{timestamp}"
            )

            messagebox.showinfo("Succès", f"Rapport vendeurs généré: {filename}")

            # Ouvrir le fichier
            try:
                import os, platform
                if platform.system() == "Windows":
                    os.startfile(filename)
                elif platform.system() == "Darwin":
                    os.system(f"open '{filename}'")
                else:
                    os.system(f"xdg-open '{filename}'")
            except:
                pass

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération: {str(e)}")

    def generate_stock_report(self):
        """Génère le rapport de stock"""
        try:
            format_type = self.format_combo.get().lower()

            # Récupérer tous les produits
            products_data = self.product_controller.get_all_products()

            if not products_data:
                messagebox.showwarning("Aucune donnée", "Aucun produit trouvé.")
                return

            # Utiliser l'exporteur d'inventaire
            from gestion.utils.exporters import inventory_exporter
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = inventory_exporter.export_stock_report(
                products_data,
                format_type,
                f"rapport_stock_{timestamp}"
            )

            messagebox.showinfo("Succès", f"Rapport de stock généré: {filename}")

            # Ouvrir le fichier
            try:
                import os, platform
                if platform.system() == "Windows":
                    os.startfile(filename)
                elif platform.system() == "Darwin":
                    os.system(f"open '{filename}'")
                else:
                    os.system(f"xdg-open '{filename}'")
            except:
                pass

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération: {str(e)}")

    def generate_alerts_report(self):
        """Génère le rapport d'alertes stock faible"""
        try:
            format_type = self.format_combo.get().lower()

            # Récupérer les produits en stock faible
            low_stock_products = self.product_controller.get_low_stock_products()

            if not low_stock_products:
                messagebox.showinfo("Information",
                                  "Aucun produit en stock faible trouvé. Excellent !")
                return

            # Utiliser l'exporteur d'inventaire
            from gestion.utils.exporters import inventory_exporter
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = inventory_exporter.export_low_stock_alert(
                low_stock_products,
                format_type,
                f"alerte_stock_{timestamp}"
            )

            messagebox.showinfo("Succès",
                              f"Rapport d'alertes généré: {filename}\n"
                              f"⚠️ {len(low_stock_products)} produit(s) en stock faible !")

            # Ouvrir le fichier
            try:
                import os, platform
                if platform.system() == "Windows":
                    os.startfile(filename)
                elif platform.system() == "Darwin":
                    os.system(f"open '{filename}'")
                else:
                    os.system(f"xdg-open '{filename}'")
            except:
                pass

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération: {str(e)}")

    def generate_financial_report(self):
        """Génère le rapport financier"""
        messagebox.showinfo("Rapport", "Génération du rapport financier...")
        # Implémenter la logique de génération

    def generate_movements_report(self):
        """Génère le rapport des mouvements"""
        messagebox.showinfo("Rapport", "Génération du rapport des mouvements...")
        # Implémenter la logique de génération

