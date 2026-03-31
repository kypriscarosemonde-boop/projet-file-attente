"""
Module de connexion pour QueueSim Pro - Version épurée
"""

import tkinter as tk
from tkinter import messagebox
import json
import os

# Import du Dashboard avec gestion d'erreur
try:
    from dashboard import Dashboard
    DASHBOARD_DISPONIBLE = True
except ImportError:
    print("⚠️ Module dashboard non trouvé")
    Dashboard = None
    DASHBOARD_DISPONIBLE = False

class LoginWindow:
    """Fenêtre de connexion - Design épuré arrière-plan clair"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("QueueSim Pro - Connexion")
        self.root.geometry("480x600")
        self.root.minsize(420, 550)
        self.root.resizable(True, True)
        
        # Palette de couleurs sobres et élégantes
        self.colors = {
            'bg': '#f5f0e8',          # Beige clair
            'card_bg': '#ffffff',      # Blanc
            'card_border': '#e8e0d5',  # Beige moyen
            'primary': '#2c3e50',      # Bleu gris foncé
            'primary_light': '#34495e',# Bleu gris
            'text_dark': '#2c3e50',    # Bleu gris foncé
            'text_light': '#7f8c8d',   # Gris
            'input_bg': '#ffffff',     # Blanc
            'input_border': '#e9e7e5', # Beige
            'separator': '#e0d6cc'     # Beige
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Centrer la fenêtre
        self.center_window()
        
        # Charger les utilisateurs
        self.users_file = 'users.json'
        self.init_users_file()
        
        # Variables pour les placeholders
        self.username_ph = "Username"
        self.password_ph = "Password"
        
        # Créer l'interface
        self.setup_ui()
    
    def center_window(self):
        """Centrer la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def init_users_file(self):
        """Initialiser le fichier des utilisateurs"""
        if not os.path.exists(self.users_file):
            default_users = {
                "admin": {
                    "password": "admin123",
                    "nom": "Administrateur",
                    "role": "admin"
                },
                "user": {
                    "password": "user123",
                    "nom": "Utilisateur",
                    "role": "user"
                },
                "prisca": {
                    "password": "ky2024",
                    "nom": "KY Prisca",
                    "role": "Développeur"
                }
            }
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=4)
    
    def setup_ui(self):
        """Configurer l'interface de connexion"""
        
        # Carte principale
        self.card = tk.Frame(
            self.root,
            bg=self.colors['card_bg'],
            highlightbackground=self.colors['card_border'],
            highlightthickness=1
        )
        self.card.place(relx=0.5, rely=0.5, anchor='center', width=380, height=550)
        
        # ===== TITRE =====
        title = tk.Label(
            self.card,
            text="Log in",
            font=('Segoe UI', 28, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark']
        )
        title.pack(pady=(40, 10))
        
        # ===== SOUS-TITRE =====
        subtitle = tk.Label(
            self.card,
            text="Login to start all features",
            font=('Segoe UI', 11),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light']
        )
        subtitle.pack(pady=(0, 40))
        
        # ===== FORMULAIRE =====
        form_frame = tk.Frame(self.card, bg=self.colors['card_bg'])
        form_frame.pack(fill='x', padx=35)
        
        # Champ Username
        username_label = tk.Label(
            form_frame,
            text="Username",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark'],
            anchor='w'
        )
        username_label.pack(fill='x', pady=(0, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 11),
            bg=self.colors['input_bg'],
            fg=self.colors['text_dark'],
            bd=1,
            relief='solid',
            highlightbackground=self.colors['input_border'],
            highlightcolor=self.colors['primary'],
            highlightthickness=1
        )
        self.username_entry.pack(fill='x', pady=(0, 20), ipady=10)
        self.username_entry.insert(0, "admin")
        
        # Champ Password
        password_label = tk.Label(
            form_frame,
            text="Password",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark'],
            anchor='w'
        )
        password_label.pack(fill='x', pady=(0, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 11),
            bg=self.colors['input_bg'],
            fg=self.colors['text_dark'],
            bd=1,
            relief='solid',
            highlightbackground=self.colors['input_border'],
            highlightcolor=self.colors['primary'],
            highlightthickness=1,
            show="•"
        )
        self.password_entry.pack(fill='x', pady=(0, 30), ipady=10)
        self.password_entry.insert(0, "admin123")
        
        # ===== BOUTON LOGIN NOW =====
        login_btn = tk.Button(
            form_frame,
            text="Login now",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            bd=0,
            cursor='hand2',
            padx=20,
            pady=12,
            command=self.login
        )
        login_btn.pack(fill='x', pady=(0, 20))
        
        # Effet hover
        login_btn.bind('<Enter>', lambda e: login_btn.configure(bg=self.colors['primary_light']))
        login_btn.bind('<Leave>', lambda e: login_btn.configure(bg=self.colors['primary']))
        
        # ===== TEXTE DE DÉMONSTRATION =====
        demo_frame = tk.Frame(self.card, bg=self.colors['card_bg'])
        demo_frame.pack(side='bottom', fill='x', pady=30)
        
        tk.Label(
            demo_frame,
            text="📝 Comptes de démonstration :",
            font=('Segoe UI', 9),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light']
        ).pack()
        
        tk.Label(
            demo_frame,
            text="admin / admin123    •    user / user123    •    prisca / ky2024",
            font=('Segoe UI', 8),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light']
        ).pack(pady=(5, 0))
        
        # Lier la touche Entrée
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Fonction de connexion"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning(
                "Erreur",
                "Veuillez remplir tous les champs"
            )
            return
        
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if username in users and users[username]['password'] == password:
                # Connexion réussie
                self.root.destroy()
                
                # Ouvrir le tableau de bord
                dashboard_root = tk.Tk()
                dashboard_root.title(f"QueueSim Pro - {users[username]['nom']}")
                dashboard_root.geometry("1200x700")
                
                app = Dashboard(dashboard_root, users[username])
                dashboard_root.mainloop()
            else:
                messagebox.showerror(
                    "Erreur",
                    "Nom d'utilisateur ou mot de passe incorrect"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Erreur: {str(e)}"
            )

# Point d'entrée pour tester
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()