#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de gestion de l'icône dans la barre des tâches pour NightMod
"""

import os
import threading
import logging
import platform

# Obtenir le logger
logger = logging.getLogger("NightMod.Tray")

class TrayIcon:
    """Gère l'icône dans la barre des tâches (si disponible)"""
    
    def __init__(self, app, toggle_window_callback, toggle_monitoring_callback, quit_callback):
        """
        Initialise l'icône de la barre des tâches
        
        Args:
            app: L'instance de l'application principale
            toggle_window_callback: Fonction pour afficher/masquer la fenêtre principale
            toggle_monitoring_callback: Fonction pour démarrer/arrêter la surveillance
            quit_callback: Fonction pour quitter l'application
        """
        self.app = app
        self.toggle_window_callback = toggle_window_callback
        self.toggle_monitoring_callback = toggle_monitoring_callback
        self.quit_callback = quit_callback
        self.tray_icon = None
        self.is_running = False
    
    def setup(self):
        """Configure l'icône dans la barre des tâches si les dépendances sont disponibles"""
        try:
            # Cette fonctionnalité nécessite pystray, qui est optionnel
            import pystray
            from PIL import Image, ImageDraw
            
            # Créer une icône simple si aucune n'est disponible
            icon_image = None
            try:
                icon_path = self.find_icon_file()
                if icon_path:
                    icon_image = Image.open(icon_path)
                else:
                    raise FileNotFoundError("Aucune icône trouvée")
            except Exception as e:
                logger.warning(f"Impossible de charger l'icône: {e}")
                # Créer une icône de secours
                icon_image = Image.new('RGB', (64, 64), color=(47, 47, 47))
                d = ImageDraw.Draw(icon_image)
                d.rectangle((10, 10, 54, 54), fill=(0, 120, 215))
            
            # Définir le menu
            menu = pystray.Menu(
                pystray.MenuItem("Afficher/Masquer", self.toggle_window_callback),
                pystray.MenuItem("Démarrer/Arrêter", self.toggle_monitoring_callback),
                pystray.MenuItem("Quitter", self.quit_callback)
            )
            
            # Créer l'icône
            self.tray_icon = pystray.Icon("nightmod", icon_image, "NightMod", menu)
            
            # Démarrer l'icône dans un thread
            self.is_running = True
            threading.Thread(target=self.run, daemon=True).start()
            
            logger.info("Icône de la barre des tâches configurée avec succès")
            return True
        
        except ImportError as e:
            logger.warning(f"pystray ou PIL non installé, fonctionnalité de barre des tâches désactivée: {e}")
            self.tray_icon = None
            return False
        
        except Exception as e:
            logger.error(f"Erreur lors de la configuration de l'icône de la barre des tâches: {e}")
            self.tray_icon = None
            return False
    
    def find_icon_file(self):
        """Trouve le fichier d'icône approprié selon la plateforme"""
        # Chemins possibles pour l'icône
        possible_paths = [
            "assets/icon.png",
            "assets/icon.ico",
            "../assets/icon.png",
            "../assets/icon.ico",
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/icon.png"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/icon.ico")
        ]
        
        # Ajoutez des chemins spécifiques au système
        if platform.system() == "Windows":
            possible_paths.append(os.path.join(os.environ.get("LOCALAPPDATA", ""), "NightMod/assets/icon.ico"))
        elif platform.system() == "Darwin":  # macOS
            possible_paths.append("/Applications/NightMod.app/Contents/Resources/icon.png")
        elif platform.system() == "Linux":
            possible_paths.append("/opt/nightmod/assets/icon.png")
            possible_paths.append(os.path.expanduser("~/.local/share/nightmod/assets/icon.png"))
        
        # Chercher l'icône dans les chemins possibles
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def run(self):
        """Exécute l'icône de la barre des tâches dans un thread séparé"""
        if self.tray_icon:
            self.tray_icon.run()
    
    def stop(self):
        """Arrête l'icône de la barre des tâches"""
        if self.tray_icon:
            try:
                self.is_running = False
                self.tray_icon.stop()
            except Exception as e:
                logger.error(f"Erreur lors de l'arrêt de l'icône de la barre des tâches: {e}")
    
    def update_icon(self, is_monitoring):
        """Met à jour l'icône pour refléter l'état de la surveillance"""
        # Cette fonctionnalité dépend de la bibliothèque pystray
        # et pourrait ne pas être supportée par toutes les versions
        if self.tray_icon:
            try:
                # Mise à jour du texte de survol
                status = "actif" if is_monitoring else "inactif"
                self.tray_icon.title = f"NightMod ({status})"
            except:
                pass  # Ignorer les erreurs car cette fonctionnalité est optionnelle
    
    def is_available(self):
        """Vérifie si l'icône de la barre des tâches est disponible"""
        return self.tray_icon is not None and self.is_running