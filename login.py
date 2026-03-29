"""
Module de connexion pour QueueSim Pro
"""

import tkinter as tk
from tkinter import messagebox
import json
import os
import sys

# Import du Dashboard avec gestion d'erreur
try:
    from dashboard import Dashboard
    DASHBOARD_DISPONIBLE = True
except ImportError:
    print("⚠️ Module dashboard non trouvé")
    Dashboard = None
    DASHBOARD_DISPONIBLE = False

class LoginWindow:
    """Fenêtre de connexion à l'application QueueSim Pro"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("QueueSim Pro - Connexion")
        self.root.geometry("600x750")
        self.root.minsize(500, 600)
        
        self.colors = {
            'bg_top': '#1e3a8a',
            'bg_bottom': '#020617',
            'card_bg': '#1e293b',
            'card_border': '#60a5fa',
            'input_bg': '#0f172a',
            'text_main': '#ffffff',
            'text_dim': '#94a3b8',
            'btn_blue': '#0056b3',
            'btn_hover': '#00418c'
        }

        self.users_file = 'users.json'
        self.init_users_file()
        self.user_ph = "Nom d'utilisateur"
        self.pass_ph = "Mot de passe"
        self.setup_ui()
        self.root.deiconify()

    def init_users_file(self):
        """Initialise le fichier users.json s'il n'existe pas"""
        if not os.path.exists(self.users_file):
            default_users = {
                "admin": {"password": "admin123", "nom": "Administrateur", "role": "Administrateur"},
                "user": {"password": "user123", "nom": "Utilisateur", "role": "Utilisateur"},
                "prisca": {"password": "ky2024", "nom": "KY Prisca", "role": "Développeur"}
            }
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(default_users, f, indent=4, ensure_ascii=False)
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.main_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.main_canvas.pack(fill="both", expand=True)
        self.main_canvas.bind("<Configure>", self.on_resize)

        self.card = tk.Frame(self.main_canvas, bg=self.colors['card_bg'],
                             highlightbackground=self.colors['card_border'],
                             highlightthickness=2, padx=35, pady=35)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=580)

        # Logo
        logo_container = tk.Canvas(self.card, width=100, height=100, 
                                   bg=self.colors['card_bg'], highlightthickness=0)
        logo_container.pack(pady=(20, 10))
        logo_container.create_oval(5, 5, 95, 95, outline=self.colors['card_border'], width=2)
        logo_container.create_text(50, 50, text="QS", fill="white", font=("Segoe UI", 24, "bold"))

        # Titre
        tk.Label(self.card, text="QueueSim Pro", bg=self.colors['card_bg'], 
                 fg="white", font=("Segoe UI", 20, "bold")).pack(pady=(0, 30))
        tk.Label(self.card, text="Connectez-vous pour accéder à la simulation",
                 bg=self.colors['card_bg'], fg=self.colors['text_dim'], 
                 font=("Segoe UI", 10)).pack(pady=(0, 20))

        # Champs de saisie
        self.username_entry = self.create_input("👤", self.user_ph)
        self.password_entry = self.create_input("🔒", self.pass_ph, is_password=True)

        # Options
        options_frame = tk.Frame(self.card, bg=self.colors['card_bg'])
        options_frame.pack(fill="x", pady=10)
        
        self.remember_var = tk.BooleanVar()
        tk.Checkbutton(options_frame, text="Se souvenir de moi", variable=self.remember_var,
                       bg=self.colors['card_bg'], fg=self.colors['text_dim'],
                       selectcolor=self.colors['input_bg'], font=("Segoe UI", 9), bd=0).pack(side="left")
        
        tk.Label(options_frame, text="Mot de passe oublié ?", bg=self.colors['card_bg'],
                 fg=self.colors['text_dim'], font=("Segoe UI", 9, "italic")).pack(side="right")

        # Bouton
        login_btn = tk.Button(self.card, text="SE CONNECTER", command=self.handle_login,
                              bg=self.colors['btn_blue'], fg="white", font=("Segoe UI", 12, "bold"),
                              bd=0, cursor="hand2", activebackground=self.colors['btn_hover'])
        login_btn.pack(fill="x", pady=(30, 10), ipady=12)
        
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg=self.colors['btn_hover']))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg=self.colors['btn_blue']))

        # Infos
        info_frame = tk.Frame(self.card, bg=self.colors['card_bg'])
        info_frame.pack(fill="x", pady=(20, 0))
        tk.Label(info_frame, text="Comptes de démonstration :", bg=self.colors['card_bg'],
                 fg=self.colors['text_dim'], font=("Segoe UI", 9, "bold")).pack()
        tk.Label(info_frame, text="admin / admin123 • user / user123 • prisca / ky2024",
                 bg=self.colors['card_bg'], fg=self.colors['text_dim'], 
                 font=("Segoe UI", 8)).pack()

    def create_input(self, icon, placeholder, is_password=False):
        """Crée un champ de saisie stylisé"""
        container = tk.Frame(self.card, bg=self.colors['input_bg'], padx=15, pady=12)
        container.pack(fill="x", pady=10)
        
        tk.Label(container, text=icon, bg=self.colors['input_bg'], 
                 fg="white", font=("Segoe UI", 12)).pack(side="left", padx=(0, 10))
        
        entry = tk.Entry(container, bg=self.colors['input_bg'], fg="white",
                         insertbackground="white", borderwidth=0, font=("Segoe UI", 11))
        entry.insert(0, placeholder)
        entry.pack(side="left", fill="x", expand=True)
        
        entry.bind("<FocusIn>", lambda e: self.clear_placeholder(entry, placeholder, is_password))
        entry.bind("<FocusOut>", lambda e: self.restore_placeholder(entry, placeholder, is_password))
        entry.bind("<Return>", lambda e: self.handle_login())
        
        return entry

    def clear_placeholder(self, entry, placeholder, is_password):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            if is_password:
                entry.config(show="•")

    def restore_placeholder(self, entry, placeholder, is_password):
        if not entry.get():
            if is_password:
                entry.config(show="")
            entry.insert(0, placeholder)

    def on_resize(self, event):
        """Redessine le dégradé"""
        self.main_canvas.delete("gradient")
        width, height = event.width, event.height
        for i in range(0, height, 2):
            ratio = i / height
            r = int(30 - ratio * 28)
            g = int(58 - ratio * 52)
            b = int(138 - ratio * 115)
            color = f'#{max(0,r):02x}{max(0,g):02x}{max(0,b):02x}'
            self.main_canvas.create_line(0, i, width, i, fill=color, tags="gradient")
        self.main_canvas.tag_lower("gradient")

    def handle_login(self):
        """Gère la tentative de connexion"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if username == self.user_ph or password == self.pass_ph or not username or not password:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs")
            return

        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            if username in users and users[username]['password'] == password:
                user_info = users[username]
                messagebox.showinfo("Connexion réussie", f"Bienvenue {user_info['nom']} !")
                
                self.root.destroy()
                
                if DASHBOARD_DISPONIBLE and Dashboard:
                    new_root = tk.Tk()
                    Dashboard(new_root, user_info)
                    new_root.mainloop()
                else:
                    messagebox.showerror("Erreur", "Dashboard non disponible")
            else:
                messagebox.showerror("Erreur", "Identifiants incorrects")
        except Exception as e:
            messagebox.showerror("Erreur", f"Problème technique : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()