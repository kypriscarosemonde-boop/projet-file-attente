"""
Tableau de bord principal de l'application - VERSION AVEC VARIABLE DISCRÈTE
Design moderne, couleurs élégantes, date en temps réel
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from simulation import SimulationFileAttente
from matplotlib import rcParams
import datetime
import warnings

# Désactiver tous les warnings matplotlib
warnings.filterwarnings('ignore', category=UserWarning)

# Configuration des polices pour les graphiques
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica']

class Dashboard:
    """Tableau de bord moderne et élégant pour la simulation"""
    
    def __init__(self, parent, user_info):
        self.parent = parent
        self.user_info = user_info
        
        # Configuration de la fenêtre
        self.parent.title(f" Pro - {user_info['nom']}")
        self.parent.geometry("1400x800")
        
        # Palette de couleurs moderne
        self.colors = {
            'bg': '#f0f2f5',
            'bg_darker': '#e4e6e9',
            'sidebar': '#093960',
            'sidebar_hover': '#6490bc',
            'primary': '#4361ee',
            'primary_light': '#6b85f5',
            'primary_dark': '#2f4b9c',
            'success': '#10b981',
            'success_light': '#6ee7b7',
            'warning': '#f59e0b',
            'warning_light': '#fcd34d',
            'danger': '#ef4444',
            'danger_light': '#fca5a5',
            'purple': '#8b5cf6',
            'pink': '#ec4899',
            'dark': '#1e293b',
            'text': '#334155',
            'text_light': '#64748b',
            'text_muted': '#94a3b8',
            'card': '#ffffff',
            'card_border': '#e2e8f0'
        }
        
        self.parent.configure(bg=self.colors['bg'])
        
        # Variables
        self.resultats = None
        self.simulation_en_cours = False
        self.historique = []
        
        # Variables pour les paramètres
        self.lambda_var = tk.DoubleVar(value=2.4)
        self.mu_var = tk.DoubleVar(value=0.5)
        self.c_var = tk.IntVar(value=5)
        self.duree_var = tk.IntVar(value=480)
        
        # Date et heure en temps réel
        self.date_var = tk.StringVar()
        self.heure_var = tk.StringVar()
        self.update_datetime()
        
        # Configuration de l'interface
        self.setup_ui()
        
    def update_datetime(self):
        """Mettre à jour la date et l'heure en temps réel"""
        now = datetime.datetime.now()
        self.date_var.set(now.strftime("%d %B %Y"))
        self.heure_var.set(now.strftime("%H:%M:%S"))
        self.parent.after(1000, self.update_datetime)
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        # Barre de navigation supérieure
        self.setup_topbar()
        
        # Conteneur principal
        main_container = tk.Frame(self.parent, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Sidebar
        self.setup_sidebar(main_container)
        
        # Contenu principal
        self.setup_main_content(main_container)
    
    def setup_topbar(self):
        """Barre de navigation supérieure"""
        topbar = tk.Frame(self.parent, bg='white', height=70)
        topbar.pack(fill='x')
        topbar.pack_propagate(False)
        
        topbar.configure(highlightbackground=self.colors['card_border'], 
                        highlightthickness=1)
        
        # Logo et titre
        title_frame = tk.Frame(topbar, bg='white')
        title_frame.pack(side='left', padx=25)
        
        # Logo
        logo_frame = tk.Frame(title_frame, bg=self.colors['primary'], 
                              width=40, height=40, relief='flat')
        logo_frame.pack(side='left', padx=(0, 15))
        logo_frame.pack_propagate(False)
        
        tk.Label(
            logo_frame,
            text="QS",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(expand=True)
        
        # Titre
        tk.Label(
            title_frame,
            text="QueueSim",
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg=self.colors['dark']
        ).pack(side='left')
        
        tk.Label(
            title_frame,
            text="Pro",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg=self.colors['primary']
        ).pack(side='left')
        
        # Badge version
        version_badge = tk.Frame(title_frame, bg=self.colors['success'], 
                                  padx=8, pady=2)
        version_badge.pack(side='left', padx=(15, 0))
        
        tk.Label(
            version_badge,
            text="v2.0",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['success'],
            fg='white'
        ).pack()
        
        # Profil utilisateur
        profile_frame = tk.Frame(topbar, bg='white')
        profile_frame.pack(side='right', padx=25)
        
        # Date et heure
        datetime_frame = tk.Frame(profile_frame, bg='white')
        datetime_frame.pack(side='left', padx=(0, 20))
        
        tk.Label(
            datetime_frame,
            textvariable=self.date_var,
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['text_light']
        ).pack(anchor='e')
        
        time_frame = tk.Frame(datetime_frame, bg=self.colors['bg'], 
                              padx=8, pady=2)
        time_frame.pack(anchor='e', pady=(2, 0))
        
        tk.Label(
            time_frame,
            text="🕐",
            font=('Segoe UI', 10),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        ).pack(side='left', padx=(0, 5))
        
        tk.Label(
            time_frame,
            textvariable=self.heure_var,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        ).pack(side='left')
        
        # Séparateur
        ttk.Separator(profile_frame, orient='vertical').pack(side='left', fill='y', padx=15)
        
        # Avatar
        avatar_frame = tk.Frame(profile_frame, bg='white')
        avatar_frame.pack(side='left')
        
        avatar_canvas = tk.Canvas(avatar_frame, width=45, height=45, 
                                   bg='white', highlightthickness=0)
        avatar_canvas.pack(side='left', padx=(0, 10))
        
        avatar_canvas.create_oval(0, 0, 45, 45, 
                                   fill=self.colors['primary'],
                                   outline=self.colors['primary_dark'], 
                                   width=2)
        avatar_canvas.create_text(22, 22, 
                                   text=self.user_info['nom'][0].upper(),
                                   fill='white', 
                                   font=('Segoe UI', 18, 'bold'))
        
        # Info utilisateur
        info_frame = tk.Frame(avatar_frame, bg='white')
        info_frame.pack(side='left')
        
        tk.Label(
            info_frame,
            text=self.user_info['nom'],
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg=self.colors['dark']
        ).pack(anchor='w')
        
        role_frame = tk.Frame(info_frame, bg='white')
        role_frame.pack(anchor='w')
        
        status_dot = tk.Canvas(role_frame, width=8, height=8, 
                                bg='white', highlightthickness=0)
        status_dot.pack(side='left', padx=(0, 5))
        status_dot.create_oval(0, 0, 8, 8, fill=self.colors['success'], outline='')
        
        tk.Label(
            role_frame,
            text=self.user_info['role'],
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['text_light']
        ).pack(side='left')
        
        # Bouton déconnexion - PLUS VISIBLE
        logout_btn = tk.Button(
            profile_frame,
            text="🔓 DÉCONNEXION",
            font=('Segoe UI', 10, 'bold'),
            bg='#dc2626',  # Rouge vif
            fg='white',
            bd=0,
            cursor='hand2',
            padx=15,
            pady=6,
            command=self.logout
        )
        logout_btn.pack(side='left', padx=(15, 0))
        logout_btn.bind('<Enter>', lambda e: logout_btn.configure(bg='#b91c1c'))  # Rouge plus foncé au hover
        logout_btn.bind('<Leave>', lambda e: logout_btn.configure(bg='#dc2626'))
    
    def setup_sidebar(self, parent):
        """Sidebar avec menu"""
        sidebar = tk.Frame(
            parent,
            bg=self.colors['sidebar'],
            width=260
        )
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        tk.Frame(sidebar, bg=self.colors['sidebar'], height=20).pack()
        
        menu_items = [
            ("🏠 Tableau de bord", self.show_dashboard, True),
            ("📊 Simulation", self.show_simulation, False),
            ("📈 Historique", self.show_history, False),
            ("❓ Aide", self.show_help, False)
        ]
        
        for text, command, active in menu_items:
            btn_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
            btn_frame.pack(fill='x', pady=2)
            
            if active:
                indicator = tk.Frame(btn_frame, bg=self.colors['primary'], width=4)
                indicator.pack(side='left', fill='y')
            
            btn = tk.Button(
                btn_frame,
                text=text,
                font=('Segoe UI', 11),
                bg=self.colors['sidebar'],
                fg='white' if not active else self.colors['primary'],
                bd=0,
                cursor='hand2',
                anchor='w',
                command=command
            )
            btn.pack(side='left', fill='x', expand=True, 
                    padx=(15 if not active else 0, 15), pady=8)
            
            btn.bind('<Enter>', lambda e, b=btn: self.on_menu_hover(b, True))
            btn.bind('<Leave>', lambda e, b=btn: self.on_menu_hover(b, False))
        
        # Séparateur
        separator = tk.Frame(sidebar, bg=self.colors['sidebar'], height=2)
        separator.pack(fill='x', padx=20, pady=20)
        
        # Bas de page
        bottom_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        bottom_frame.pack(side='bottom', fill='x', pady=20)
        
        sim_count = len(self.historique)
        stats_frame = tk.Frame(bottom_frame, bg=self.colors['sidebar'])
        stats_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(
            stats_frame,
            text="📊 Simulations",
            font=('Segoe UI', 9),
            bg=self.colors['sidebar'],
            fg=self.colors['text_muted']
        ).pack(side='left')
        
        tk.Label(
            stats_frame,
            text=str(sim_count),
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['sidebar'],
            fg=self.colors['primary']
        ).pack(side='right')
        
        tk.Label(
            bottom_frame,
            text="designed by QueueSim Pro",
            font=('Segoe UI', 8),
            bg=self.colors['sidebar'],
            fg=self.colors['text_muted']
        ).pack(pady=(10, 0))
    
    def on_menu_hover(self, button, is_hover):
        """Effet hover pour les menus"""
        if is_hover:
            if button['fg'] != self.colors['primary']:
                button.configure(bg=self.colors['sidebar_hover'])
        else:
            if button['fg'] != self.colors['primary']:
                button.configure(bg=self.colors['sidebar'])
    
    def setup_main_content(self, parent):
        """Contenu principal"""
        self.main_content = tk.Frame(parent, bg=self.colors['bg'])
        self.main_content.pack(side='left', fill='both', expand=True, padx=20)
        
        self.show_dashboard()
    
    def clear_main_content(self):
        """Effacer le contenu principal"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Afficher le tableau de bord"""
        self.clear_main_content()
        
        # En-tête
        header_frame = tk.Frame(self.main_content, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        title_frame.pack(side='left')
        
        tk.Label(
            title_frame,
            text="📊",
            font=('Segoe UI', 28),
            bg=self.colors['bg']
        ).pack(side='left', padx=(0, 10))
        
        tk.Label(
            title_frame,
            text="Tableau de bord",
            font=('Segoe UI', 26, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['dark']
        ).pack(side='left')
        
        today_badge = tk.Frame(header_frame, bg=self.colors['primary_light'], 
                               padx=12, pady=5)
        today_badge.pack(side='right')
        
        tk.Label(
            today_badge,
            text="📅 AUJOURD'HUI",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['primary_light'],
            fg='white'
        ).pack()
        
        # Cartes de statistiques
        cards_frame = tk.Frame(self.main_content, bg=self.colors['bg'])
        cards_frame.pack(fill='x', pady=20)
        
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        # Mise à jour des statistiques si disponibles
        sims = str(len(self.historique)) if self.historique else "0"
        
        if self.resultats and self.resultats.get('temps_attente_echantillon'):
            temps_moyen = f"{self.resultats['temps_attente_moyen']:.1f} min"
            clients_servis = str(self.resultats['nb_clients_servis'])
        else:
            temps_moyen = "--"
            clients_servis = "0"
        
        stats = [
            ("Simulations", sims, self.colors['primary'], "📊", "+0%"),
            ("Temps moyen", temps_moyen, self.colors['success'], "⏱️", "-"),
            ("Clients servis", clients_servis, self.colors['warning'], "👥", "+"),
            ("Précision", "98%", self.colors['purple'], "🎯", "+2%")
        ]
        
        for i, (label, value, color, icon, trend) in enumerate(stats):
            self.create_stat_card(cards_frame, label, value, color, icon, trend, i)
        
        # Graphique
        self.create_chart()
    
    def create_stat_card(self, parent, label, value, color, icon, trend, col):
        """Créer une carte de statistique"""
        card = tk.Frame(
            parent,
            bg='white',
            highlightbackground=self.colors['card_border'],
            highlightthickness=1
        )
        card.grid(row=0, column=col, padx=10, sticky='nsew')
        
        header = tk.Frame(card, bg='white')
        header.pack(fill='x', padx=20, pady=(20, 10))
        
        icon_frame = tk.Frame(header, bg=color, width=40, height=40)
        icon_frame.pack(side='left')
        icon_frame.pack_propagate(False)
        
        tk.Label(
            icon_frame,
            text=icon,
            font=('Segoe UI', 20),
            bg=color,
            fg='white'
        ).pack(expand=True)
        
        if trend != "-":
            trend_color = self.colors['success'] if '+' in trend else self.colors['danger']
            tk.Label(
                header,
                text=trend,
                font=('Segoe UI', 11, 'bold'),
                bg='white',
                fg=trend_color
            ).pack(side='right')
        
        tk.Label(
            card,
            text=value,
            font=('Segoe UI', 32, 'bold'),
            bg='white',
            fg=color
        ).pack(pady=(5, 0))
        
        tk.Label(
            card,
            text=label,
            font=('Segoe UI', 12),
            bg='white',
            fg=self.colors['text_light']
        ).pack(pady=(0, 20))
    
    def create_chart(self):
        """Créer un graphique"""
        chart_frame = tk.Frame(self.main_content, bg='white')
        chart_frame.pack(fill='both', expand=True, pady=20)
        
        header = tk.Frame(chart_frame, bg='white')
        header.pack(fill='x', padx=25, pady=15)
        
        tk.Label(
            header,
            text="Évolution des temps d'attente",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg=self.colors['dark']
        ).pack(side='left')
        
        tk.Label(
            header,
            text="7 derniers jours",
            font=('Segoe UI', 11),
            bg='white',
            fg=self.colors['text_light']
        ).pack(side='right')
        
        fig = Figure(figsize=(12, 4.5), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        
        jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        valeurs = [2.1, 2.3, 1.9, 2.4, 3.2, 4.1, 2.8]
        
        bars = ax.bar(jours, valeurs, color=self.colors['primary'], 
                     alpha=0.8, edgecolor='white', linewidth=2)
        
        ax.axhline(y=2.5, color=self.colors['warning'], linestyle='--', 
                  linewidth=2, label='Seuil d\'alerte', alpha=0.7)
        ax.axhline(y=4.0, color=self.colors['danger'], linestyle='--', 
                  linewidth=2, label='Seuil critique', alpha=0.7)
        
        ax.set_xlabel('Jour', fontsize=11, fontweight='bold')
        ax.set_ylabel('Temps d\'attente moyen (min)', fontsize=11, fontweight='bold')
    
        ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
        ax.grid(True, alpha=0.2, linestyle='--')
        ax.set_facecolor('#f8faff')
        ax.set_ylim(0, 5)
        
        plt.setp(ax.get_xticklabels(), rotation=0, ha='center')
        
        for bar, val in zip(bars, valeurs):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{val:.1f} min', ha='center', va='bottom', 
                   fontsize=9, fontweight='bold')
        
        # Protection contre l'erreur tight_layout
        try:
            fig.tight_layout()
        except Exception:
            fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.1)
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    def show_simulation(self):
        """Afficher l'interface de simulation"""
        self.clear_main_content()
        
        # En-tête
        header_frame = tk.Frame(self.main_content, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="⚙️ Simulation M/M/c",
            font=('Segoe UI', 26, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['dark']
        ).pack(side='left')
        
        tk.Label(
            header_frame,
            text="Configuration et analyse",
            font=('Segoe UI', 12),
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        ).pack(side='right')
        
        # Frame principal
        main_frame = tk.Frame(self.main_content, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True)
        
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        
        # Panneau paramètres
        self.create_params_panel(main_frame).grid(row=0, column=0, padx=(0, 10), sticky='nsew')
        
        # Panneau résultats
        self.create_results_panel(main_frame).grid(row=0, column=1, padx=(10, 0), sticky='nsew')
    
    def create_params_panel(self, parent):
        """Panneau de paramètres"""
        frame = tk.Frame(
            parent,
            bg='white',
            highlightbackground=self.colors['card_border'],
            highlightthickness=1
        )
        
        # En-tête
        header = tk.Frame(frame, bg=self.colors['primary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🔧 PARAMÈTRES",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(expand=True)
        
        # Formulaire
        form_frame = tk.Frame(frame, bg='white')
        form_frame.pack(fill='both', expand=True, padx=25, pady=20)
        
        fields = [
            ("Taux d'arrivée λ", self.lambda_var, 0.1, 10.0, 0.1, "clients/min", self.colors['primary']),
            ("Taux de service μ", self.mu_var, 0.1, 5.0, 0.1, "clients/min", self.colors['success']),
            ("Nombre de caisses c", self.c_var, 1, 30, 1, "caisses", self.colors['warning']),
            ("Durée de simulation", self.duree_var, 60, 1440, 60, "minutes", self.colors['purple'])
        ]
        
        for i, (label, var, min_val, max_val, inc, unit, color) in enumerate(fields):
            field_container = tk.Frame(form_frame, bg='white')
            field_container.pack(fill='x', pady=(15 if i > 0 else 5, 5))
            
            label_frame = tk.Frame(field_container, bg='white')
            label_frame.pack(fill='x')
            
            indicator = tk.Frame(label_frame, bg=color, width=4, height=16)
            indicator.pack(side='left', padx=(0, 8))
            
            tk.Label(
                label_frame,
                text=label,
                font=('Segoe UI', 11, 'bold'),
                bg='white',
                fg=self.colors['text']
            ).pack(side='left')
            
            input_frame = tk.Frame(field_container, bg='white')
            input_frame.pack(fill='x', pady=(8, 0))
            
            spinbox = tk.Spinbox(
                input_frame,
                from_=min_val,
                to=max_val,
                increment=inc,
                textvariable=var,
                font=('Segoe UI', 11),
                width=15,
                bd=1,
                relief='solid',
                bg=self.colors['bg']
            )
            spinbox.pack(side='left')
            
            tk.Label(
                input_frame,
                text=unit,
                font=('Segoe UI', 10),
                bg='white',
                fg=self.colors['text_light']
            ).pack(side='left', padx=(10, 0))
        
        # Boutons
        buttons_frame = tk.Frame(form_frame, bg='white')
        buttons_frame.pack(pady=30)
            # Largeur commune pour les deux boutons
        btn_width = 25
        
        self.simulate_btn = tk.Button(
            buttons_frame,
            text="🚀 Run",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            bd=0,
            cursor='hand2',
            padx=30,
            pady=12,
            command=self.run_simulation
        )
        self.simulate_btn.pack(side='left', padx=5)
        
        self.simulate_btn.bind('<Enter>', 
            lambda e: self.simulate_btn.configure(bg=self.colors['primary_dark']))
        self.simulate_btn.bind('<Leave>', 
            lambda e: self.simulate_btn.configure(bg=self.colors['primary']))
        
        reset_btn = tk.Button(
            buttons_frame,
            text="↺ Réinitialiser",
            font=('Segoe UI', 12),
            bg='white',
            fg=self.colors['text_light'],
            bd=1,
            relief='solid',
            cursor='hand2',
            padx=30,
            pady=12,
            command=self.reset_params
        )
        reset_btn.pack(side='left', padx=5)
        
        reset_btn.bind('<Enter>', lambda e: reset_btn.configure(bg=self.colors['bg']))
        reset_btn.bind('<Leave>', lambda e: reset_btn.configure(bg='white'))
        
        return frame
    
    def create_results_panel(self, parent):
        """Panneau de résultats avec 2 onglets principaux"""
        frame = tk.Frame(
            parent,
            bg='white',
            highlightbackground=self.colors['card_border'],
            highlightthickness=1
        )
        
        # En-tête
        header = tk.Frame(frame, bg=self.colors['success'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📊 RÉSULTATS",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['success'],
            fg='white'
        ).pack(expand=True)
        
        # Notebook avec 2 onglets principaux
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Modern.TNotebook', background='white')
        style.configure('Modern.TNotebook.Tab', 
                       font=('Segoe UI', 11),
                       padding=[20, 8])
        
        self.notebook = ttk.Notebook(frame, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ========== ONGLET 1 : CONTINUE ==========
        self.continue_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.continue_tab, text="📈 Variable Continue (Temps d'attente)")
        
        # Sous-notebook pour l'onglet Continue
        self.continue_notebook = ttk.Notebook(self.continue_tab)
        self.continue_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Graphiques Continue
        self.graph_tab = tk.Frame(self.continue_notebook, bg='white')
        self.continue_notebook.add(self.graph_tab, text="📈 Graphiques")
        
        self.fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_tab)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=15, pady=15)
        
        # Statistiques Continue
        self.stats_continue_tab = tk.Frame(self.continue_notebook, bg='white')
        self.continue_notebook.add(self.stats_continue_tab, text="📋 Statistiques")
        
        text_frame = tk.Frame(self.stats_continue_tab, bg='white')
        text_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        self.stats_text = tk.Text(
            text_frame,
            wrap='word',
            font=('Consolas', 10),
            bg='white',
            fg=self.colors['text'],
            bd=1,
            relief='solid',
            padx=15,
            pady=15
        )
        self.stats_text.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=self.stats_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.stats_text.configure(yscrollcommand=scrollbar.set)
        
        # Données brutes Continue
        self.data_tab = tk.Frame(self.continue_notebook, bg='white')
        self.continue_notebook.add(self.data_tab, text="📊 Données brutes")
        
        self.data_frame = tk.Frame(self.data_tab, bg='white')
        self.data_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # ========== ONGLET 2 : DISCRÈTE ==========
        self.discrete_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.discrete_tab, text="📊 Variable Discrète (Nombre de clients en file)")
        
        # Sous-notebook pour l'onglet Discrète
        self.discrete_notebook = ttk.Notebook(self.discrete_tab)
        self.discrete_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Graphiques Discrète
        self.discrete_graph_tab = tk.Frame(self.discrete_notebook, bg='white')
        self.discrete_notebook.add(self.discrete_graph_tab, text="📊 Graphique")
        
        self.fig_discrete = Figure(figsize=(8, 5), dpi=100, facecolor='white')
        self.canvas_discrete = FigureCanvasTkAgg(self.fig_discrete, self.discrete_graph_tab)
        self.canvas_discrete.get_tk_widget().pack(fill='both', expand=True, padx=15, pady=15)
        
        # Interprétations Discrète
        self.discrete_interpret_tab = tk.Frame(self.discrete_notebook, bg='white')
        self.discrete_notebook.add(self.discrete_interpret_tab, text="📋 Interprétations")
        
        self.discrete_interpret_text = tk.Text(
            self.discrete_interpret_tab,
            wrap='word',
            font=('Consolas', 10),
            bg='white',
            fg=self.colors['text'],
            bd=1,
            relief='solid',
            padx=15,
            pady=15
        )
        self.discrete_interpret_text.pack(fill='both', expand=True, padx=15, pady=15)
        
        return frame
    
    def display_discrete_results(self):
        """Affiche les résultats discrets - Graphique propre sans chiffres sur les barres"""
        if not self.resultats:
            return
        
        distribution = self.resultats.get('distribution_file', {})
        
        # Effacer la figure
        self.fig_discrete.clear()
        fig = self.fig_discrete
        fig.set_size_inches(8, 5)
        fig.patch.set_facecolor('white')
        
        ax = fig.add_subplot(111)
        
        # Vérifier si la distribution existe
        if not distribution or len(distribution) == 0:
            ax.text(0.5, 0.5, "⚠️ Aucune donnée discrète disponible\n\nAugmentez λ ou diminuez c\npour créer de l'attente", 
                    ha='center', va='center', fontsize=11, transform=ax.transAxes)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            self.canvas_discrete.draw()
            self.display_discrete_interpretation()
            return
        
        # Extraire les données
        k_values = list(distribution.keys())
        probas = list(distribution.values())
        
        # Diagramme en bâtons - SANS CHIFFRES SUR LES BARRES
        colors = plt.cm.Blues(np.linspace(0.5, 0.9, len(k_values)))
        bars = ax.bar(k_values, probas, color=colors, edgecolor=self.colors['primary'], 
                      linewidth=1.5, alpha=0.85, width=0.7)
        
        # Configuration des axes
        ax.set_xlabel('Nombre de clients en file d\'attente (k)', fontsize=11, fontweight='bold', labelpad=10)
        ax.set_ylabel('Probabilité P(Q = k)', fontsize=11, fontweight='bold', labelpad=10)
        ax.set_title('Distribution du nombre de clients en file d\'attente', fontsize=13, fontweight='bold', pad=12)
        ax.grid(True, alpha=0.25, axis='y', linestyle='--')
        ax.set_axisbelow(True)
        
        # Limites
        max_k = max(k_values)
        ax.set_xlim(-0.6, max_k + 0.8)
        ax.set_ylim(0, max(probas) * 1.2 if probas else 1)
        ax.set_xticks(k_values)
        ax.set_xticklabels(k_values, fontsize=10)
        ax.tick_params(axis='y', labelsize=10)
        
        # Loi de Poisson théorique
        lambda_poisson = self.resultats.get('lambda', 2.4)
        max_k_theo = max(max_k + 2, 8)
        k_theo = list(range(max_k_theo + 1))
        from math import exp, factorial
        probas_poisson = [(lambda_poisson ** k * exp(-lambda_poisson)) / factorial(k) for k in k_theo]
        
        ax.plot(k_theo, probas_poisson, 'r-', linewidth=2.5, 
                label=f'Loi de Poisson (λ={lambda_poisson:.1f})', alpha=0.8)
        ax.legend(loc='upper right', fontsize=9, frameon=True)
        
        # Zone de texte pour les statistiques (en bas à droite, propre)
        moyenne_file = self.resultats.get('moyenne_file_discrete', 0)
        variance_file = self.resultats.get('variance_file', 0)
        proba_file_vide = self.resultats.get('proba_file_vide', 0)
        
        stats_text = f"Moyenne = {moyenne_file:.3f}   |   Variance = {variance_file:.3f}   |   P(file vide) = {proba_file_vide:.2%}"
        ax.text(0.98, 0.02, stats_text, transform=ax.transAxes,
                fontsize=9, verticalalignment='bottom', horizontalalignment='right',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f2f5', edgecolor=self.colors['primary'], alpha=0.9))
        
        try:
            fig.tight_layout()
        except:
            fig.subplots_adjust(left=0.08, right=0.96, top=0.94, bottom=0.08)
        
        self.canvas_discrete.draw()
        self.display_discrete_interpretation()
    
    def display_discrete_interpretation(self):
        """Affiche les interprétations pour la variable discrète"""
        if not self.resultats:
            return
        
        self.discrete_interpret_text.delete(1.0, tk.END)
        
        distribution = self.resultats.get('distribution_file', {})
        
        if not distribution or len(distribution) == 0:
            self.discrete_interpret_text.insert(1.0, 
                "⚠️ INTERPRÉTATION - VARIABLE DISCRÈTE\n\n"
                "Aucune donnée discrète disponible pour cette simulation.\n\n"
                "🔍 CAUSES POSSIBLES :\n"
                "• Le taux d'arrivée λ est trop faible par rapport à la capacité de service\n"
                "• Le nombre de caisses c est trop élevé\n"
                "• Le taux d'occupation ρ = λ/(c·μ) est trop faible\n\n"
                "💡 RECOMMANDATIONS :\n"
                "• Augmentez λ (taux d'arrivée)\n"
                "• Diminuez c (nombre de caisses)\n"
                "• Diminuez μ (taux de service) pour augmenter ρ\n"
                "• Visez un taux d'occupation ρ > 0.7 pour créer de l'attente")
            return
        
        # Calculs pour les interprétations
        moyenne_file = self.resultats.get('moyenne_file_discrete', 0)
        variance_file = self.resultats.get('variance_file', 0)
        proba_file_vide = self.resultats.get('proba_file_vide', 0)
        proba_file_grande = self.resultats.get('proba_file_grande', 0)
        lambda_val = self.resultats.get('lambda', 2.4)
        mu_val = self.resultats.get('mu', 0.5)
        c_val = self.resultats.get('c', 5)
        rho = self.resultats.get('rho', 0)
        
        # Distribution
        k_values = list(distribution.keys())
        probas = list(distribution.values())
        
        # Mode (valeur la plus probable)
        idx_max = probas.index(max(probas))
        mode = k_values[idx_max]
        
        # Calcul du coefficient de dispersion (variance/moyenne)
        if moyenne_file > 0:
            dispersion = variance_file / moyenne_file
        else:
            dispersion = 0
        
        interpretation = f"""
{'='*70}
📊 INTERPRÉTATION - VARIABLE DISCRÈTE
Nombre de clients en file d'attente (Q)
{'='*70}

📈 STATISTIQUES CLÉS
{'-'*50}
• Moyenne (E[Q])        : {moyenne_file:.3f} clients
• Variance (Var[Q])      : {variance_file:.3f}
• Écart-type (σ)         : {np.sqrt(variance_file):.3f} clients
• Mode (valeur la plus probable) : {mode} client(s)
• Probabilité file vide  : {proba_file_vide:.2%}
• Probabilité file > 5   : {proba_file_grande:.2%}

📐 ANALYSE DE LA DISTRIBUTION
{'-'*50}
"""
        
        # Analyse du coefficient de dispersion
        if dispersion < 0.8:
            interpretation += f"• Coefficient de dispersion = {dispersion:.2f} (< 0.8)\n"
            interpretation += "  → Distribution sous-dispersée. Les files sont moins variables que prévu.\n"
            interpretation += "  → Les arrivées sont relativement régulières.\n"
        elif dispersion > 1.2:
            interpretation += f"• Coefficient de dispersion = {dispersion:.2f} (> 1.2)\n"
            interpretation += "  → Distribution sur-dispersée. Les files sont très variables.\n"
            interpretation += "  → Présence probable de pics d'affluence.\n"
        else:
            interpretation += f"• Coefficient de dispersion = {dispersion:.2f} (≈ 1)\n"
            interpretation += "  → Distribution proche d'une loi de Poisson.\n"
            interpretation += "  → Comportement typique des files d'attente aléatoires.\n"
        
        interpretation += f"""
📊 DISTRIBUTION DES PROBABILITÉS
{'-'*50}
"""
        
        # Afficher les probabilités principales
        for k, p in zip(k_values[:10], probas[:10]):
            if p > 0.01:
                interpretation += f"P(Q = {k}) = {p:.4f} ({p*100:.2f}%)\n"
        
        if len(k_values) > 10:
            interpretation += f"... et {len(k_values)-10} autres valeurs\n"
        
        interpretation += f"""
📈 COMPARAISON AVEC LA LOI DE POISSON
{'-'*50}
La loi de Poisson est souvent utilisée pour modéliser le nombre d'arrivées.
Pour λ = {lambda_val:.1f}, la moyenne théorique serait {lambda_val:.1f} clients.

Ici, la moyenne empirique E[Q] = {moyenne_file:.3f} est {'inférieure' if moyenne_file < lambda_val else 'supérieure'} à λ.
"""

        # Analyse de la file vide
        if proba_file_vide > 0.5:
            interpretation += f"""
✅ FILE VIDE TRÈS FRÉQUENTE ({proba_file_vide:.2%})
   Le système est généralement sous-utilisé. Les caisses sont souvent libres.
   → Peut-être trop de caisses ouvertes pour l'affluence actuelle.
"""
        elif proba_file_vide > 0.2:
            interpretation += f"""
ℹ️ FILE VIDE MODÉRÉMENT FRÉQUENTE ({proba_file_vide:.2%})
   Le système fonctionne normalement avec des périodes d'activité et d'inactivité.
   → Configuration acceptable pour un supermarché standard.
"""
        else:
            interpretation += f"""
⚠️ FILE VIDE PEU FRÉQUENTE ({proba_file_vide:.2%})
   Le système est presque toujours occupé.
   → Risque de saturation et d'attente prolongée.
"""

        # Analyse des files longues
        if proba_file_grande > 0.1:
            interpretation += f"""
⚠️ RISQUE DE FILES LONGUES ({proba_file_grande:.2%} de chances d'avoir plus de 5 clients)
   Les clients risquent de subir des attentes importantes.
   → Recommandation : augmenter le nombre de caisses ou réduire l'affluence.
"""
        elif proba_file_grande > 0.02:
            interpretation += f"""
ℹ️ FILES LONGUES OCCASIONNELLES ({proba_file_grande:.2%})
   Quelques pics d'affluence peuvent générer des files, mais c'est acceptable.
   → Surveiller les heures de pointe.
"""
        else:
            interpretation += f"""
✅ FILES LONGUES RARES ({proba_file_grande:.2%})
   Le système gère bien l'affluence même aux heures chargées.
   → Configuration optimale.
"""

        interpretation += f"""
{'='*70}
📌 RECOMMANDATIONS
{'='*70}
"""
        if rho < 0.5:
            interpretation += "🔹 Taux d'occupation très faible (ρ < 0.5)\n"
            interpretation += "   → Le système est sous-utilisé. Envisagez de réduire le nombre de caisses pour optimiser les coûts.\n"
        elif rho < 0.7:
            interpretation += "🔹 Taux d'occupation correct (0.5 < ρ < 0.7)\n"
            interpretation += "   → Fonctionnement normal. Peu de risque de congestion.\n"
        elif rho < 0.9:
            interpretation += "🔹 Taux d'occupation élevé (0.7 < ρ < 0.9)\n"
            interpretation += "   → Système sous tension. Surveiller les pics d'affluence.\n"
        else:
            interpretation += "🔹 Taux d'occupation critique (ρ > 0.9)\n"
            interpretation += "   → Risque élevé de saturation. Augmenter la capacité de service.\n"

        interpretation += f"""
💡 Pour améliorer la fluidité :
   • Ajouter {max(0, int(c_val * 1.2) - c_val)} caisse(s) supplémentaire(s)
   • Former le personnel pour accélérer le service (augmenter μ)
   • Mettre en place des caisses rapides (moins de 10 articles)

📊 NOTE: Ces résultats sont basés sur une simulation de {self.resultats.get('duree_effective', 0):.0f} minutes.
"""

        self.discrete_interpret_text.insert(1.0, interpretation)
    
    def run_simulation(self):
        """Lancer la simulation avec nettoyage des données"""
        if self.simulation_en_cours:
            return
            
        try:
            self.simulation_en_cours = True
            self.simulate_btn.configure(state='disabled', text="⏳ Simulation en cours...")
            self.parent.update()
            
            # Récupérer les paramètres
            lambda_val = self.lambda_var.get()
            mu_val = self.mu_var.get()
            c_val = int(self.c_var.get())
            duree_val = int(self.duree_var.get())
            
            # Validation des paramètres
            if lambda_val <= 0 or mu_val <= 0 or c_val <= 0:
                messagebox.showerror("❌ Erreur", "Les paramètres doivent être positifs")
                self.simulation_en_cours = False
                self.simulate_btn.configure(state='normal', text="🚀 LANCER LA SIMULATION")
                return
            
            # Créer et lancer la simulation
            sim = SimulationFileAttente(lambda_val, mu_val, c_val)
            
            # Vérifier la stabilité
            rho = lambda_val / (c_val * mu_val)
            if rho >= 1:
                if not messagebox.askyesno(
                    "⚠️ Système instable",
                    f"ρ = {rho:.2f} ≥ 1\n\nLe système est instable.\nVoulez-vous continuer ?"
                ):
                    self.simulation_en_cours = False
                    self.simulate_btn.configure(state='normal', text="🚀 LANCER LA SIMULATION")
                    return
            
            # Lancer la simulation
            self.resultats = sim.simuler(duree_val)
            
            # Nettoyer les données
            self.nettoyer_donnees()
            
            # Ajouter à l'historique
            now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            self.historique.append({
                'params': (lambda_val, mu_val, c_val, duree_val),
                'resultats': self.resultats,
                'date': now
            })
            
            # Afficher les résultats
            self.display_results()
            self.display_raw_data()
            self.display_discrete_results()
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la simulation:\n{str(e)}")
        finally:
            self.simulation_en_cours = False
            self.simulate_btn.configure(state='normal', text="🚀 LANCER LA SIMULATION")
    
    def nettoyer_donnees(self):
        """Nettoie et valide les données reçues de la simulation"""
        if not self.resultats:
            return
        
        # S'assurer que l'échantillon existe
        if 'temps_attente_echantillon' not in self.resultats:
            self.resultats['temps_attente_echantillon'] = []
        
        # Convertir en liste de floats et filtrer les valeurs négatives
        echant = self.resultats['temps_attente_echantillon']
        if echant:
            echant = [float(t) for t in echant if t >= 0]
            self.resultats['temps_attente_echantillon'] = echant
            
            # Recalculer la moyenne
            if echant:
                self.resultats['temps_attente_moyen'] = float(np.mean(echant))
            else:
                self.resultats['temps_attente_moyen'] = 0.0
        
        # S'assurer que les autres valeurs sont des floats
        for key in ['nb_moyen_clients', 'nb_moyen_file', 'rho']:
            if key in self.resultats:
                self.resultats[key] = float(self.resultats[key])
    
    def display_results(self):
        """Afficher les résultats de la simulation - Version corrigée sans erreur tight_layout"""
        if not self.resultats:
            return
        
        # Nettoyer à nouveau les données avant affichage
        self.nettoyer_donnees()
        
        # Effacer les graphiques précédents
        self.fig.clear()
        
        echantillon = self.resultats.get('temps_attente_echantillon', [])
        
        # Vérifier si l'échantillon est vide
        if not echantillon or len(echantillon) == 0:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, "⚠️ Aucun client servi pendant la simulation\n\n"
                              "Causes possibles :\n"
                              "• Taux d'arrivée λ trop faible\n"
                              "• Durée de simulation trop courte\n\n"
                              f"λ = {self.resultats.get('lambda', 0):.2f} clients/min\n"
                              f"μ = {self.resultats.get('mu', 0):.2f} clients/min\n"
                              f"c = {self.resultats.get('c', 0)}\n"
                              f"ρ = {self.resultats.get('rho', 0):.3f}",
                    ha='center', va='center', fontsize=11, transform=ax.transAxes)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            self.fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
            self.canvas.draw()
            self.display_statistics()
            return
        
        # Créer les sous-graphiques
        gs = self.fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        ax1 = self.fig.add_subplot(gs[0, 0])
        ax2 = self.fig.add_subplot(gs[0, 1])
        ax3 = self.fig.add_subplot(gs[1, :])
        
        # 1. HISTOGRAMME
        ax1.hist(echantillon, bins=30, edgecolor='white', 
                color=self.colors['primary'], alpha=0.7)
        ax1.axvline(self.resultats['temps_attente_moyen'], 
                   color=self.colors['danger'], 
                   linestyle='--', 
                   linewidth=2,
                   label=f'Moyenne = {self.resultats["temps_attente_moyen"]:.2f} min')
        
        ax1.set_ylabel('Fréquence')
        ax1.set_title('Distribution des temps d\'attente')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. FONCTION DE RÉPARTITION
        echantillon_trie = sorted(echantillon)
        n = len(echantillon_trie)
        y = [(i+1)/n for i in range(n)]
        
        ax2.plot(echantillon_trie, y, color=self.colors['success'], linewidth=2)
        
        ax2.set_ylabel('Probabilité cumulée')
        ax2.set_title('Fonction de répartition')
        ax2.grid(True, alpha=0.3)
        
        # Ajouter les quartiles
        q1 = np.percentile(echantillon, 25)
        q2 = np.percentile(echantillon, 50)
        q3 = np.percentile(echantillon, 75)
        
        ax2.axvline(x=q1, color=self.colors['warning'], linestyle=':', alpha=0.7, label=f'Q1 = {q1:.2f}')
        ax2.axvline(x=q2, color=self.colors['danger'], linestyle=':', alpha=0.7, label=f'Médiane = {q2:.2f}')
        ax2.axvline(x=q3, color=self.colors['dark'], linestyle=':', alpha=0.7, label=f'Q3 = {q3:.2f}')
        ax2.legend(fontsize=8)
        
        # 3. ÉVOLUTION TEMPORELLE (simulée)
        temps = np.linspace(0, self.resultats.get('duree_effective', 480), 100)
        clients = self.resultats['nb_moyen_clients'] + 0.5 * np.sin(temps/30) + np.random.normal(0, 0.2, 100)
        clients = np.maximum(0, clients)
        
        ax3.plot(temps, clients, color=self.colors['primary'], linewidth=2, alpha=0.7)
        ax3.axhline(y=self.resultats['nb_moyen_clients'], 
                   color=self.colors['danger'], 
                   linestyle='--',
                   label=f'Moyenne = {self.resultats["nb_moyen_clients"]:.2f}')
        ax3.fill_between(temps, 
                        self.resultats['nb_moyen_clients'] - np.std(clients),
                        self.resultats['nb_moyen_clients'] + np.std(clients), 
                        alpha=0.2, color=self.colors['primary'])
        
        
        ax3.set_title('Évolution du nombre de clients')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Protection contre l'erreur tight_layout
        try:
            self.fig.tight_layout()
        except Exception:
            self.fig.subplots_adjust(left=0.08, right=0.95, top=0.93, bottom=0.08)
        
        self.canvas.draw()
        self.display_statistics()
    
    def display_statistics(self):
        """Afficher les statistiques détaillées"""
        if not self.resultats:
            return
        
        self.stats_text.delete(1.0, tk.END)
        
        echant = self.resultats.get('temps_attente_echantillon', [])
        
        # Vérifier si l'échantillon est vide
        if not echant or len(echant) == 0:
            self.stats_text.insert(1.0, "⚠️ AUCUN CLIENT SERVI\n\n"
                                        "La simulation n'a généré aucun client.\n"
                                        "Causes possibles :\n"
                                        "• Taux d'arrivée λ trop faible\n"
                                        "• Durée de simulation trop courte\n\n"
                                        "Valeurs actuelles :\n"
                                        f"λ = {self.resultats.get('lambda', 0):.2f} clients/min\n"
                                        f"μ = {self.resultats.get('mu', 0):.2f} clients/min\n"
                                        f"c = {self.resultats.get('c', 0)}\n"
                                        f"ρ = {self.resultats.get('rho', 0):.3f}")
            return
        
        # Calculs statistiques
        moyenne = self.resultats['temps_attente_moyen']
        minimum = min(echant)
        maximum = max(echant)
        q1 = np.percentile(echant, 25)
        mediane = np.percentile(echant, 50)
        q3 = np.percentile(echant, 75)
        ecart_type = np.std(echant)
        
        # Probabilités
        p0 = sum(1 for t in echant if t > 0) / len(echant)
        p2 = sum(1 for t in echant if t > 2) / len(echant)
        p5 = sum(1 for t in echant if t > 5) / len(echant)
        p10 = sum(1 for t in echant if t > 10) / len(echant) if max(echant) > 10 else 0.0
        
        stats = f"""
{'='*70}
RAPPORT DE SIMULATION - MODÈLE M/M/c
{'='*70}

PARAMÈTRES D'ENTRÉE
{'-'*50}
Taux d'arrivée (λ)         : {self.resultats.get('lambda', 0):.2f} clients/minute
Taux de service (μ)         : {self.resultats.get('mu', 0):.2f} clients/minute par caisse
Nombre de caisses (c)       : {self.resultats.get('c', 0)}
Taux d'occupation (ρ)       : {self.resultats.get('rho', 0):.3f}
Durée de simulation         : {self.resultats.get('duree_effective', 0):.0f} minutes

INDICATEURS DE PERFORMANCE
{'-'*50}
Clients servis              : {self.resultats.get('nb_clients_servis', 0)} clients
Temps d'attente moyen       : {moyenne:.3f} minutes
Temps d'attente minimum     : {minimum:.3f} minutes
Temps d'attente maximum     : {maximum:.3f} minutes

STATISTIQUES DESCRIPTIVES
{'-'*50}
Premier quartile (Q1)       : {q1:.3f} minutes
Médiane (Q2)                : {mediane:.3f} minutes
Troisième quartile (Q3)     : {q3:.3f} minutes
Écart-type                  : {ecart_type:.3f} minutes

PROBABILITÉS D'ATTENTE
{'-'*50}
P(attente > 0 min)          : {p0:.1%}
P(attente > 2 min)          : {p2:.1%}
P(attente > 5 min)          : {p5:.1%}
P(attente > 10 min)         : {p10:.1%}

ANALYSE ET RECOMMANDATIONS
{'-'*50}
"""
        # Analyse du taux d'occupation
        rho_val = self.resultats.get('rho', 0)
        if rho_val >= 1:
            stats += "⚠️ SYSTÈME INSTABLE : ρ ≥ 1\n"
            stats += "   La file d'attente va croître indéfiniment.\n"
            stats += "   ▶ Action requise : augmenter le nombre de caisses.\n\n"
        elif rho_val > 0.8:
            stats += "⚠️ SYSTÈME SOUS TENSION : ρ > 0,8\n"
            stats += "   Risque de saturation aux heures de pointe.\n"
            stats += "   ▶ Recommandation : prévoir des renforts.\n\n"
        else:
            stats += "✅ SYSTÈME STABLE\n\n"
        
        # Analyse du temps d'attente
        if moyenne > 5:
            stats += "⏰ TEMPS D'ATTENTE CRITIQUE : > 5 minutes\n"
            stats += "   Risque élevé de mécontentement client.\n"
            stats += "   ▶ Action urgente : ouvrir des caisses supplémentaires.\n"
        elif moyenne > 2:
            stats += "⏱️ TEMPS D'ATTENTE ACCEPTABLE : entre 2 et 5 minutes\n"
            stats += "   Qualité de service correcte mais à surveiller.\n"
        else:
            stats += "⚡ TEMPS D'ATTENTE EXCELLENT : < 2 minutes\n"
            stats += "   Qualité de service optimale.\n"
        
        # Ajouter une note sur la fiabilité
        stats += f"\n📊 NOTE: Résultats basés sur {len(echant)} clients servis.\n"
        
        self.stats_text.insert(1.0, stats)
    
    def display_raw_data(self):
        """Afficher les données brutes"""
        if not self.resultats:
            return
        
        echant = self.resultats.get('temps_attente_echantillon', [])
        
        # Effacer l'ancien contenu
        for widget in self.data_frame.winfo_children():
            widget.destroy()
        
        # Vérifier si l'échantillon est vide
        if not echant or len(echant) == 0:
            tk.Label(
                self.data_frame,
                text="📭 Aucune donnée à afficher",
                font=('Segoe UI', 14),
                bg='white',
                fg=self.colors['text_light']
            ).pack(expand=True)
            return
        
        # En-tête avec statistiques rapides
        header_frame = tk.Frame(self.data_frame, bg='white')
        header_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            header_frame,
            text="📋 DONNÉES BRUTES DES TEMPS D'ATTENTE",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg=self.colors['primary']
        ).pack()
        
        tk.Label(
            header_frame,
            text=f"Total: {len(echant)} clients | Min: {min(echant):.3f} min | Max: {max(echant):.3f} min | Moyenne: {self.resultats['temps_attente_moyen']:.3f} min",
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['text']
        ).pack(pady=(5, 5))
        
        # Canvas avec scrollbar
        canvas = tk.Canvas(self.data_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.data_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame pour deux colonnes
        cols_frame = tk.Frame(scrollable_frame, bg='white')
        cols_frame.pack(fill='both', expand=True, padx=20)
        
        col1 = tk.Frame(cols_frame, bg='white')
        col2 = tk.Frame(cols_frame, bg='white')
        col1.pack(side='left', fill='both', expand=True, padx=(0, 5))
        col2.pack(side='left', fill='both', expand=True, padx=(5, 0))
        
        milieu = len(echant) // 2
        
        # Première moitié
        for i in range(milieu):
            frame = tk.Frame(col1, bg='white')
            frame.pack(fill='x', pady=1)
            
            tk.Label(
                frame,
                text=f"Client {i+1:4d}:",
                font=('Consolas', 10, 'bold'),
                bg='white',
                fg=self.colors['primary'],
                width=15,
                anchor='w'
            ).pack(side='left')
            
            if echant[i] == 0:
                tk.Label(
                    frame,
                    text=f"{echant[i]:6.3f} min (service immédiat) ⚡",
                    font=('Consolas', 10),
                    bg='white',
                    fg=self.colors['success']
                ).pack(side='left')
            else:
                tk.Label(
                    frame,
                    text=f"{echant[i]:6.3f} minutes",
                    font=('Consolas', 10),
                    bg='white',
                    fg=self.colors['text']
                ).pack(side='left')
        
        # Deuxième moitié
        for i in range(milieu, len(echant)):
            frame = tk.Frame(col2, bg='white')
            frame.pack(fill='x', pady=1)
            
            tk.Label(
                frame,
                text=f"Client {i+1:4d}:",
                font=('Consolas', 10, 'bold'),
                bg='white',
                fg=self.colors['primary'],
                width=15,
                anchor='w'
            ).pack(side='left')
            
            if echant[i] == 0:
                tk.Label(
                    frame,
                    text=f"{echant[i]:6.3f} min (service immédiat) ⚡",
                    font=('Consolas', 10),
                    bg='white',
                    fg=self.colors['success']
                ).pack(side='left')
            else:
                tk.Label(
                    frame,
                    text=f"{echant[i]:6.3f} minutes",
                    font=('Consolas', 10),
                    bg='white',
                    fg=self.colors['text']
                ).pack(side='left')
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def reset_params(self):
        """Réinitialiser les paramètres"""
        self.lambda_var.set(2.4)
        self.mu_var.set(0.5)
        self.c_var.set(5)
        self.duree_var.set(480)
    
    def show_history(self):
        """Afficher l'historique"""
        self.clear_main_content()
        
        tk.Label(
            self.main_content,
            text="📜 Historique",
            font=('Segoe UI', 26, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['dark']
        ).pack(anchor='w', pady=(0, 20))
        
        if not self.historique:
            empty_frame = tk.Frame(self.main_content, bg='white')
            empty_frame.pack(fill='both', expand=True, pady=50)
            
            tk.Label(
                empty_frame,
                text="📭",
                font=('Segoe UI', 72),
                bg='white',
                fg=self.colors['text_light']
            ).pack(pady=20)
            
            tk.Label(
                empty_frame,
                text="Aucune simulation",
                font=('Segoe UI', 18),
                bg='white',
                fg=self.colors['text_light']
            ).pack()
        else:
            hist_frame = tk.Frame(self.main_content, bg='white')
            hist_frame.pack(fill='both', expand=True, pady=10)
            
            for i, sim in enumerate(self.historique[-10:]):
                sim_frame = tk.Frame(hist_frame, bg='white', relief='solid', bd=1)
                sim_frame.pack(fill='x', pady=2, padx=5)
                
                tk.Label(
                    sim_frame,
                    text=f"{sim['date']} - λ={sim['params'][0]:.1f}, μ={sim['params'][1]:.1f}, c={sim['params'][2]}, durée={sim['params'][3]}min",
                    font=('Segoe UI', 10),
                    bg='white',
                    fg=self.colors['text'],
                    anchor='w'
                ).pack(side='left', padx=10, pady=5)
                
                tk.Label(
                    sim_frame,
                    text=f"Servis: {sim['resultats']['nb_clients_servis']} clients",
                    font=('Segoe UI', 10, 'bold'),
                    bg='white',
                    fg=self.colors['primary'],
                    anchor='e'
                ).pack(side='right', padx=10, pady=5)
    
    def show_help(self):
        """Afficher l'aide"""
        self.clear_main_content()
        
        tk.Label(
            self.main_content,
            text="❓ Aide",
            font=('Segoe UI', 26, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['dark']
        ).pack(anchor='w', pady=(0, 20))
        
        canvas = tk.Canvas(self.main_content, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.main_content, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        sections = [
        ("🎯 INTRODUCTION", 
        "═══════════════════════════════════════════════════════════\n"
        "            Pro - Simulation de files d'attente          \n"
        "═══════════════════════════════════════════════════════════\n\n"
        "Application basée sur le modèle probabiliste M/M/c.\n\n"
        "Elle permet aux gestionnaires de supermarchés de :\n"
        "  • Optimiser le nombre de caisses ouvertes\n"
        "  • Anticiper les périodes d'affluence\n"
        "  • Réduire les temps d'attente des clients\n"
        "  • Maîtriser les coûts de personnel\n\n"
        "📌 MODÈLE M/M/c\n"
        "  • Premier M  →  Arrivées aléatoires (loi exponentielle)\n"
        "  • Second M   →  Services aléatoires (loi exponentielle)\n"
        "  • c          →  Nombre de caisses ouvertes",
        self.colors['primary']),
        
        ("📊 PARAMÈTRES DE SIMULATION", 
        "═══════════════════════════════════════════════════════════\n"
        "                    📈 TAUX D'ARRIVÉE (λ)                       \n"
        "═══════════════════════════════════════════════════════════\n\n"
        "  • Définition : Nombre moyen de clients arrivant par minute\n"
        "  • Exemple    : λ = 2 → 2 clients par minute en moyenne\n"
        "  • Impact     : Plus λ est élevé, plus le système est sollicité\n\n"
        "═══════════════════════════════════════════════════════════\n"
        "                    ⚡ TAUX DE SERVICE (μ)                       \n"
        "═══════════════════════════════════════════════════════════\n\n"
        "  • Définition : Nombre moyen de clients servis par minute\n"
        "  • Exemple    : μ = 0,5 → 0,5 client/min (2 min par client)\n"
        "  • Impact     : Plus μ est élevé, plus le service est rapide\n\n"
        "═══════════════════════════════════════════════════════════\n"
        "                    🏪 NOMBRE DE CAISSES (c)                     \n"
        "═══════════════════════════════════════════════════════════\n\n"
        "  • Définition : Nombre de caisses ouvertes simultanément\n"
        "  • Exemple    : c = 5 → 5 caisses en service\n"
        "  • Impact     : Capacité de traitement parallèle\n\n"
        "═══════════════════════════════════════════════════════════\n"
        "                    ⏱️ DURÉE DE SIMULATION                       \n"
        "═══════════════════════════════════════════════════════════\n\n"
        "  • Définition : Temps de simulation en minutes\n"
        "  • Exemple    : 480 minutes = 8 heures de travail\n"
        "  • Recommandation : Minimum 480 min pour des résultats stables",
        self.colors['success']),
        
        ("📈 INTERPRÉTATION DES RÉSULTATS", 
        "═══════════════════════════════════════════════════════════\n"
        "              📊 TAUX D'OCCUPATION (ρ = λ / (c × μ))           \n"
        "═══════════════════════════════════════════════════════════\n\n"
        "  ρ < 1  →  ✅ SYSTÈME STABLE\n"
        "  ρ = 1  →  ⚠️ LIMITE DE SATURATION\n"
        "  ρ > 1  →  ❌ SYSTÈME INSTABLE (file infinie)\n\n"
        "═══════════════════════════════════════════════════════════\n"
        "                 ⏱️ TEMPS D'ATTENTE MOYEN (Wq)                   \n"
        "═══════════════════════════════════════════════════════════\n\n"
        "     🟢 EXCELLENT        🟡 ACCEPTABLE        🔴 CRITIQUE\n"
        "       < 2 min            2 - 5 min            > 5 min\n\n"
        "═══════════════════════════════════════════════════════════\n"
        "               👥 FILE D'ATTENTE MOYENNE (Lq)                   \n"
        "═══════════════════════════════════════════════════════════\n\n"
        "     🟢 NORMAL          🟡 SURVEILLANCE      🔴 ACTION\n"
        "       < 3 clients        3 - 5 clients         > 5 clients",
        self.colors['warning']),

        
        ("💡 CONSEILS D'UTILISATION", 
        "═══════════════════════════════════════════════════════════\n"
        "                      🚀 GUIDE PRATIQUE                       \n"
        "═══════════════════════════════════════════════════════════\n\n"
        "📌 ÉTAPE 1 : CONFIGURATION INITIALE\n"
        "  λ = 2,4 clients/min   |   μ = 0,5 clients/min\n"
        "  c = 5 caisses         |   Durée = 480 minutes\n\n"
        "📌 ÉTAPE 2 : ANALYSE DU TAUX D'OCCUPATION\n"
        "  ρ = λ / (c × μ)  →  Objectif : ρ < 1\n\n"
        "📌 ÉTAPE 3 : AJUSTEMENT DES PARAMÈTRES\n"
        "  • Pour créer de l'attente  →  Augmenter λ ou diminuer c\n"
        "  • Pour réduire l'attente   →  Diminuer λ ou augmenter c\n"
        "  • Pour plus de stabilité   →  Visez ρ = 0,7 - 0,8\n\n"
        "📌 ÉTAPE 4 : INTERPRÉTATION\n"
        "  ✅ Temps d'attente < 2 min  →  Configuration optimale\n"
        "  ⚠️ Temps d'attente 2-5 min →  À surveiller\n"
        "  ❌ Temps d'attente > 5 min  →  Action urgente\n\n"
        "📌 ÉTAPE 5 : ANTICIPATION\n"
        "  • P(Wq > 5 min) > 10%  →  Risque de mécontentement\n"
        "  • P(Q > 5) > 5%        →  Risque d'encombrement\n\n"
        "⚠️ CAS PARTICULIER : SYSTÈME INSTABLE (ρ ≥ 1)\n"
        "  • La file d'attente croît indéfiniment\n"
        "  • Solution : Augmenter le nombre de caisses (c)",
        self.colors['pink'])
    ]  
        
        for titre, texte, couleur in sections:
            frame = tk.Frame(scrollable_frame, bg='white', relief='solid', bd=1)
            frame.pack(fill='x', pady=10, padx=10)
            
            tk.Label(
                frame,
                text=titre,
                font=('Segoe UI', 14, 'bold'),
                bg=couleur,
                fg='white',
                pady=8,
                padx=15
            ).pack(fill='x')
            
            tk.Label(
                frame,
                text=texte,
                font=('Segoe UI', 11),
                bg='white',
                fg=self.colors['text'],
                justify='left',
                padx=15,
                pady=15
            ).pack(fill='x')
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def logout(self):
        """Déconnexion"""
        if messagebox.askyesno("Déconnexion", "Êtes-vous sûr de vouloir vous déconnecter ?"):
            self.parent.destroy()
            import login
            root = tk.Tk()
            root.withdraw()
            login.LoginWindow(root)
            root.mainloop()