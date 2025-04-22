import tkinter as tk
from tkinter import ttk, messagebox
import os
import platform
import logging
import threading
import time
from datetime import datetime

from src.config import ConfigManager
from src.popup import PopupChecker
from src.system_actions import SystemActions
from src.tray import TrayIcon
from src.styles import apply_custom_styles
from src.monitoring import MonitoringManager

# Définir le logger
logger = logging.getLogger("NightMod.App")

class NightModApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_all()

        # Configuration de la fenêtre principale
        self.setup_main_window()
        
        # Configuration de l'interface utilisateur
        self.setup_ui()
        
        # Initialisation du gestionnaire de surveillance
        self.is_monitoring = False
        self.next_check_time = None
        self.monitoring_manager = MonitoringManager(
            self, 
            self.config,
            self.on_user_response,
            self.on_no_response
        )
        
        # Création de l'icône dans la barre des tâches
        self.tray_icon = TrayIcon(
            self,
            self.toggle_visibility,
            self.toggle_monitoring,
            self.on_close
        )
        self.tray_icon.setup()

        # Démarrage automatique de la surveillance si configuré
        if self.config.get("start_with_system", False):
            self.toggle_monitoring()
            
        # Protocole de fermeture de la fenêtre
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_main_window(self):
        """Configuration de la fenêtre principale"""
        self.title("NightMod")
        self.geometry("480x520")
        self.minsize(480, 520)

        # Centre la fenêtre sur l'écran
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 480) // 2
        y = (screen_height - 520) // 2
        self.geometry(f"+{x}+{y}")

        # Configuration du thème et du style
        self.configure(bg="#1a1a1a")
        self.style = ttk.Style(self)
        apply_custom_styles(self.style)
        
        # Configuration de l'icône de l'application
        self.set_application_icon()
        
        # Raccourcis clavier
        self.bind("<Alt-q>", lambda e: self.on_close())
        self.bind("<Alt-n>", lambda e: self.toggle_visibility())

    def set_application_icon(self):
        """Définit l'icône de l'application selon la plateforme"""
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/icon.png")
            if platform.system() == "Windows":
                ico_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/icon.ico")
                if os.path.exists(ico_path):
                    self.iconbitmap(ico_path)
            elif os.path.exists(icon_path):
                from PIL import Image, ImageTk
                img = Image.open(icon_path).resize((64, 64))
                icon = ImageTk.PhotoImage(img)
                self.iconphoto(True, icon)
        except Exception as e:
            logger.warning(f"Impossible de charger l'icône: {e}")

    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        # Frame principale avec padding
        self.main_frame = ttk.Frame(self, padding="30 35 30 35")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame d'état
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Indicateur visuel d'état (point coloré)
        self.status_indicator = ttk.Label(
            status_frame,
            text="●",
            font=("Segoe UI", 14),
            foreground="#888888"
        )
        self.status_indicator.grid(row=0, column=0, padx=(0, 15))
        
        # Étiquettes d'état
        ttk.Label(status_frame, text="État").grid(row=0, column=1, sticky=tk.W)
        
        self.status_var = tk.StringVar(value="Inactif")
        ttk.Label(status_frame, textvariable=self.status_var).grid(row=0, column=2, sticky=tk.W, padx=10)
        
        # Frame pour le temps avant la prochaine vérification
        time_frame = ttk.Frame(self.main_frame)
        time_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(time_frame, text="Prochaine vérification:").grid(row=0, column=0, sticky=tk.W)
        
        self.next_check_var = tk.StringVar(value="Aucune vérification prévue")
        ttk.Label(time_frame, textvariable=self.next_check_var).grid(row=0, column=1, sticky=tk.W, padx=10)
        
        # Séparateur
        ttk.Separator(self.main_frame).pack(fill=tk.X, pady=15)
        
        # Frame pour les contrôles principaux
        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.pack(pady=20)
        
        # Bouton de surveillance - utiliser un bouton standard au lieu de ttk
        self.monitoring_button = tk.Button(
            controls_frame,
            text="Démarrer la surveillance",
            command=self.toggle_monitoring,
            width=30,
            padx=10,
            pady=5
        )
        self.monitoring_button.pack(pady=5)
        
        # Séparateur
        ttk.Separator(self.main_frame).pack(fill=tk.X, pady=15)
        
        # Frame pour les paramètres
        settings_frame = ttk.Frame(self.main_frame)
        settings_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(settings_frame, text="Paramètres", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W)
        
        # Frame pour l'intervalle entre les vérifications
        interval_frame = ttk.Frame(settings_frame)
        interval_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(interval_frame, text="Intervalle entre les vérifications (minutes):").grid(row=0, column=0, sticky=tk.W)
        
        self.interval_var = tk.StringVar(value=str(self.config.get("check_interval_minutes", 20)))
        # Utiliser un widget Entry standard au lieu de Spinbox
        interval_entry = tk.Entry(
            interval_frame,
            textvariable=self.interval_var,
            width=5
        )
        interval_entry.grid(row=0, column=1, padx=10)
        interval_entry.bind("<FocusOut>", self.save_settings)
        
        # Frame pour le temps de réponse
        response_frame = ttk.Frame(settings_frame)
        response_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(response_frame, text="Temps de réponse maximum (secondes):").grid(row=0, column=0, sticky=tk.W)
        
        self.response_var = tk.StringVar(value=str(self.config.get("response_time_seconds", 30)))
        # Utiliser un widget Entry standard au lieu de Spinbox
        response_entry = tk.Entry(
            response_frame,
            textvariable=self.response_var,
            width=5
        )
        response_entry.grid(row=0, column=1, padx=10)
        response_entry.bind("<FocusOut>", self.save_settings)
        
        # Frame pour l'action en cas d'inactivité
        action_frame = ttk.Frame(settings_frame)
        action_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(action_frame, text="Action en cas d'inactivité:").grid(row=0, column=0, sticky=tk.W)
        
        self.action_var = tk.StringVar(value=self.config.get("shutdown_action", "shutdown"))
        # Utiliser un OptionMenu standard au lieu de Combobox
        action_options = ["shutdown", "sleep", "lock"]
        action_menu = tk.OptionMenu(
            action_frame,
            self.action_var,
            *action_options
        )
        action_menu.config(width=10)
        action_menu.grid(row=0, column=1, padx=10)
        self.action_var.trace("w", lambda *args: self.save_settings())
        
        # Options supplémentaires
        options_frame = ttk.Frame(settings_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        # Option pour le son de notification - utiliser Checkbutton standard
        self.sound_var = tk.BooleanVar(value=self.config.get("sound_enabled", True))
        sound_check = tk.Checkbutton(
            options_frame,
            text="Activer le son de notification",
            variable=self.sound_var,
            command=self.save_settings
        )
        sound_check.pack(anchor=tk.W, pady=2)
        
        # Option pour démarrer la surveillance automatiquement
        self.autostart_var = tk.BooleanVar(value=self.config.get("start_with_system", False))
        autostart_check = tk.Checkbutton(
            options_frame,
            text="Démarrer la surveillance automatiquement",
            variable=self.autostart_var,
            command=self.save_settings
        )
        autostart_check.pack(anchor=tk.W, pady=2)
        
        # Option pour minimiser dans la barre des tâches
        self.minimize_var = tk.BooleanVar(value=self.config.get("minimize_to_tray", True))
        minimize_check = tk.Checkbutton(
            options_frame,
            text="Minimiser dans la barre des tâches",
            variable=self.minimize_var,
            command=self.save_settings
        )
        minimize_check.pack(anchor=tk.W, pady=2)
        
        # Appliquer les couleurs à tous les widgets créés
        if hasattr(apply_custom_styles, 'fix_widget_colors'):
            for widget in self.winfo_children():
                apply_custom_styles.fix_widget_colors(widget)

    def save_settings(self, event=None):
        """Sauvegarde les paramètres dans le fichier de configuration"""
        try:
            # Récupérer les valeurs des widgets
            new_config = {
                "check_interval_minutes": int(self.interval_var.get()),
                "response_time_seconds": int(self.response_var.get()),
                "shutdown_action": self.action_var.get(),
                "sound_enabled": self.sound_var.get(),
                "start_with_system": self.autostart_var.get(),
                "minimize_to_tray": self.minimize_var.get()
            }
            
            # Mettre à jour la configuration
            self.config_manager.update(new_config)
            self.config = self.config_manager.get_all()
            
            # Mettre à jour l'autostart système si nécessaire
            try:
                SystemActions.configure_autostart(self.autostart_var.get())
            except Exception as e:
                logger.warning(f"Impossible de configurer le démarrage automatique: {e}")
            
            logger.info("Paramètres sauvegardés")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des paramètres: {e}")
            messagebox.showerror("Erreur", f"Impossible de sauvegarder les paramètres: {e}")

    def toggle_monitoring(self):
        """Démarre ou arrête la surveillance"""
        if self.is_monitoring:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def start_monitoring(self):
        """Démarre la surveillance"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        
        # Démarrer la surveillance via le gestionnaire
        self.monitoring_manager.start_monitoring()
        
        # Mettre à jour l'interface
        self.update_status("Actif", True)
        self.monitoring_button.config(text="Arrêter la surveillance", bg="#F44336", fg="#FFFFFF")
        
        # Mettre à jour l'icône de la barre des tâches
        if self.tray_icon:
            self.tray_icon.update_icon(True)
            
        # Démarrer la mise à jour périodique de l'affichage
        self.schedule_display_update()
            
        logger.info("Surveillance démarrée")

    def stop_monitoring(self):
        """Arrête la surveillance"""
        self.is_monitoring = False
        
        # Arrêter la surveillance via le gestionnaire
        self.monitoring_manager.stop_monitoring()
        
        # Mettre à jour l'interface
        self.update_status("Inactif", False)
        self.monitoring_button.config(text="Démarrer la surveillance", bg="#4CAF50", fg="#FFFFFF")
        self.next_check_var.set("Aucune vérification prévue")
        
        # Mettre à jour l'icône de la barre des tâches
        if self.tray_icon:
            self.tray_icon.update_icon(False)
            
        logger.info("Surveillance arrêtée")
    
    def schedule_display_update(self):
        """Programme la mise à jour périodique de l'affichage"""
        if self.is_monitoring:
            self.update_next_check_time()
            self.after(1000, self.schedule_display_update)
    
    def update_next_check_time(self):
        """Met à jour l'affichage du temps avant la prochaine vérification"""
        next_time = self.monitoring_manager.next_check_time
        
        if not next_time:
            self.next_check_var.set("Aucune vérification prévue")
            return
            
        # Calculer le temps restant
        remaining = max(0, int(next_time - datetime.now().timestamp()))
        minutes = remaining // 60
        seconds = remaining % 60
        
        # Mettre à jour l'affichage
        if minutes > 0:
            self.next_check_var.set(f"Dans {minutes} min {seconds} sec")
        else:
            self.next_check_var.set(f"Dans {seconds} secondes")

    def update_status(self, status, active=False):
        """Met à jour l'affichage de l'état"""
        self.status_var.set(status)
        self.status_indicator.config(foreground="#4CAF50" if active else "#888888")

    def toggle_visibility(self):
        """Affiche ou masque la fenêtre principale"""
        if self.state() == 'withdrawn':
            self.deiconify()
            self.lift()
        else:
            if self.minimize_var.get() and self.tray_icon and self.tray_icon.is_available():
                self.withdraw()
    
    def on_user_response(self):
        """Appelé lorsque l'utilisateur répond au popup"""
        logger.info("L'utilisateur a répondu au popup")
        # Rien à faire ici, la surveillance continue normalement
    
    def on_no_response(self):
        """Appelé lorsque l'utilisateur ne répond pas au popup"""
        logger.info("Aucune réponse de l'utilisateur, arrêt de la surveillance")
        # Arrêter la surveillance
        self.stop_monitoring()
    
    def confirm_quit(self):
        """Demande confirmation avant de quitter si la surveillance est active"""
        if self.is_monitoring:
            return messagebox.askyesno(
                "NightMod",
                "La surveillance est en cours. Voulez-vous vraiment quitter NightMod ?"
            )
        return True

    def on_close(self):
        """Gère la fermeture de l'application"""
        if not self.confirm_quit():
            return
            
        # Arrêter la surveillance si elle est active
        if self.is_monitoring:
            self.stop_monitoring()
            
        # Arrêter l'icône de la barre des tâches
        if self.tray_icon:
            self.tray_icon.stop()
            
        # Fermer l'application
        self.destroy()


if __name__ == "__main__":
    app = NightModApp()
    app.mainloop()