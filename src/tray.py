#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de gestion de l'icône dans la barre des tâches pour NightMod
"""

import os
import threading
import logging
import platform
import weakref

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
        # Utiliser weakref pour éviter des références circulaires
        self.app = weakref.ref(app) if app else None
        self.toggle_window_callback = toggle_window_callback
        self.toggle_monitoring_callback = toggle_monitoring_callback
        self.quit_callback = quit_callback
        
        self.tray_icon = None
        self.tray_thread = None
        
        # Attributs pour les icônes
        self.active_icon = None  
        self.inactive_icon = None
        
        # État de l'icône
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
                # Créer une icône de secours plus élégante
                icon_image = self.create_default_icon(is_active=False)
            
            # Enregistrer les images d'état
            self.active_icon = icon_image
            
            # Créer une version désactivée de l'icône
            self.inactive_icon = self.create_grayscale_version(icon_image)
            
            # Définir le menu avec libellés plus clairs
            menu = pystray.Menu(
                pystray.MenuItem("Ouvrir NightMod", self._safe_callback(self.toggle_window_callback)),
                pystray.MenuItem("Surveillance active", self._safe_callback(self.toggle_monitoring_callback), 
                                checked=self._is_monitoring_active),
                pystray.MenuItem("Quitter", self._safe_callback(self.quit_callback))
            )
            
            # Créer l'icône
            self.tray_icon = pystray.Icon("nightmod", icon_image, "NightMod (inactif)", menu)
            
            # Démarrer l'icône dans un thread
            self.is_running = True
            self.tray_thread = threading.Thread(target=self.run, daemon=True)
            self.tray_thread.start()
            
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
    
    def _safe_callback(self, callback):
        """Wrapper pour rendre les callbacks plus sûrs"""
        def wrapper(*args, **kwargs):
            try:
                if callback:
                    return callback(*args, **kwargs)
            except Exception as e:
                logger.error(f"Erreur dans un callback de l'icône de la barre des tâches: {e}")
        return wrapper
    
    def _is_monitoring_active(self, item):
        """Vérifie si la surveillance est active pour le menu coché"""
        try:
            app = self.app()
            if app and hasattr(app, 'is_monitoring'):
                return app.is_monitoring
        except Exception:
            pass
        return False
    
    def create_default_icon(self, is_active=False):
        """Crée une icône par défaut moderne en cas d'absence du fichier d'icône"""
        from PIL import Image, ImageDraw
        
        # Tailles et couleurs
        size = 64
        padding = 6
        
        # Couleurs de base
        if is_active:
            bg_color = (32, 32, 32)
            circle_color = (76, 175, 80)  # Vert
        else:
            bg_color = (32, 32, 32)
            circle_color = (128, 128, 128)  # Gris
        
        # Créer l'image de base (fond transparent)
        icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(icon)
        
        # Dessiner un cercle avec un croissant de lune
        # Cercle principal
        draw.ellipse(
            (padding, padding, size - padding, size - padding),
            fill=circle_color
        )
        
        # Créer un effet de "lune" en décalant un cercle légèrement
        draw.ellipse(
            (padding + size//5, padding, size - padding + size//5, size - padding),
            fill=bg_color
        )
        
        return icon
    
    def create_grayscale_version(self, original_icon):
        """Crée une version grisée de l'icône pour l'état inactif"""
        from PIL import Image, ImageOps, ImageEnhance
        
        # Créer une copie pour ne pas modifier l'original
        if original_icon.mode != 'RGBA':
            # Convertir en RGBA si ce n'est pas déjà le cas
            grayscale = original_icon.convert('RGBA')
        else:
            grayscale = original_icon.copy()
        
        # Extraire les couches alpha
        alpha = grayscale.split()[3]
        
        # Convertir en niveaux de gris
        grayscale = ImageOps.grayscale(grayscale.convert('RGB'))
        
        # Réduire la luminosité et le contraste
        enhancer = ImageEnhance.Brightness(grayscale)
        grayscale = enhancer.enhance(0.7)
        
        enhancer = ImageEnhance.Contrast(grayscale)
        grayscale = enhancer.enhance(0.8)
        
        # Reconvertir en RGBA et réappliquer l'alpha
        grayscale = grayscale.convert('RGBA')
        grayscale.putalpha(alpha)
        
        return grayscale
    
    def update_icon(self, is_monitoring):
        """Met à jour l'icône pour refléter l'état de la surveillance"""
        if self.tray_icon:
            try:
                # Mettre à jour l'icône en fonction de l'état
                if is_monitoring:
                    self.tray_icon.icon = self.active_icon
                    self.tray_icon.title = "NightMod (actif)"
                else:
                    self.tray_icon.icon = self.inactive_icon  # Utiliser l'icône grisée
                    self.tray_icon.title = "NightMod (inactif)"
            except Exception as e:
                logger.error(f"Erreur lors de la mise à jour de l'icône: {e}")
                # Si la mise à jour de l'icône échoue, essayer une approche plus simple
                try:
                    # Mise à jour du texte de survol uniquement
                    status = "actif" if is_monitoring else "inactif"
                    self.tray_icon.title = f"NightMod ({status})"
                except:
                    pass  # Ignorer les erreurs car cette fonctionnalité est optionnelle
    
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
            try:
                self.tray_icon.run()
            except Exception as e:
                logger.error(f"Erreur lors de l'exécution de l'icône de la barre des tâches: {e}")
                self.tray_icon = None
    
    def stop(self):
        """Arrête l'icône de la barre des tâches et libère les ressources"""
        if self.tray_icon:
            try:
                self.is_running = False
                
                # Essayer d'arrêter proprement l'icône
                try:
                    self.tray_icon.stop()
                except:
                    pass
                
                # Libérer les références pour aider le ramasse-miettes
                self.tray_icon = None
                self.active_icon = None
                self.inactive_icon = None
                
                # Attendre que le thread se termine (avec timeout)
                if self.tray_thread and self.tray_thread.is_alive():
                    self.tray_thread.join(timeout=2.0)
                    
                logger.info("Icône de la barre des tâches arrêtée avec succès")
            except Exception as e:
                logger.error(f"Erreur lors de l'arrêt de l'icône de la barre des tâches: {e}")
                
            # S'assurer que les références sont libérées même en cas d'erreur
            self.tray_icon = None
            self.active_icon = None
            self.inactive_icon = None
            self.tray_thread = None
    
    def is_available(self):
        """Vérifie si l'icône de la barre des tâches est disponible"""
        return self.tray_icon is not None and self.is_running