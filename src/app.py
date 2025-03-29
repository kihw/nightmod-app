#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module principal de l'application NightMod
Gère l'interface utilisateur et la logique principale
"""

import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import platform
from datetime import datetime
import logging
import traceback

# Importer les modules internes
from src.config import ConfigManager
from src.system_actions import SystemActions
from src.popup import PopupChecker
from src.tray import TrayIcon

# Obtenir le logger
logger = logging.getLogger("NightMod.App")

class NightModApp(tk.Tk):
    """Application principale NightMod"""
    
    def __init__(self):
        super().__init__()
        
        # Chargement de la configuration
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_all()
        
        # Variables d'état
        self.is_running = False
        self.timer_thread = None
        self.next_check_time = None
        
        # Configuration de la fenêtre principale
        self.setup_main_window()
        
        # Configuration du système de notification
        self.tray_icon = TrayIcon(
            self,
            self.toggle_visibility,
            self.toggle_monitoring,
            self.on_close
        )
        self.tray_icon.setup()
        
        # Initialisation de l'interface utilisateur
        self.setup_ui()
        
        # Démarre automatiquement la surveillance si configuré
        if self.config.get("start_with_system", False):
            self.start_monitoring()
    
    def setup_main_window(self):
        """Configure la fenêtre principale de l'application avec une mise en page moderne"""
        self.title("NightMod")
        self.geometry("480x520")  # Dimensions optimisées
        self.minsize(480, 520)
        
        # Centrer la fenêtre sur l'écran
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 480) // 2
        y = (screen_height - 520) // 2
        self.geometry(f"+{x}+{y}")
        
        # Style et thème
        self.style = ttk.Style()
        
        # Appliquer un thème moderne
        self.configure_theme()
        
        # Icône de l'application
        self.set_application_icon()
        
        # IMPORTANT: Gestion de la fermeture
        # Utilisation d'une fonction lambda au lieu d'une référence directe à méthode
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        
        # Raccourcis clavier
        self.bind("<Alt-q>", lambda e: self.on_close())
        self.bind("<Alt-n>", lambda e: self.toggle_visibility())
        self.bind("<F1>", lambda e: self.show_help())
        
        # Empêcher le redimensionnement sur certaines plateformes (pour une meilleure apparence)
        if platform.system() == "Windows" or platform.system() == "Darwin":  # Windows ou macOS
            self.resizable(False, False)
    
    
    def configure_theme(self):
        """Configure un thème moderne pour l'interface utilisateur"""
        try:
            # Essayer de charger le thème moderne personnalisé
            theme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "themes/modern.tcl")
            if os.path.exists(theme_path):
                self.tk.call("source", theme_path)
                self.tk.call("set_theme", "dark")
                logger.info("Thème moderne appliqué avec succès")
                return True
                
            # Fallback: essayer le thème Azure
            theme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "themes/azure.tcl")
            if os.path.exists(theme_path):
                self.tk.call("source", theme_path)
                self.tk.call("set_theme", "dark")
                logger.info("Thème Azure appliqué avec succès")
                return True
        except Exception as e:
            logger.warning(f"Impossible de charger le thème personnalisé: {e}")
        
        # Fallback: style personnalisé basique
        try:
            # Configuration manuelle des styles
            self.configure(bg="#1a1a1a")
            
            # Configurer les styles ttk
            self.style = ttk.Style(self)
            
            # Style de base
            self.style.configure(".", 
                                 background="#1a1a1a",
                                 foreground="#FFFFFF",
                                 troughcolor="#121212",
                                 selectbackground="#4CAF50",
                                 selectforeground="#FFFFFF",
                                 borderwidth=0)
            
            # Frames
            self.style.configure("TFrame", background="#1a1a1a")
            self.style.configure("Card.TFrame", background="#252525", relief="flat")
            
            # Labels
            self.style.configure("TLabel", background="#1a1a1a", foreground="#FFFFFF")
            self.style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
            self.style.configure("Subtitle.TLabel", font=("Segoe UI", 12, "bold"))
            self.style.configure("Caption.TLabel", foreground="#AAAAAA", font=("Segoe UI", 9))
            
            # Boutons
            self.style.configure("TButton", padding=6, relief="flat", background="#2d2d2d")
            self.style.map("TButton", 
                           background=[("pressed", "#252525"), ("active", "#333333")],
                           foreground=[("disabled", "#888888")])
            
            self.style.configure("Primary.TButton", 
                                 background="#4CAF50",
                                 foreground="#FFFFFF")
            self.style.map("Primary.TButton",
                           background=[("pressed", "#388E3C"), ("active", "#388E3C")],
                           foreground=[("disabled", "#CCCCCC")])
            
            self.style.configure("Secondary.TButton", 
                                 background="#2d2d2d")
            
            self.style.configure("Accent.TButton", 
                                 background="#4CAF50",
                                 foreground="#FFFFFF")
            self.style.map("Accent.TButton",
                           background=[("pressed", "#388E3C"), ("active", "#388E3C")],
                           foreground=[("disabled", "#CCCCCC")])
            
            # Checkbuttons et Radiobuttons
            self.style.configure("TCheckbutton", background="#1a1a1a", foreground="#FFFFFF")
            self.style.configure("TRadiobutton", background="#1a1a1a", foreground="#FFFFFF")
            
            # Entrées
            self.style.configure("TEntry", 
                                 fieldbackground="#252525",
                                 foreground="#FFFFFF",
                                 padding=8)
            
            # Séparateurs
            self.style.configure("TSeparator", background="#333333")
            
            logger.info("Style personnalisé de base appliqué avec succès")
            return True
            
        except Exception as e:
            logger.error(f"Impossible d'appliquer le style personnalisé: {e}")
            return False
    
    def set_application_icon(self):
        """Définit l'icône de l'application"""
        try:
            if platform.system() == "Windows":
                icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/icon.ico")
                if os.path.exists(icon_path):
                    self.iconbitmap(icon_path)
            else:
                icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/icon.png")
                if os.path.exists(icon_path):
                    icon = tk.PhotoImage(file=icon_path)
                    self.iconphoto(True, icon)
        except Exception as e:
            logger.warning(f"Impossible de charger l'icône: {e}")
    
    def setup_ui(self):
        """Configure l'interface utilisateur principale"""
        # Utiliser un padding plus généreux et une palette de couleurs apaisante
        main_frame = ttk.Frame(self, padding="30 35 30 35")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # En-tête avec logo moderne
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Tenter de charger le logo
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/icon.png")
            if os.path.exists(icon_path):
                logo = tk.PhotoImage(file=icon_path)
                logo = logo.subsample(3, 3)  # Ajuster la taille
                logo_label = ttk.Label(header_frame, image=logo)
                logo_label.image = logo  # Garder une référence
                logo_label.pack(side=tk.LEFT, padx=(0, 15))
        except Exception as e:
            logger.warning(f"Impossible de charger le logo: {e}")
        
        ttk.Label(
            header_frame, 
            text="NightMod", 
            font=("Segoe UI", 22, "bold")
        ).pack(side=tk.LEFT)
        
        # Séparateur élégant
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 25))
        
        # État actuel - Conception plus minimaliste avec indicateur visuel
        self.status_var = tk.StringVar(value="Inactif")
        self.next_check_var = tk.StringVar(value="Aucune vérification prévue")
        
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Indicateur visuel de statut (cercle coloré)
        self.status_indicator = ttk.Label(
            status_frame, 
            text="●", 
            font=("Segoe UI", 14),
            foreground="#888888"  # Gris quand inactif
        )
        self.status_indicator.grid(row=0, column=0, rowspan=2, padx=(0, 15))
        
        ttk.Label(
            status_frame, 
            text="État", 
            font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(
            status_frame, 
            textvariable=self.status_var,
            font=("Segoe UI", 11)
        ).grid(row=0, column=2, sticky=tk.W, padx=10)
        
        ttk.Label(
            status_frame, 
            text="Prochaine vérification", 
            font=("Segoe UI", 11, "bold")
        ).grid(row=1, column=1, sticky=tk.W, pady=(8, 0))
        
        ttk.Label(
            status_frame, 
            textvariable=self.next_check_var,
            font=("Segoe UI", 11)
        ).grid(row=1, column=2, sticky=tk.W, padx=10, pady=(8, 0))
        
        # Boutons d'action principaux - Placés en haut pour un accès facile
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 25))
        
        self.start_button = ttk.Button(
            action_frame, 
            text="Démarrer la surveillance",
            command=self.toggle_monitoring,
            style="Accent.TButton",
            width=22
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            action_frame, 
            text="Tester la vérification",
            command=self.test_popup,
            width=22
        ).pack(side=tk.RIGHT)
        
        # Paramètres avec design épuré
        settings_frame = ttk.LabelFrame(main_frame, text="Paramètres", padding="20 15")
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Grille avec plus d'espace
        settings_grid = ttk.Frame(settings_frame)
        settings_grid.pack(fill=tk.X)
        
        # Première colonne: Intervalles
        interval_frame = ttk.Frame(settings_grid)
        interval_frame.grid(row=0, column=0, sticky=tk.W, padx=(0, 20), pady=10)
        
        ttk.Label(
            interval_frame, 
            text="Intervalles",
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(
            interval_frame, 
            text="Vérification:"
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.check_interval_var = tk.IntVar(value=self.config.get("check_interval_minutes", 20))
        interval_spinner = ttk.Spinbox(
            interval_frame, 
            from_=5, 
            to=120, 
            width=5, 
            textvariable=self.check_interval_var
        )
        interval_spinner.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        ttk.Label(interval_frame, text="min").grid(row=1, column=2, sticky=tk.W)
        
        ttk.Label(
            interval_frame, 
            text="Réponse:"
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.response_time_var = tk.IntVar(value=self.config.get("response_time_seconds", 30))
        response_spinner = ttk.Spinbox(
            interval_frame, 
            from_=15, 
            to=60, 
            width=5, 
            textvariable=self.response_time_var
        )
        response_spinner.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        ttk.Label(interval_frame, text="sec").grid(row=2, column=2, sticky=tk.W)
        
        # Deuxième colonne: Comportement
        behavior_frame = ttk.Frame(settings_grid)
        behavior_frame.grid(row=0, column=1, sticky=tk.W, padx=20, pady=10)
        
        ttk.Label(
            behavior_frame, 
            text="Comportement",
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(
            behavior_frame, 
            text="Action:"
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.action_var = tk.StringVar(value=self.config.get("shutdown_action", "shutdown"))
        action_combo = ttk.Combobox(
            behavior_frame, 
            width=10, 
            textvariable=self.action_var, 
            state="readonly"
        )
        action_combo["values"] = ("shutdown", "sleep", "lock")
        action_combo.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Section des options avec cases à cocher - Alignement simplifié
        options_frame = ttk.Frame(settings_frame)
        options_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Separator(settings_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        # Options groupées avec une meilleure organisation
        self.sound_var = tk.BooleanVar(value=self.config.get("sound_enabled", True))
        sound_check = ttk.Checkbutton(
            options_frame, 
            text="Son de notification", 
            variable=self.sound_var
        )
        sound_check.grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 30))
        
        self.autostart_var = tk.BooleanVar(value=self.config.get("start_with_system", False))
        autostart_check = ttk.Checkbutton(
            options_frame, 
            text="Démarrage automatique", 
            variable=self.autostart_var
        )
        autostart_check.grid(row=0, column=1, sticky=tk.W, pady=5, padx=10)
        
        self.minimize_var = tk.BooleanVar(value=self.config.get("minimize_to_tray", True))
        minimize_check = ttk.Checkbutton(
            options_frame, 
            text="Minimiser dans la barre des tâches", 
            variable=self.minimize_var
        )
        minimize_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Bouton pour appliquer les paramètres - Bien distinct et en bas
        save_button_frame = ttk.Frame(main_frame)
        save_button_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Button(
            save_button_frame, 
            text="Appliquer les paramètres",
            command=self.save_settings,
            width=25
        ).pack(side=tk.RIGHT)
        
        # Pied de page discret
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(30, 0))
        
        ttk.Label(
            footer_frame, 
            text="NightMod v1.0.0", 
            font=("Segoe UI", 8),
            foreground="#888888"
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            footer_frame, 
            text="© 2025", 
            font=("Segoe UI", 8),
            foreground="#888888" 
        ).pack(side=tk.RIGHT)
    
    def show_help(self):
        """Affiche une fenêtre d'aide simplifiée"""
        help_window = tk.Toplevel(self)
        help_window.title("Aide NightMod")
        help_window.geometry("400x300")
        help_window.transient(self)  # Fenêtre modale
        help_window.grab_set()
        
        # Appliquer le même style
        help_window.configure(background="#2E2E2E")
        
        # Contenu de l'aide
        help_frame = ttk.Frame(help_window, padding="20")
        help_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            help_frame,
            text="Aide NightMod",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(
            help_frame,
            text="NightMod surveille votre activité et éteint ou verrouille votre ordinateur automatiquement si vous vous endormez.",
            wraplength=360,
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(0, 15))
        
        help_text = """
• Démarrer/Arrêter: Active ou désactive la surveillance
• Intervalle: Temps entre les vérifications (minutes)
• Réponse: Délai pour répondre à la vérification (secondes)
• Action: Ce qui se passe si vous ne répondez pas

Raccourcis clavier:
Alt+N: Affiche/masque la fenêtre principale
Alt+Q: Quitte l'application
F1: Affiche cette aide
Échap: Répond aux vérifications
        """
        
        ttk.Label(
            help_frame,
            text=help_text,
            justify=tk.LEFT,
            wraplength=360
        ).pack(anchor=tk.W)
        
        ttk.Button(
            help_frame,
            text="Fermer",
            command=help_window.destroy
        ).pack(side=tk.BOTTOM, anchor=tk.SE, pady=(15, 0))
        
        # Centrer la fenêtre par rapport à la fenêtre principale
        help_window.update_idletasks()
        width = help_window.winfo_width()
        height = help_window.winfo_height()
        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        help_window.geometry(f"+{x}+{y}")
    
    def toggle_visibility(self):
        """Affiche ou masque la fenêtre principale"""
        if self.state() == 'withdrawn':
            self.deiconify()
            self.lift()
        else:
            self.withdraw()
    
    def toggle_monitoring(self):
        """Démarre ou arrête la surveillance"""
        if self.is_running:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def start_monitoring(self):
        """Démarre le processus de surveillance"""
        if self.is_running:
            return
        
        self.is_running = True
        self.status_var.set("Actif")
        self.status_indicator.config(foreground="#4CAF50")  # Vert quand actif
        self.start_button.config(text="Arrêter la surveillance")
        
        # Mettre à jour les valeurs de configuration
        self.config["check_interval_minutes"] = self.check_interval_var.get()
        self.config["response_time_seconds"] = self.response_time_var.get()
        
        # Mettre à jour l'icône de la barre des tâches
        if hasattr(self, 'tray_icon') and self.tray_icon:
            self.tray_icon.update_icon(True)
        
        # Démarrer le thread de surveillance
        self.timer_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.timer_thread.start()
        
        logger.info("Surveillance démarrée")
        
        # Minimiser dans la barre des tâches si configuré
        if self.config.get("minimize_to_tray", True) and hasattr(self, 'tray_icon') and self.tray_icon.is_available():
            self.withdraw()
    
    def stop_monitoring(self):
        """Arrête le processus de surveillance"""
        self.is_running = False
        self.status_var.set("Inactif")
        self.status_indicator.config(foreground="#888888")  # Gris quand inactif
        self.next_check_var.set("Aucune vérification prévue")
        self.start_button.config(text="Démarrer la surveillance")
        self.next_check_time = None
        
        # Mettre à jour l'icône de la barre des tâches
        if hasattr(self, 'tray_icon') and self.tray_icon:
            self.tray_icon.update_icon(False)
            
        logger.info("Surveillance arrêtée")
    
    def monitoring_loop(self):
        """Boucle principale de surveillance exécutée dans un thread séparé"""
        while self.is_running:
            # Calcul du temps jusqu'à la prochaine vérification
            interval_seconds = self.config.get("check_interval_minutes", 20) * 60
            
            # Mettre à jour l'heure de la prochaine vérification
            self.next_check_time = datetime.now().timestamp() + interval_seconds
            
            # Mettre à jour l'interface
            self.update_next_check_time()
            
            # Attendre l'intervalle spécifié
            for _ in range(interval_seconds):
                if not self.is_running:
                    break
                time.sleep(1)
                # Mettre à jour le temps restant toutes les 60 secondes
                if _ % 60 == 0:
                    self.update_next_check_time()
            
            # Vérifier si on est toujours en cours d'exécution
            if not self.is_running:
                break
            
            # Lancer la vérification
            self.show_check_popup()
    
    def update_next_check_time(self):
        """Met à jour l'affichage du temps restant jusqu'à la prochaine vérification"""
        if not self.next_check_time:
            self.next_check_var.set("Aucune vérification prévue")
            return
        
        now = datetime.now().timestamp()
        remaining = max(0, self.next_check_time - now)
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        # Mettre à jour l'interface depuis le thread principal
        self.after(0, lambda: self.next_check_var.set(f"Dans {time_str}"))
    
    def show_check_popup(self):
        """Affiche la fenêtre popup de vérification"""
        if not self.is_running:
            return
        
        # S'assurer que ceci est exécuté dans le thread principal
        self.after(0, lambda: self._create_popup())
    
    def _create_popup(self):
        """Crée et affiche la fenêtre popup"""
        # Actualiser la configuration avant de créer le popup
        response_time = self.config.get("response_time_seconds", 30)
        
        # Créer le popup
        popup = PopupChecker(
            self,
            response_time,
            self.on_user_response,
            self.on_no_response,
            self.config
        )
    
    def test_popup(self):
        """Fonction pour tester le popup de vérification"""
        self._create_popup()
    
    def on_user_response(self):
        """Appelé quand l'utilisateur répond au popup"""
        logger.info("L'utilisateur a répondu. Reprise de la surveillance.")
        # Rien à faire de spécial, la boucle de surveillance continue normalement
    
    def on_no_response(self):
        """Appelé quand l'utilisateur ne répond pas au popup"""
        logger.info("L'utilisateur n'a pas répondu. Exécution de l'action configurée.")
        
        # Arrêter la surveillance
        self.stop_monitoring()
        
        # Exécuter l'action configurée immédiatement
        action = self.config.get("shutdown_action", "shutdown")
        
        # Journal pour garder une trace de l'action exécutée
        if action == "shutdown":
            logger.warning("Aucune réponse détectée. Extinction immédiate de l'ordinateur.")
        elif action == "sleep":
            logger.warning("Aucune réponse détectée. Mise en veille immédiate de l'ordinateur.")
        elif action == "lock":
            logger.warning("Aucune réponse détectée. Verrouillage immédiat de l'écran.")
        
        try:
            # Exécuter l'action directement sans message ni délai
            SystemActions.perform_action(action)
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de l'action: {e}")
            logger.error(traceback.format_exc())
    
    def save_settings(self):
        """Sauvegarde les paramètres avec animation de confirmation"""
        # Récupérer les valeurs depuis l'interface
        self.config["check_interval_minutes"] = self.check_interval_var.get()
        self.config["response_time_seconds"] = self.response_time_var.get()
        self.config["shutdown_action"] = self.action_var.get()
        self.config["sound_enabled"] = self.sound_var.get()
        self.config["start_with_system"] = self.autostart_var.get()
        self.config["minimize_to_tray"] = self.minimize_var.get()
        
        # Sauvegarder la configuration
        if self.config_manager.update(self.config):
            # Afficher une animation de confirmation au lieu d'une messagebox
            self.show_save_confirmation()
            
            # Configurer le démarrage automatique avec le système si nécessaire
            try:
                autostart = self.config.get("start_with_system", False)
                SystemActions.configure_autostart(autostart)
            except Exception as e:
                logger.error(f"Erreur lors de la configuration du démarrage automatique: {e}")
                messagebox.showwarning(
                    "NightMod", 
                    "Impossible de configurer le démarrage automatique. "
                    "Veuillez le faire manuellement."
                )
        else:
            messagebox.showerror("NightMod", "Erreur lors de l'enregistrement des paramètres.")

    def show_save_confirmation(self):
        """Affiche une confirmation stylisée pour l'enregistrement des paramètres"""
        # Créer un label flottant pour la confirmation
        confirmation = ttk.Label(
            self,
            text="✓ Paramètres enregistrés",
            background="#4CAF50",
            foreground="#FFFFFF",
            padding=(15, 8),
            font=("Segoe UI", 10)
        )
        
        # Positionner le label en bas de la fenêtre
        confirmation.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        
        # Programmer la disparition du label après 2 secondes
        self.after(2000, lambda: confirmation.destroy())
    
    def on_close(self, force_quit=False):
        """Gère la fermeture de l'application"""
        # Si force_quit est True, quitter directement sans minimiser
        if not force_quit and self.minimize_var.get() and hasattr(self, 'tray_icon') and self.tray_icon.is_available() and not self.winfo_toplevel().wm_state() == 'iconic':
            # Minimiser dans la barre des tâches au lieu de quitter
            self.withdraw()
            return
        
        # Confirmation avant de quitter si la surveillance est active
        if self.is_running:
            confirm = messagebox.askyesno(
                "NightMod", 
                "La surveillance est en cours. Voulez-vous vraiment quitter NightMod ?"
            )
            if not confirm:
                return
        
        # Arrêter la surveillance
        self.is_running = False
        
        # Supprimer l'icône de la barre des tâches si elle existe
        if hasattr(self, 'tray_icon') and self.tray_icon:
            self.tray_icon.stop()
        
        # Fermer l'application
        self.destroy()