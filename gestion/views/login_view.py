# gestion/views/login_view.py
"""
Interface de connexion avec design moderne - Version corrigée
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gestion.controllers.auth_controller import AuthController

class LoginView:
    def __init__(self, parent, on_success_callback):
        """Initialise l'interface de connexion"""
        self.parent = parent
        self.on_success_callback = on_success_callback
        self.auth_controller = AuthController()

        print("🔐 Création de la fenêtre de connexion...")

        # Créer la fenêtre de connexion
        self.login_window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()

        print("✅ Interface de connexion prête")

    def setup_window(self):
        """Configure la fenêtre de connexion"""
        print("⚙️ Configuration de la fenêtre...")

        self.login_window.title("Connexion - Gestion d'Inventaire")
        self.login_window.geometry("400x400")
        self.login_window.resizable(False, False)
        self.login_window.configure(bg='#f0f0f0')

        # FORCER l'affichage de la fenêtre
        self.login_window.deiconify()
        self.login_window.lift()
        self.login_window.attributes('-topmost', True)  # Toujours au premier plan
        self.login_window.focus_force()

        # Centrer sur l'écran
        self.login_window.update_idletasks()
        screen_width = self.login_window.winfo_screenwidth()
        screen_height = self.login_window.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (300 // 2)
        self.login_window.geometry(f"400x400+{x}+{y}")

        # Gérer la fermeture
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_close)

        print(f"📍 Fenêtre positionnée à {x},{y}")

    def on_close(self):
        """Gère la fermeture de la fenêtre"""
        self.parent.quit()

    def create_widgets(self):
        """Crée l'interface utilisateur moderne"""
        print("🎨 Création des widgets...")

        # Frame principal avec padding
        main_frame = tk.Frame(self.login_window, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)

        # Titre avec style moderne
        title_label = tk.Label(
            main_frame,
            text="🏪 GESTION D'INVENTAIRE",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50',
            bg='#f0f0f0'
        )
        title_label.pack(pady=(0, 30))

        # Sous-titre
        subtitle_label = tk.Label(
            main_frame,
            text="Connexion à votre compte",
            font=('Arial', 10),
            fg='#7f8c8d',
            bg='#f0f0f0'
        )
        subtitle_label.pack(pady=(0, 25))

        # Frame pour les champs de saisie
        fields_frame = tk.Frame(main_frame, bg='#f0f0f0')
        fields_frame.pack(fill='x', pady=(0, 20))

        # Champ nom d'utilisateur
        username_label = tk.Label(
            fields_frame,
            text="Nom d'utilisateur",
            font=('Arial', 9),
            fg='#34495e',
            bg='#f0f0f0'
        )
        username_label.pack(anchor='w', pady=(0, 5))

        self.username_entry = tk.Entry(
            fields_frame,
            font=('Arial', 10),
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightcolor='#3498db',
            highlightbackground='#bdc3c7'
        )
        self.username_entry.pack(fill='x', ipady=8, pady=(0, 15))
        self.username_entry.insert(0, "admin")  # Valeur par défaut

        # Champ mot de passe
        password_label = tk.Label(
            fields_frame,
            text="Mot de passe",
            font=('Arial', 9),
            fg='#34495e',
            bg='#f0f0f0'
        )
        password_label.pack(anchor='w', pady=(0, 5))

        self.password_entry = tk.Entry(
            fields_frame,
            font=('Arial', 10),
            show='*',
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightcolor='#3498db',
            highlightbackground='#bdc3c7'
        )
        self.password_entry.pack(fill='x', ipady=8)
        self.password_entry.insert(0, "admin")  # Valeur par défaut

        # Bouton de connexion avec style moderne
        self.login_button = tk.Button(
            main_frame,
            text="Se connecter",
            command=self.handle_login,
            font=('Arial', 10, 'bold'),
            fg='white',
            bg='#3498db',
            relief='flat',
            bd=0,
            cursor='hand2',
            pady=10
        )
        self.login_button.pack(fill='x', pady=(20, 10))

        # Effets hover pour le bouton
        self.login_button.bind('<Enter>', lambda e: self.login_button.configure(bg='#2980b9'))
        self.login_button.bind('<Leave>', lambda e: self.login_button.configure(bg='#3498db'))

        # Lien d'information
        info_label = tk.Label(
            main_frame,
            text="Identifiant par défaut: admin / admin",
            font=('Arial', 8),
            fg='#95a5a6',
            bg='#f0f0f0'
        )
        info_label.pack(pady=(10, 0))

        # Lier la touche Entrée à la connexion
        self.login_window.bind('<Return>', lambda e: self.handle_login())

        # Focus sur le champ nom d'utilisateur
        self.username_entry.focus()

        print("✅ Widgets créés et configurés")

    def handle_login(self):
        """Gère la tentative de connexion"""
        print("🔐 Tentative de connexion...")

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez saisir vos identifiants")
            return

        # Désactiver le bouton pendant la connexion
        self.login_button.configure(state='disabled', text='Connexion...')
        self.login_window.update()

        try:
            success, result = self.auth_controller.login(username, password)

            if success:
                print(f"✅ Connexion réussie pour {result['full_name']}")
                # Connexion réussie
                self.login_window.destroy()
                self.on_success_callback(result)
            else:
                print(f"❌ Échec de connexion: {result}")
                # Erreur de connexion
                messagebox.showerror("Erreur de connexion", result)
                self.password_entry.delete(0, 'end')
                self.password_entry.focus()

        except Exception as e:
            print(f"💥 Erreur lors de la connexion: {e}")
            messagebox.showerror("Erreur", f"Erreur inattendue: {str(e)}")

        finally:
            # Réactiver le bouton
            self.login_button.configure(state='normal', text='Se connecter')