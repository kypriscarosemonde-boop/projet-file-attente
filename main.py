#!/usr/bin/env python3
"""
Application professionnelle de simulation de files d'attente
Auteur : KY Prisca
Date : 2024
"""

import tkinter as tk
from tkinter import messagebox
from login import LoginWindow

def main():
    """Point d'entrée principal de l'application"""
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    
    # Afficher la fenêtre de connexion
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()