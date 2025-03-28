#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NightMod - Surveillant de sommeil et économiseur d'énergie

Ce programme vérifie périodiquement si l'utilisateur est encore éveillé en affichant
une fenêtre popup. Si l'utilisateur ne répond pas, l'ordinateur est éteint.
"""

import os
import sys
import time
import json
import threading
import logging
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import platform

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("nightmod.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NightMod")

# Configuration par défaut
DEFAULT_CONFIG = {
    "check_interval_minutes": 20,
    "response_time_seconds": 30,
    "shutdown_action": "shutdown",  # Options: shutdown, sleep, lock
    "sound_enabled": True,
    "start_with_system": False,
    "minimize_to_tray": True
}

class PopupChecker(tk.Toplevel):
    """Fenêtre popup qui vérifie si l'utilisateur est éveillé"""
    
    def __init__(self, parent, response_time, on_response, on_timeout):
        super().__init__(parent)
        self.parent = parent
        self.response_time = response_time
        self.on_response = on_response
        self.on_timeout = on_timeout
        self.remaining_time = response_time
        
        # Configuration de la fenêtre
        self.title("NightMod - Vérification")
        self.geometry("400x200")
        self.resizable(False, False)
        self.configure(background="#2E2E2E")
        
        # Toujours au premier plan et centré
        self.attributes("-topmost", True)
        self.withdraw()  # Masquer d'abord
        self.update_idletasks()
        
        # Centrer la fenêtre sur l'écran
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"+{x}+{y}")
        
        self.deiconify()  # Afficher après le centrage
        
        # Jouer un son si activé
        if parent.config.get("sound_enabled", True):
            self.bell()
        
        # Éléments d'interface
        self.create_widgets()
        
        # Démarrer le compte à rebours
        self.countdown()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message principal
        ttk.Label(
            main_frame, 
            text="Êtes-vous encore éveillé ?", 
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)
        
        # Texte du compte à rebours
        self.time_label = ttk.Label(
            main_frame, 
            text=f"Temps restant: {self.remaining_time} secondes",
            font=("Segoe UI", 10)
        )
        self.time_label.pack(pady=10)
        
        # Bouton de réponse
        response_button = ttk.Button(
            main_frame, 
            text="Je suis éveillé",
            command=self.handle_response,
            style="Accent.TButton"
        )
        response_button.pack(pady=10)
        response_button.focus_set()
        
        # Gérer la touche Échap pour fermer
        self.bind("<Escape>", lambda e: self.handle_response())
        
        # Intercepter la fermeture de la fenêtre
        self.protocol("WM_DELETE_WINDOW", self.handle_response)
    
    def countdown(self):
        """Gère le compte à rebours et vérifie si le temps est écoulé"""
        if self.remaining_time > 0:
            self.time_label.config(text=f"Temps restant: {self.remaining_time} secondes")
            self.remaining_time -= 1
            self.after(1000, self.countdown)
        else:
            logger.info("Aucune réponse reçue dans le délai imparti")
            self.destroy()
            self.on_timeout()
    
    def handle_response(self, event=None):
        """Appelé quand l'utilisateur répond au popup"""
        logger.info("Réponse reçue de l'utilisateur")
        self.destroy()
        self.on_response()


class SystemActions:
    """Classe utilitaire pour les actions système (extinction, veille, etc.)"""
    
    @staticmethod
    def shutdown():
        """Éteint l'ordinateur"""
        logger.info("Extinction de l'ordinateur...")
        
        try:
            if platform.system() == "Windows":
                os.system("shutdown /s /t 10 /c \"NightMod: Extinction automatique\"")
            elif platform.system() == "Darwin":  # macOS
                os.system("osascript -e 'tell app \"System Events\" to shut down'")
            else:  # Linux et autres Unix
                os.system("shutdown -h now")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'extinction: {e}")
            return False
    
    @staticmethod
    def sleep():
        """Met l'ordinateur en veille"""
        logger.info("Mise en veille de l'ordinateur...")
        
        try:
            if platform.system() == "Windows":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif platform.system() == "Darwin":  # macOS
                os.system("pmset sleepnow")
            else:  # Linux
                os.system("systemctl suspend")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la mise en veille: {e}")
            return False
    
    @staticmethod
    def lock():
        """Verrouille l'écran"""
        logger.info("Verrouillage de l'écran...")
        
        try:
            if platform.system() == "Windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
            elif platform.system() == "Darwin":  # macOS
                os.system("pmset displaysleepnow")
            else:  # Linux
                os.system("loginctl lock-session")
            return True
        except Exception as e:
            logger.error(f"Erreur lors du verrouillage: {e}")
            return False
    
    @staticmethod
    def perform_action(action):
        """Exécute l'action spécifiée"""
        actions = {
            "shutdown": SystemActions.shutdown,
            "sleep": SystemActions.sleep,
            "lock": SystemActions.lock
        }
        
        if action in actions:
            return actions[action]()
        else:
            logger.error(f"Action non reconnue: {action}")
            return False


class ConfigManager:
    """Gère la configuration et la persiste sur le disque"""
    
    def __init__(self, config_file="nightmod_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Charge la configuration depuis le fichier ou retourne la configuration par défaut"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Fusionner avec les paramètres par défaut pour les nouvelles options
                    return {**DEFAULT_CONFIG, **config}
            return DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la configuration: {e}")
            return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Sauvegarde la configuration dans le fichier"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la configuration: {e}")
            return False
    
    def get(self, key, default=None):
        """Récupère une valeur de configuration avec une valeur par défaut"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Définit une valeur de configuration et la sauvegarde"""
        self.config[key] = value
        return self.save_config()


class NightModApp(tk.Tk):
    """Application principale NightMod"""
    
    def __init__(self):
        super().__init__()
        
        # Chargement de la configuration
        self.config_manager = ConfigManager()
        self.config = self.config_manager.config
        
        # Variables d'état
        self.is_running = False
        self.timer_thread = None
        self.next_check_time = None
        
        # Configuration de la fenêtre principale
        self.setup_main_window()
        
        # Initialisation de l'interface utilisateur
        self.setup_ui()
        
        # Configuration du système de notification
        self.setup_system_tray()
        
        # Démarre automatiquement la surveillance si configuré
        if self.config.get("start_with_system", False):
            self.start_monitoring()
    
    def setup_main_window(self):
        """Configure la fenêtre principale de l'application"""
        self.title("NightMod")
        self.geometry("500x400")
        self.minsize(500, 400)
        
        # Style et thème
        self.style = ttk.Style()
        
        if platform.system() == "Windows":
            # Utiliser le thème par défaut de Windows si disponible
            try:
                from tkinter import _tkinter
                self.tk.call("source", "azure.tcl")
                self.tk.call("set_theme", "dark")
            except Exception:
                # Utiliser un style personnalisé simple
                self.configure(bg="#2E2E2E")
                self.style.configure("TFrame", background="#2E2E2E")
                self.style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
                self.style.configure("TButton", padding=6)
                self.style.configure("Accent.TButton", background="#0078D7")
        
        # Icône de l'application
        try:
            if platform.system() == "Windows":
                self.iconbitmap("assets/icon.ico")
            else:
                icon = tk.PhotoImage(file="assets/icon.png")
                self.iconphoto(True, icon)
        except Exception as e:
            logger.warning(f"Impossible de charger l'icône: {e}")
        
        # Gestion de la fermeture
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Raccourcis clavier
        self.bind("<Alt-q>", lambda e: self.on_close())
        self.bind("<Alt-n>", lambda e: self.toggle_visibility())
    
    def setup_ui(self):
        """Configure l'interface utilisateur principale"""
        main_frame = ttk.Frame(self, padding="20")
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
        
        # Boutons d'action
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=20)
        
        self.start_button = ttk.Button(
            action_frame, 
            text="Démarrer la surveillance",
            command=self.toggle_monitoring,
            style="Accent.TButton"
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            action_frame, 
            text="Appliquer les paramètres",
            command=self.save_settings
        ).pack(side=tk.LEFT)
        
        # Informations de version
        version_frame = ttk.Frame(main_frame)
        version_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
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
    
    def setup_system_tray(self):
        """Configure l'icône dans la barre des tâches si disponible"""
        try:
            # Cette fonctionnalité nécessite pystray, qui est optionnel
            import pystray
            from PIL import Image, ImageDraw
            
            # Créer une icône simple si aucune n'est disponible
            icon_image = None
            try:
                icon_image = Image.open("assets/icon.png")
            except:
                # Créer une icône de secours
                icon_image = Image.new('RGB', (64, 64), color=(47, 47, 47))
                d = ImageDraw.Draw(icon_image)
                d.rectangle((10, 10, 54, 54), fill=(0, 120, 215))
            
            # Définir le menu
            menu = pystray.Menu(
                pystray.MenuItem("Afficher/Masquer", self.toggle_visibility),
                pystray.MenuItem("Démarrer/Arrêter", self.toggle_monitoring),
                pystray.MenuItem("Quitter", self.on_close)
            )
            
            # Créer l'icône
            self.tray_icon = pystray.Icon("nightmod", icon_image, "NightMod", menu)
            
            # Démarrer l'icône dans un thread
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
            
            # Si configuré pour minimiser dans la barre des tâches au démarrage
            if self.config.get("minimize_to_tray", True):
                self.after(1000, self.withdraw)
        
        except ImportError:
            logger.warning("pystray non installé, fonctionnalité de barre des tâches désactivée")
            self.tray_icon = None
    
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
        
        # Démarrer le thread de surveillance
        self.timer_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.timer_thread.start()
        
        logger.info("Surveillance démarrée")
        
        # Minimiser dans la barre des tâches si configuré
        if self.config.get("minimize_to_tray", True) and self.tray_icon:
            self.withdraw()
    
    def stop_monitoring(self):
        """Arrête le processus de surveillance"""
        self.is_running = False
        self.status_var.set("Inactif")
        self.next_check_var.set("Aucune vérification prévue")
        self.start_button.config(text="Démarrer la surveillance")
        self.next_check_time = None
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
        self.next_check_var.set(f"Dans {time_str}")
    
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
            self.on_no_response
        )
    
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
        if self.config_manager.save_config():
            messagebox.showinfo("NightMod", "Paramètres enregistrés avec succès.")
            
            # Configurer le démarrage automatique avec le système si nécessaire
            self.configure_autostart()
        else:
            messagebox.showerror("NightMod", "Erreur lors de l'enregistrement des paramètres.")
    
    def configure_autostart(self):
        """Configure le démarrage automatique au démarrage du système"""
        autostart = self.config.get("start_with_system", False)
        
        try:
            if platform.system() == "Windows":
                import winreg
                
                # Chemin du registre pour le démarrage automatique
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                
                # Ouvrir la clé de registre
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, 
                    key_path, 
                    0, 
                    winreg.KEY_SET_VALUE
                )
                
                if autostart:
                    # Ajouter au démarrage automatique
                    winreg.SetValueEx(
                        key, 
                        "NightMod", 
                        0, 
                        winreg.REG_SZ, 
                        sys.executable + " " + os.path.abspath(__file__)
                    )
                else:
                    # Supprimer du démarrage automatique
                    try:
                        winreg.DeleteValue(key, "NightMod")
                    except FileNotFoundError:
                        pass  # La clé n'existe pas, c'est normal
                
                winreg.CloseKey(key)
            
            elif platform.system() == "Darwin":  # macOS
                # Chemin vers le répertoire de démarrage
                launch_dir = os.path.expanduser("~/Library/LaunchAgents")
                plist_path = os.path.join(launch_dir, "com.nightmod.startup.plist")
                
                if autostart:
                    # Créer le répertoire s'il n'existe pas
                    os.makedirs(launch_dir, exist_ok=True)
                    
                    # Créer le fichier plist
                    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nightmod.startup</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{os.path.abspath(__file__)}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""
                    
                    with open(plist_path, "w") as f:
                        f.write(plist_content)
                else:
                    # Supprimer le fichier plist s'il existe
                    if os.path.exists(plist_path):
                        os.remove(plist_path)
            
            elif platform.system() == "Linux":
                # Chemin vers le répertoire de démarrage
                autostart_dir = os.path.expanduser("~/.config/autostart")
                desktop_path = os.path.join(autostart_dir, "nightmod.desktop")
                
                if autostart:
                    # Créer le répertoire s'il n'existe pas
                    os.makedirs(autostart_dir, exist_ok=True)
                    
                    # Créer le fichier .desktop
                    desktop_content = f"""[Desktop Entry]
Type=Application
Name=NightMod
Comment=Surveillant de sommeil et économiseur d'énergie
Exec={sys.executable} {os.path.abspath(__file__)}
Terminal=false
Categories=Utility;"""
                    
                    with open(desktop_path, "w") as f:
                        f.write(desktop_content)
                    
                    # Rendre le fichier exécutable
                    os.chmod(desktop_path, 0o755)
                else:
                    # Supprimer le fichier .desktop s'il existe
                    if os.path.exists(desktop_path):
                        os.remove(desktop_path)
        
        except Exception as e:
            logger.error(f"Erreur lors de la configuration du démarrage automatique: {e}")
            messagebox.showwarning(
                "NightMod", 
                "Impossible de configurer le démarrage automatique. "
                "Veuillez le faire manuellement."
            )
    
    def on_close(self):
        """Gère la fermeture de l'application"""
        if self.minimize_var.get() and self.tray_icon:
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


def main():
    """Point d'entrée principal de l'application"""
    try:
        app = NightModApp()
        app.mainloop()
    except Exception as e:
        logger.critical(f"Erreur critique lors de l'exécution de l'application: {e}")
        messagebox.showerror(
            "NightMod - Erreur critique",
            f"Une erreur critique s'est produite:\n\n{str(e)}\n\nConsultez le fichier de log pour plus d'informations."
        )


if __name__ == "__main__":
    main()