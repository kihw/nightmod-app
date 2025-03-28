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
        """Configure la fenêtre principale de l'application"""
        self.title("NightMod")
        self.geometry("550x550")  # Augmentation significative de la hauteur et largeur
        self.minsize(550, 550)    # Augmentation significative des dimensions minimales
        
        # Style et thème
        self.style = ttk.Style()
        
        # Appliquer un thème moderne si disponible
        self.configure_theme()
        
        # Icône de l'application
        self.set_application_icon()
        
        # Gestion de la fermeture
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Raccourcis clavier
        self.bind("<Alt-q>", lambda e: self.on_close())
        self.bind("<Alt-n>", lambda e: self.toggle_visibility())
    
    def configure_theme(self):
        """Configure le thème de l'interface utilisateur"""
        if platform.system() == "Windows":
            # Utiliser le thème par défaut de Windows si disponible
            try:
                theme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "themes/azure.tcl")
                if os.path.exists(theme_path):
                    self.tk.call("source", theme_path)
                    self.tk.call("set_theme", "dark")
                else:
                    # Utiliser un style personnalisé simple
                    self.configure(bg="#2E2E2E")
                    self.style.configure("TFrame", background="#2E2E2E")
                    self.style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
                    self.style.configure("TButton", padding=6)
                    self.style.configure("Accent.TButton", background="#0078D7")
            except Exception as e:
                logger.warning(f"Impossible de configurer le thème: {e}")
                # Utiliser un style personnalisé simple en cas d'erreur
                self.configure(bg="#2E2E2E")
                self.style.configure("TFrame", background="#2E2E2E")
                self.style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
                self.style.configure("TButton", padding=6)
                self.style.configure("Accent.TButton", background="#0078D7")
        else:
            # Style personnalisé pour macOS et Linux
            self.configure(bg="#2E2E2E")
            self.style.configure("TFrame", background="#2E2E2E")
            self.style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
            self.style.configure("TButton", padding=6)
            self.style.configure("Accent.TButton", background="#0078D7")
    
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
        main_frame = ttk.Frame(self, padding="25 25 25 35")  # Augmentation significative du padding
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # En-tête
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            header_frame, 
            text="NightMod", 
            font=("Segoe UI", 18, "bold")
        ).pack(side=tk.LEFT)
        
        # État actuel
        self.status_var = tk.StringVar(value="Inactif")
        self.next_check_var = tk.StringVar(value="Aucune vérification prévue")
        
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            status_frame, 
            text="État:", 
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        ttk.Label(
            status_frame, 
            textvariable=self.status_var
        ).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(
            status_frame, 
            text="Prochaine vérification:", 
            font=("Segoe UI", 10, "bold")
        ).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        
        ttk.Label(
            status_frame, 
            textvariable=self.next_check_var
        ).grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Paramètres
        settings_frame = ttk.LabelFrame(main_frame, text="Paramètres", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Intervalle de vérification
        ttk.Label(
            settings_frame, 
            text="Intervalle entre les vérifications (minutes):"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.check_interval_var = tk.IntVar(value=self.config.get("check_interval_minutes", 20))
        interval_spinner = ttk.Spinbox(
            settings_frame, 
            from_=5, 
            to=120, 
            width=5, 
            textvariable=self.check_interval_var
        )
        interval_spinner.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Temps de réponse
        ttk.Label(
            settings_frame, 
            text="Temps de réponse maximum (secondes):"
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.response_time_var = tk.IntVar(value=self.config.get("response_time_seconds", 30))
        response_spinner = ttk.Spinbox(
            settings_frame, 
            from_=15, 
            to=60, 
            width=5, 
            textvariable=self.response_time_var
        )
        response_spinner.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Action en cas d'inactivité
        ttk.Label(
            settings_frame, 
            text="Action en cas d'inactivité:"
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.action_var = tk.StringVar(value=self.config.get("shutdown_action", "shutdown"))
        action_combo = ttk.Combobox(
            settings_frame, 
            width=15, 
            textvariable=self.action_var, 
            state="readonly"
        )
        action_combo["values"] = ("shutdown", "sleep", "lock")
        action_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Son activé
        self.sound_var = tk.BooleanVar(value=self.config.get("sound_enabled", True))
        sound_check = ttk.Checkbutton(
            settings_frame, 
            text="Activer le son de notification", 
            variable=self.sound_var
        )
        sound_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Démarrage automatique
        self.autostart_var = tk.BooleanVar(value=self.config.get("start_with_system", False))
        autostart_check = ttk.Checkbutton(
            settings_frame, 
            text="Démarrer la surveillance automatiquement", 
            variable=self.autostart_var
        )
        autostart_check.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Minimiser dans la barre des tâches
        self.minimize_var = tk.BooleanVar(value=self.config.get("minimize_to_tray", True))
        minimize_check = ttk.Checkbutton(
            settings_frame, 
            text="Minimiser dans la barre des tâches", 
            variable=self.minimize_var
        )
        minimize_check.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Information sur la compatibilité
        if hasattr(self, 'tray_icon') and not self.tray_icon.is_available():
            info_label = ttk.Label(
                settings_frame,
                text="Note: L'option de barre des tâches nécessite pystray et pillow.",
                font=("Segoe UI", 8, "italic"),
                foreground="#AAAAAA"
            )
            info_label.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Modifier la présentation pour utiliser grid au lieu de pack pour les boutons
        # afin d'assurer plus d'espace et une meilleure visibilité
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(25, 15))
        
        # Organisation des boutons en grille plutôt qu'en ligne
        self.start_button = ttk.Button(
            action_frame, 
            text="Démarrer la surveillance",
            command=self.toggle_monitoring,
            style="Accent.TButton",
            width=25  # Fixer la largeur du bouton
        )
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Button(
            action_frame, 
            text="Appliquer les paramètres",
            command=self.save_settings,
            width=25  # Fixer la largeur du bouton
        ).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(
            action_frame,
            text="Tester la vérification",
            command=self.test_popup,
            width=25  # Fixer la largeur du bouton
        ).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Informations de version
        version_frame = ttk.Frame(main_frame)
        version_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(40, 0))  # Augmentation significative du padding supérieur
        
        ttk.Label(
            version_frame, 
            text="NightMod v1.0.0", 
            font=("Segoe UI", 8)
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            version_frame, 
            text="© 2025", 
            font=("Segoe UI", 8)
        ).pack(side=tk.RIGHT)
    
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
        
        # Exécuter l'action configurée
        action = self.config.get("shutdown_action", "shutdown")
        
        # Afficher un message d'avertissement avant d'exécuter l'action
        message = "Aucune réponse détectée. "
        
        if action == "shutdown":
            message += "L'ordinateur va s'éteindre dans 10 secondes."
        elif action == "sleep":
            message += "L'ordinateur va se mettre en veille."
        elif action == "lock":
            message += "L'écran va être verrouillé."
        
        # Afficher un message final à l'utilisateur
        try:
            messagebox.showwarning("NightMod - Action imminente", message)
            self.update()  # Mettre à jour l'interface pour afficher le message
            
            # Attendre quelques secondes pour que l'utilisateur puisse voir le message
            time.sleep(5)
            
            # Exécuter l'action
            SystemActions.perform_action(action)
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de l'action: {e}")
            logger.error(traceback.format_exc())
    
    def save_settings(self):
        """Sauvegarde les paramètres actuels"""
        # Récupérer les valeurs depuis l'interface
        self.config["check_interval_minutes"] = self.check_interval_var.get()
        self.config["response_time_seconds"] = self.response_time_var.get()
        self.config["shutdown_action"] = self.action_var.get()
        self.config["sound_enabled"] = self.sound_var.get()
        self.config["start_with_system"] = self.autostart_var.get()
        self.config["minimize_to_tray"] = self.minimize_var.get()
        
        # Sauvegarder la configuration
        if self.config_manager.update(self.config):
            messagebox.showinfo("NightMod", "Paramètres enregistrés avec succès.")
            
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
    
    def on_close(self):
        """Gère la fermeture de l'application"""
        if self.minimize_var.get() and hasattr(self, 'tray_icon') and self.tray_icon.is_available() and not self.winfo_toplevel().wm_state() == 'iconic':
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