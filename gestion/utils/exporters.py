# gestion/utils/exporters.py
"""
Fonctions d'export des données vers différents formats
"""

import csv
import json
import os
from datetime import datetime
from gestion.utils.helpers import clean_filename, format_currency, format_datetime

class ExportError(Exception):
    """Exception personnalisée pour les erreurs d'export"""
    pass

class DataExporter:
    def __init__(self):
        """Initialise l'exporteur de données"""
        self.supported_formats = ['csv', 'txt', 'json', 'html']

    def export_to_csv(self, data, headers, filename, delimiter=','):
        """Exporte des données vers un fichier CSV"""
        try:
            clean_filename_str = clean_filename(filename)
            if not clean_filename_str.endswith('.csv'):
                clean_filename_str += '.csv'

            with open(clean_filename_str, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile, delimiter=delimiter)

                # Écrire les en-têtes
                writer.writerow(headers)

                # Écrire les données
                for row in data:
                    writer.writerow(row)

            return clean_filename_str

        except Exception as e:
            raise ExportError(f"Erreur lors de l'export CSV: {str(e)}")

    def export_to_txt(self, data, headers, filename, separator='\t'):
        """Exporte des données vers un fichier texte"""
        try:
            clean_filename_str = clean_filename(filename)
            if not clean_filename_str.endswith('.txt'):
                clean_filename_str += '.txt'

            with open(clean_filename_str, 'w', encoding='utf-8') as txtfile:
                # Écrire l'en-tête
                txtfile.write(separator.join(headers) + '\n')
                txtfile.write('=' * (len(separator.join(headers))) + '\n')

                # Écrire les données
                for row in data:
                    txtfile.write(separator.join(str(cell) for cell in row) + '\n')

            return clean_filename_str

        except Exception as e:
            raise ExportError(f"Erreur lors de l'export TXT: {str(e)}")

    def export_to_json(self, data, headers, filename):
        """Exporte des données vers un fichier JSON"""
        try:
            clean_filename_str = clean_filename(filename)
            if not clean_filename_str.endswith('.json'):
                clean_filename_str += '.json'

            # Convertir les données en dictionnaires
            json_data = []
            for row in data:
                row_dict = {}
                for i, header in enumerate(headers):
                    row_dict[header] = row[i] if i < len(row) else None
                json_data.append(row_dict)

            # Métadonnées
            export_info = {
                'metadata': {
                    'export_date': datetime.now().isoformat(),
                    'total_records': len(json_data),
                    'headers': headers
                },
                'data': json_data
            }

            with open(clean_filename_str, 'w', encoding='utf-8') as jsonfile:
                json.dump(export_info, jsonfile, indent=2, ensure_ascii=False, default=str)

            return clean_filename_str

        except Exception as e:
            raise ExportError(f"Erreur lors de l'export JSON: {str(e)}")

    def export_to_html(self, data, headers, filename, title="Rapport"):
        """Exporte des données vers un fichier HTML"""
        try:
            clean_filename_str = clean_filename(filename)
            if not clean_filename_str.endswith('.html'):
                clean_filename_str += '.html'

            html_content = self._generate_html_table(data, headers, title)

            with open(clean_filename_str, 'w', encoding='utf-8') as htmlfile:
                htmlfile.write(html_content)

            return clean_filename_str

        except Exception as e:
            raise ExportError(f"Erreur lors de l'export HTML: {str(e)}")

    def _generate_html_table(self, data, headers, title):
        """Génère le contenu HTML pour un tableau"""
        html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }}
        .export-info {{
            background: #e8f4f8;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
            font-size: 14px;
            color: #2c3e50;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th {{
            background-color: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #ecf0f1;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e8f4f8;
        }}
        .number {{
            text-align: right;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            font-size: 12px;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="export-info">
            📅 Généré le: {datetime.now().strftime('%d/%m/%Y à %H:%M')}<br>
            📊 Nombre d'enregistrements: {len(data)}
        </div>
        <table>
            <thead>
                <tr>
"""

        # Ajouter les en-têtes
        for header in headers:
            html += f"                    <th>{header}</th>\n"

        html += """                </tr>
            </thead>
            <tbody>
"""

        # Ajouter les données
        for row in data:
            html += "                <tr>\n"
            for i, cell in enumerate(row):
                css_class = ""
                # Détection automatique des nombres pour l'alignement
                if isinstance(cell, (int, float)) or (isinstance(cell, str) and 'Ar' in cell):
                    css_class = ' class="number"'

                html += f"                    <td{css_class}>{cell}</td>\n"
            html += "                </tr>\n"

        html += """            </tbody>
        </table>
        <div class="footer">
            Généré par le système de Gestion d'Inventaire
        </div>
    </div>
</body>
</html>
"""
        return html

# Classes spécialisées pour différents types de rapports

class SalesExporter(DataExporter):
    """Exporteur spécialisé pour les rapports de ventes"""

    def export_sales_report(self, sales_data, format_type='csv', filename=None):
        """Exporte un rapport de ventes"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"rapport_ventes_{timestamp}"

        headers = ['Date', 'Produit', 'Vendeur', 'Quantité', 'Prix Unitaire', 'Total', 'Bénéfice']

        # Formatter les données
        formatted_data = []
        for sale in sales_data:
            row = [
                format_datetime(sale.get('created_at', ''), output_format='%d/%m/%Y'),
                sale.get('product_name', 'N/A'),
                sale.get('vendeur_name', 'N/A'),
                str(sale.get('quantity', 0)),
                format_currency(sale.get('unit_price', 0)),
                format_currency(sale.get('total_amount', 0)),
                'À calculer'  # Le bénéfice nécessite plus de calculs
            ]
            formatted_data.append(row)

        return self._export_by_format(formatted_data, headers, filename, format_type, "Rapport des Ventes")

    def export_vendor_performance(self, vendor_stats, format_type='csv', filename=None):
        """Exporte les performances des vendeurs"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_vendeurs_{timestamp}"

        headers = ['Vendeur', 'Nb Ventes', 'Quantité Totale', 'CA Total', 'CA Moyen', 'Performance']

        formatted_data = []
        for vendor in vendor_stats:
            total_sales = vendor.get('total_sales', 0)
            total_transactions = vendor.get('total_transactions', 0)
            avg_sale = total_sales / total_transactions if total_transactions > 0 else 0

            # Calculer le niveau de performance
            if total_sales > 1000000:  # Plus d'1M Ar
                performance = "Excellent"
            elif total_sales > 500000:  # Plus de 500k Ar
                performance = "Très Bon"
            elif total_sales > 200000:  # Plus de 200k Ar
                performance = "Bon"
            else:
                performance = "À améliorer"

            row = [
                vendor.get('vendeur_name', 'N/A'),
                str(total_transactions),
                str(vendor.get('total_quantity_sold', 0)),
                format_currency(total_sales),
                format_currency(avg_sale),
                performance
            ]
            formatted_data.append(row)

        return self._export_by_format(formatted_data, headers, filename, format_type, "Performance des Vendeurs")

class InventoryExporter(DataExporter):
    """Exporteur spécialisé pour les rapports d'inventaire"""

    def export_stock_report(self, products_data, format_type='csv', filename=None):
        """Exporte un rapport de stock"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"rapport_stock_{timestamp}"

        headers = ['Produit', 'Catégorie', 'Stock Actuel', 'Stock Min', 'Statut', 'Valeur Stock', 'Dernière MAJ']

        formatted_data = []
        for product in products_data:
            stock_value = product.get('quantity', 0) * product.get('purchase_price', 0)

            # Déterminer le statut du stock
            if product.get('quantity', 0) == 0:
                status = "❌ Rupture"
            elif product.get('quantity', 0) <= product.get('min_stock_level', 0):
                status = "⚠️ Faible"
            else:
                status = "✅ Normal"

            row = [
                product.get('name', 'N/A'),
                product.get('category_name', 'N/A'),
                str(product.get('quantity', 0)),
                str(product.get('min_stock_level', 0)),
                status,
                format_currency(stock_value),
                format_datetime(product.get('last_updated', ''), output_format='%d/%m/%Y')
            ]
            formatted_data.append(row)

        return self._export_by_format(formatted_data, headers, filename, format_type, "Rapport de Stock")

    def export_low_stock_alert(self, low_stock_products, format_type='csv', filename=None):
        """Exporte les alertes de stock faible"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"alerte_stock_faible_{timestamp}"

        headers = ['Produit', 'Catégorie', 'Stock Actuel', 'Stock Min', 'Urgence', 'À Commander']

        formatted_data = []
        for product in low_stock_products:
            current_stock = product.get('quantity', 0)
            min_stock = product.get('min_stock_level', 0)

            # Calculer l'urgence
            if current_stock == 0:
                urgence = "🔴 CRITIQUE"
                to_order = min_stock * 2  # Commander le double du minimum
            elif current_stock <= min_stock / 2:
                urgence = "🟠 ÉLEVÉE"
                to_order = min_stock * 1.5
            else:
                urgence = "🟡 MODÉRÉE"
                to_order = min_stock

            row = [
                product.get('name', 'N/A'),
                product.get('category_name', 'N/A'),
                str(current_stock),
                str(min_stock),
                urgence,
                str(int(to_order))
            ]
            formatted_data.append(row)

        return self._export_by_format(formatted_data, headers, filename, format_type, "Alerte Stock Faible")

    def _export_by_format(self, data, headers, filename, format_type, title):
        """Exporte selon le format demandé"""
        if format_type.lower() == 'csv':
            return self.export_to_csv(data, headers, filename)
        elif format_type.lower() == 'txt':
            return self.export_to_txt(data, headers, filename)
        elif format_type.lower() == 'json':
            return self.export_to_json(data, headers, filename)
        elif format_type.lower() == 'html':
            return self.export_to_html(data, headers, filename, title)
        else:
            raise ExportError(f"Format non supporté: {format_type}")

# Fonction utilitaire pour l'export rapide
def quick_export(data, headers, filename, format_type='csv', title="Rapport"):
    """Fonction d'export rapide"""
    exporter = DataExporter()

    if format_type.lower() == 'csv':
        return exporter.export_to_csv(data, headers, filename)
    elif format_type.lower() == 'txt':
        return exporter.export_to_txt(data, headers, filename)
    elif format_type.lower() == 'json':
        return exporter.export_to_json(data, headers, filename)
    elif format_type.lower() == 'html':
        return exporter.export_to_html(data, headers, filename, title)
    else:
        raise ExportError(f"Format non supporté: {format_type}")

# Instance globale pour utilisation facile
default_exporter = DataExporter()
sales_exporter = SalesExporter()
inventory_exporter = InventoryExporter()