import tkinter as tk
from tkinter import font as tkfont, messagebox
import threading
import os
import sys
import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageTk

# Configuration avec valeurs par défaut
CONFIG_FILE = Path.home() / "mode_nuit_config.json"
DEFAULT_CONFIG = {
    "countdown_time": 60,      # Temps du compte à rebours en secondes
    "interval": 2700,          # Interval par défaut (45 minutes)
    "theme": {
        "bg_color": "#000000", # Noir
        "fg_color": "#FFFFFF", # Blanc
        "accent_color": "#304FFE" # Bleu accent
    },
    "language": "fr",          # Langue par défaut
    "auto_start": False        # Démarrage automatique
}

# Traductions
TRANSLATIONS = {
    "fr": {
        "app_name": "Mode Nuit",
        "are_you_sleeping": "Dormez-vous?",
        "no": "Non",
        "time_remaining": "Temps restant: {} s",
        "quit": "Quitter",
        "settings": "Paramètres",
        "start": "Démarrer",
        "restart": "Redémarrer",
        "pause": "Pause"
    },
    "en": {
        "app_name": "Night Mode",
        "are_you_sleeping": "Are you sleeping?",
        "no": "No",
        "time_remaining": "Time remaining: {} s",
        "quit": "Quit",
        "settings": "Settings",
        "start": "Start",
        "restart": "Restart",
        "pause": "Pause"
    }
}

class Config:
    """Gestionnaire de configuration"""
    
    def __init__(self):
        self.config = DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self):
        """Charge la configuration depuis le fichier"""
        try:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, 'r') as f:
                    user_config = json.load(f)
                    # Mise à jour avec les valeurs utilisateur
                    self.update_config(user_config)
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            
    def update_config(self, new_config):
        """Met à jour la configuration de manière récursive"""
        for key, value in new_config.items():
            if isinstance(value, dict) and key in self.config and isinstance(self.config[key], dict):
                # Pour les dictionnaires imbriqués comme 'theme'
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def save_config(self):
        """Sauvegarde la configuration dans un fichier"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la configuration: {e}")
    
    def get(self, key, default=None):
        """Récupère une valeur de configuration"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key, value):
        """Définit une valeur de configuration"""
        keys = key.split('.')
        conf = self.config
        for i, k in enumerate(keys[:-1]):
            if k not in conf:
                conf[k] = {}
            conf = conf[k]
        conf[keys[-1]] = value
        self.save_config()


class CustomTitleBar(tk.Frame):
    """Barre de titre personnalisée pour les fenêtres"""
    
    def __init__(self, parent, config, text, on_close=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.config = config
        self.on_close = on_close if on_close else self.close_window
        
        # Couleurs de thème
        bg_color = self.config.get('theme.bg_color')
        fg_color = self.config.get('theme.fg_color')
        accent_color = self.config.get('theme.accent_color')
        
        self.configure(bg=bg_color)
        
        # Titre
        self.title_label = tk.Label(
            self, 
            text=text, 
            bg=bg_color, 
            fg=fg_color, 
            font=tkfont.Font(weight="bold", size=16)
        )
        self.title_label.pack(side="left", padx=20, pady=10)
        
        # Bouton de fermeture
        self.close_button = tk.Button(
            self, 
            text="×", 
            command=self.on_close, 
            bg=bg_color, 
            fg=accent_color, 
            activebackground=bg_color,
            activeforeground=fg_color,
            borderwidth=0, 
            font=tkfont.Font(weight="bold", size=20)
        )
        self.close_button.pack(side="right", padx=10, pady=10)
        
        # Gestion du déplacement de la fenêtre
        for widget in (self, self.title_label):
            widget.bind("<B1-Motion>", self.move_window)
            widget.bind("<Button-1>", self.click_window)
    
    def close_window(self):
        """Ferme la fenêtre parente"""
        self.parent.destroy()
    
    def click_window(self, event):
        """Enregistre la position initiale lors du clic pour le déplacement"""
        self.x = event.x
        self.y = event.y
    
    def move_window(self, event):
        """Déplace la fenêtre en fonction de la position de la souris"""
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.parent.geometry(f"+{x}+{y}")


class CountdownApp:
    """Application principale de compte à rebours"""
    
    def __init__(self, root, stop_event, config, tray_icon=None, icon_path=None):
        self.root = root
        self.stop_event = stop_event
        self.config = config
        self.tray_icon = tray_icon
        self.icon_path = icon_path
        self.paused = False
        
        # Récupération des paramètres
        self.countdown_time = self.config.get('countdown_time')
        self.interval = self.config.get('interval')
        self.lang = self.config.get('language')
        self.bg_color = self.config.get('theme.bg_color')
        self.fg_color = self.config.get('theme.fg_color')
        self.accent_color = self.config.get('theme.accent_color')
        
        # Configuration de la fenêtre
        self.root.overrideredirect(True)
        self.root.configure(bg=self.bg_color)
        self.root.attributes("-alpha", 0.95)  # Légère transparence
        
        # Barre de titre personnalisée
        self.title_bar = CustomTitleBar(
            self.root, 
            self.config, 
            self.translate('app_name'),
            on_close=self.on_close
        )
        self.title_bar.pack(fill="x")
        
        # Icône de l'application
        if self.icon_path and Path(self.icon_path).exists():
            try:
                self.icon_image = ImageTk.PhotoImage(Image.open(self.icon_path))
                self.root.iconphoto(True, self.icon_image)
            except Exception as e:
                print(f"Erreur lors du chargement de l'icône: {e}")
        
        # Styles de texte
        title_font = tkfont.Font(weight="bold", size=22)
        button_font = tkfont.Font(weight="bold", size=18)
        countdown_font = tkfont.Font(weight="bold", size=16)
        
        # Frame principale
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Message
        self.label = tk.Label(
            main_frame, 
            text=self.translate('are_you_sleeping'), 
            font=title_font, 
            bg=self.bg_color, 
            fg=self.fg_color
        )
        self.label.pack(pady=20)
        
        # Bouton de réponse
        self.button = tk.Button(
            main_frame, 
            text=self.translate('no'), 
            command=self.button_press, 
            width=20, 
            height=2, 
            font=button_font, 
            bg=self.accent_color, 
            fg=self.fg_color,
            activebackground=self.fg_color,
            activeforeground=self.bg_color,
            borderwidth=0,
            relief="flat"
        )
        self.button.pack(pady=20)
        
        # Étiquette de compte à rebours
        self.countdown_label = tk.Label(
            main_frame, 
            text=self.translate('time_remaining').format(self.countdown_time), 
            font=countdown_font, 
            bg=self.bg_color, 
            fg=self.fg_color
        )
        self.countdown_label.pack(pady=20)
        
        # Centrage de la fenêtre
        self.center_window(500, 350)
        
        # Début du compte à rebours
        self.count = self.countdown_time
        self.update_label()
        
        # Garder la fenêtre au premier plan
        self.root.attributes("-topmost", True)
        
        # Animation d'ouverture
        self.animate_open()
    
    def animate_open(self):
        """Animation d'ouverture de la fenêtre"""
        self.root.attributes('-alpha', 0.0)
        
        def fade_in(alpha=0.0):
            alpha += 0.1
            self.root.attributes('-alpha', alpha)
            if alpha < 0.95:
                self.root.after(20, lambda: fade_in(alpha))
        
        fade_in()
    
    def animate_close(self, callback):
        """Animation de fermeture de la fenêtre"""
        def fade_out(alpha=0.95):
            alpha -= 0.1
            self.root.attributes('-alpha', alpha)
            if alpha > 0:
                self.root.after(20, lambda: fade_out(alpha))
            else:
                callback()
        
        fade_out()
    
    def on_close(self):
        """Gère la fermeture de la fenêtre"""
        self.animate_close(self.root.destroy)
    
    def translate(self, key):
        """Récupère une traduction"""
        return TRANSLATIONS.get(self.lang, TRANSLATIONS['en']).get(key, key)
    
    def update_label(self):
        """Met à jour l'étiquette de compte à rebours"""
        if self.stop_event.is_set() or not self.root.winfo_exists():
            return
        
        if not self.paused and self.count >= 0:
            # Mise à jour du texte
            self.countdown_label.config(
                text=self.translate('time_remaining').format(self.count)
            )
            
            # Mise à jour du titre de l'icône
            if self.tray_icon:
                self.tray_icon.title = self.translate('time_remaining').format(self.count)
            
            # Décrément du compteur
            self.count -= 1
            
            # Planification de la prochaine mise à jour
            self.root.after(1000, self.update_label)
        elif self.count < 0:
            # Temps écoulé, exécution de l'action
            self.shutdown_popup()
    
    def button_press(self):
        """Gère l'appui sur le bouton"""
        self.animate_close(lambda: self.continue_after_button_press())
    
    def continue_after_button_press(self):
        """Suite de l'action après animation de fermeture"""
        self.root.destroy()
        
        if not self.stop_event.is_set():
            # Mise à jour du titre de l'icône
            if self.tray_icon:
                minutes, seconds = divmod(self.interval, 60)
                self.tray_icon.title = f"{self.translate('app_name')}: {minutes:02d}:{seconds:02d}"
            
            # Démarrage du minuteur d'intervalle
            self.start_interval_timer(self.interval)
    
    def start_interval_timer(self, interval):
        """Démarre le minuteur d'intervalle"""
        self.interval_count = interval
        self.next_popup_time = datetime.now() + timedelta(seconds=interval)
        self.update_tooltip()
    
    def update_tooltip(self):
        """Met à jour l'infobulle de l'icône de la barre des tâches"""
        if self.stop_event.is_set():
            return
            
        current_time = datetime.now()
        time_left = (self.next_popup_time - current_time).total_seconds()
        
        if time_left > 0:
            # Mise à jour du titre
            if self.tray_icon:
                minutes, seconds = divmod(int(time_left), 60)
                self.tray_icon.title = f"{self.translate('app_name')}: {minutes:02d}:{seconds:02d}"
            
            # Planification de la prochaine mise à jour
            threading.Timer(1, self.update_tooltip).start()
        else:
            # Temps écoulé, affichage de la fenêtre
            self.show_popup()
    
    def show_popup(self):
        """Affiche la fenêtre de compte à rebours"""
        if not self.stop_event.is_set():
            root = tk.Tk()
            app = CountdownApp(root, self.stop_event, self.config, self.tray_icon, self.icon_path)
            root.mainloop()
    
    def shutdown_popup(self):
        """Arrête l'ordinateur après confirmation"""
        self.root.destroy()
        
        if not self.stop_event.is_set():
            # Création d'une fenêtre de confirmation
            confirm_root = tk.Tk()
            confirm_root.overrideredirect(True)
            confirm_root.configure(bg=self.bg_color)
            confirm_root.attributes("-topmost", True)
            confirm_root.attributes("-alpha", 0.95)
            
            # Barre de titre
            title_bar = CustomTitleBar(
                confirm_root, 
                self.config, 
                self.translate('app_name')
            )
            title_bar.pack(fill="x")
            
            # Frame principale
            confirm_frame = tk.Frame(confirm_root, bg=self.bg_color)
            confirm_frame.pack(expand=True, fill="both", padx=20, pady=20)
            
            # Message
            confirm_label = tk.Label(
                confirm_frame,
                text="L'ordinateur va s'éteindre dans 10 secondes",
                font=tkfont.Font(weight="bold", size=16),
                bg=self.bg_color,
                fg=self.fg_color
            )
            confirm_label.pack(pady=20)
            
            # Boutons
            button_frame = tk.Frame(confirm_frame, bg=self.bg_color)
            button_frame.pack(pady=20)
            
            # Style de bouton
            button_style = {
                "font": tkfont.Font(weight="bold", size=14),
                "borderwidth": 0,
                "relief": "flat",
                "padx": 20,
                "pady": 10
            }
            
            # Bouton d'annulation
            cancel_button = tk.Button(
                button_frame,
                text="Annuler",
                command=lambda: (confirm_root.destroy(), self.show_popup()),
                bg=self.bg_color,
                fg=self.accent_color,
                activebackground=self.bg_color,
                activeforeground=self.fg_color,
                **button_style
            )
            cancel_button.pack(side="left", padx=10)
            
            # Bouton de confirmation
            confirm_button = tk.Button(
                button_frame,
                text="Éteindre",
                command=lambda: self.execute_shutdown(confirm_root),
                bg=self.accent_color,
                fg=self.fg_color,
                activebackground=self.fg_color,
                activeforeground=self.bg_color,
                **button_style
            )
            confirm_button.pack(side="right", padx=10)
            
            # Compte à rebours
            countdown = 10
            
            def update_countdown():
                nonlocal countdown
                countdown -= 1
                confirm_label.config(text=f"L'ordinateur va s'éteindre dans {countdown} secondes")
                
                if countdown > 0:
                    confirm_root.after(1000, update_countdown)
                else:
                    self.execute_shutdown(confirm_root)
            
            # Centrage de la fenêtre
            confirm_root.update_idletasks()
            width, height = 400, 200
            x = (confirm_root.winfo_screenwidth() // 2) - (width // 2)
            y = (confirm_root.winfo_screenheight() // 2) - (height // 2)
            confirm_root.geometry(f'{width}x{height}+{x}+{y}')
            
            # Début du compte à rebours
            update_countdown()
            
            # Boucle principale
            confirm_root.mainloop()
    
    def execute_shutdown(self, window=None):
        """Exécute la commande d'arrêt"""
        if window:
            window.destroy()
        
        # Détermine le système d'exploitation et utilise la commande appropriée
        if sys.platform.startswith('win'):
            os.system("shutdown /s /t 1")
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            os.system("sudo shutdown -h now")
    
    def center_window(self, width, height):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')


class SettingsWindow:
    """Fenêtre de paramètres"""
    
    def __init__(self, parent, config, on_close=None):
        self.parent = parent
        self.config = config
        self.on_close = on_close
        
        # Création de la fenêtre
        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)
        self.window.configure(bg=config.get('theme.bg_color'))
        self.window.attributes("-alpha", 0.95)
        
        # Barre de titre
        self.title_bar = CustomTitleBar(
            self.window, 
            config, 
            TRANSLATIONS[config.get('language')]['settings'],
            on_close=self.close_window
        )
        self.title_bar.pack(fill="x")
        
        # Frame principale
        self.main_frame = tk.Frame(self.window, bg=config.get('theme.bg_color'))
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Styles
        label_style = {
            "bg": config.get('theme.bg_color'),
            "fg": config.get('theme.fg_color'),
            "font": tkfont.Font(size=12)
        }
        
        entry_style = {
            "bg": config.get('theme.bg_color'),
            "fg": config.get('theme.accent_color'),
            "insertbackground": config.get('theme.fg_color'),
            "relief": "flat",
            "borderwidth": 1,
            "highlightbackground": config.get('theme.accent_color'),
            "highlightthickness": 1,
            "font": tkfont.Font(size=12)
        }
        
        # Paramètres
        settings = [
            ("Temps du compte à rebours (secondes)", "countdown_time", 60),
            ("Intervalle entre les rappels (secondes)", "interval", 2700)
        ]
        
        # Créer les contrôles pour chaque paramètre
        self.entries = {}
        row = 0
        
        for label_text, key, default in settings:
            # Étiquette
            label = tk.Label(self.main_frame, text=label_text, anchor="w", **label_style)
            label.grid(row=row, column=0, sticky="w", padx=10, pady=10)
            
            # Champ de saisie
            var = tk.StringVar(value=str(config.get(key, default)))
            entry = tk.Entry(self.main_frame, textvariable=var, width=10, **entry_style)
            entry.grid(row=row, column=1, padx=10, pady=10)
            
            self.entries[key] = var
            row += 1
        
        # Choix de la langue
        lang_label = tk.Label(self.main_frame, text="Langue", anchor="w", **label_style)
        lang_label.grid(row=row, column=0, sticky="w", padx=10, pady=10)
        
        self.lang_var = tk.StringVar(value=config.get('language', 'fr'))
        lang_frame = tk.Frame(self.main_frame, bg=config.get('theme.bg_color'))
        lang_frame.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        
        languages = [("Français", "fr"), ("English", "en")]
        
        for i, (text, value) in enumerate(languages):
            tk.Radiobutton(
                lang_frame,
                text=text,
                value=value,
                variable=self.lang_var,
                bg=config.get('theme.bg_color'),
                fg=config.get('theme.fg_color'),
                selectcolor=config.get('theme.accent_color'),
                activebackground=config.get('theme.bg_color'),
                activeforeground=config.get('theme.fg_color')
            ).pack(side="left", padx=5)
        
        row += 1
        
        # Démarrage automatique
        self.autostart_var = tk.BooleanVar(value=config.get('auto_start', False))
        autostart_check = tk.Checkbutton(
            self.main_frame,
            text="Démarrer automatiquement avec Windows",
            variable=self.autostart_var,
            bg=config.get('theme.bg_color'),
            fg=config.get('theme.fg_color'),
            selectcolor=config.get('theme.accent_color'),
            activebackground=config.get('theme.bg_color'),
            activeforeground=config.get('theme.fg_color')
        )
        autostart_check.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        
        row += 1
        
        # Bouton de sauvegarde
        save_button = tk.Button(
            self.main_frame,
            text="Sauvegarder",
            command=self.save_settings,
            bg=config.get('theme.accent_color'),
            fg=config.get('theme.fg_color'),
            activebackground=config.get('theme.fg_color'),
            activeforeground=config.get('theme.bg_color'),
            borderwidth=0,
            relief="flat",
            font=tkfont.Font(weight="bold", size=12),
            padx=20,
            pady=5
        )
        save_button.grid(row=row, column=0, columnspan=2, pady=20)
        
        # Centrage de la fenêtre
        self.window.update_idletasks()
        width, height = 450, 300
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Garder la fenêtre au premier plan
        self.window.attributes("-topmost", True)
    
    def save_settings(self):
        """Sauvegarde les paramètres"""
        try:
            # Mise à jour des paramètres numériques
            for key, var in self.entries.items():
                value = int(var.get())
                self.config.set(key, value)
            
            # Mise à jour de la langue
            self.config.set('language', self.lang_var.get())
            
            # Mise à jour du démarrage automatique
            self.config.set('auto_start', self.autostart_var.get())
            
            # Configuration du démarrage automatique
            self.configure_autostart(self.autostart_var.get())
            
            # Sauvegarde de la configuration
            self.config.save_config()
            
            # Fermeture de la fenêtre
            self.close_window()
        except ValueError:
            # Affichage d'un message d'erreur
            tk.messagebox.showerror(
                "Erreur",
                "Veuillez entrer des valeurs numériques valides pour les temps."
            )
    
    def configure_autostart(self, enable):
        """Configure le démarrage automatique"""
        if sys.platform.startswith('win'):
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    key_path,
                    0,
                    winreg.KEY_SET_VALUE
                )
                
                if enable:
                    # Ajout au registre
                    executable = sys.executable
                    script_path = os.path.abspath(sys.argv[0])
                    command = f'"{executable}" "{script_path}"'
                    winreg.SetValueEx(key, "ModeNuit", 0, winreg.REG_SZ, command)
                else:
                    # Suppression du registre
                    try:
                        winreg.DeleteValue(key, "ModeNuit")
                    except FileNotFoundError:
                        pass
                
                winreg.CloseKey(key)
            except Exception as e:
                print(f"Erreur lors de la configuration du démarrage automatique: {e}")
    
    def close_window(self):
        """Ferme la fenêtre des paramètres"""
        self.window.destroy()
        if self.on_close:
            self.on_close()


def create_image(width, height, color1, color2):
    """Crée une image pour l'icône"""
    # Création d'une image transparente
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    
    # Fond
    dc.ellipse((0, 0, width, height), fill=color2)
    
    # Lune
    moon_offset = width // 4
    dc.ellipse((moon_offset, 0, width + moon_offset, height), fill=(0, 0, 0, 0))
    
    # Ajout d'étoiles (petits points)
    for _ in range(5):
        star_x = int(width * 0.7 * random.random())
        star_y = int(height * 0.7 * random.random())
        star_size = int(width * 0.05)
        dc.ellipse(
            (star_x, star_y, star_x + star_size, star_y + star_size),
            fill=(255, 255, 255, 200)
        )
    
    return image


def save_image(image, path):
    """Sauvegarde l'image sur le disque"""
    try:
        # Création du dossier parent si nécessaire
        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        # Sauvegarde de l'image
        image.save(path)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'image: {e}")
        return None
    return path


def check_stop_event(stop_event):
    """Vérifie si l'événement d'arrêt a été déclenché"""
    while not stop_event.is_set():
        threading.Event().wait(1)
    os._exit(0)


def create_tray_menu(tray_icon, stop_event, config, icon_path):
    """Crée le menu de la barre des tâches"""
    lang = config.get('language', 'fr')
    translations = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    
    return menu(
        item(
            translations['settings'],
            lambda: show_settings(tray_icon, config)
        ),
        item(
            translations['start'],
            lambda: show_popup(tray_icon, stop_event, config, icon_path)
        ),
        item(
            translations['quit'],
            lambda: on_exit(tray_icon, stop_event)
        )
    )


def show_settings(tray_icon, config):
    """Affiche la fenêtre des paramètres"""
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale
    
    settings = SettingsWindow(
        root,
        config,
        on_close=lambda: root.destroy()
    )
    
    root.mainloop()


def show_popup(tray_icon, stop_event, config, icon_path):
    """Affiche la fenêtre principale"""
    if stop_event.is_set():
        return
    
    root = tk.Tk()
    app = CountdownApp(root, stop_event, config, tray_icon, icon_path)
    root.mainloop()


def on_exit(tray_icon, stop_event):
    """Gère la sortie de l'application"""
    stop_event.set()
    tray_icon.stop()


def setup_tray(icon, stop_event, config, icon_path):
    """Configure l'icône de la barre des tâches"""
    icon.visible = True
    
    # Met à jour le menu
    icon.menu = create_tray_menu(icon, stop_event, config, icon_path)
    
    # Message de démarrage
    icon.notify(
        TRANSLATIONS[config.get('language')]['app_name'] + " démarré",
        "Cliquez sur l'icône pour accéder aux options."
    )
    
    # Démarrage automatique si configuré
    if config.get('auto_start', False):
        threading.Timer(2, lambda: show_popup(icon, stop_event, config, icon_path)).start()
    
    # Démarrage du thread de surveillance
    threading.Thread(
        target=check_stop_event,
        args=(stop_event,),
        daemon=True
    ).start()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NightMod - Surveillant de sommeil et économiseur d'énergie

Ce programme vérifie périodiquement si l'utilisateur est encore éveillé en affichant
une fenêtre popup. Si l'utilisateur ne répond pas, l'ordinateur est éteint.
"""

import sys
import os
import logging
from src.app import NightModApp

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

def main():
    """Point d'entrée principal de l'application"""
    try:
        # S'assurer que le répertoire de configuration existe
        config_dir = os.path.join(os.path.expanduser("~"), ".nightmod")
        os.makedirs(config_dir, exist_ok=True)

        # Démarrer l'application
        app = NightModApp()
        app.mainloop()
    except Exception as e:
        import traceback
        logger.critical(f"Erreur critique lors de l'exécution de l'application: {e}")
        logger.critical(traceback.format_exc())
        
        # Afficher une boîte de dialogue d'erreur si possible
        try:
            import tkinter.messagebox as messagebox
            messagebox.showerror(
                "NightMod - Erreur critique",
                f"Une erreur critique s'est produite:\n\n{str(e)}\n\nConsultez le fichier de log pour plus d'informations."
            )
        except:
            print(f"ERREUR CRITIQUE: {e}")


if __name__ == "__main__":
    main()
