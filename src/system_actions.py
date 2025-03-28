#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module d'actions système pour NightMod
Gère les opérations de système comme l'extinction, la mise en veille, etc.
"""

import os
import platform
import logging
import subprocess

# Obtenir le logger
logger = logging.getLogger("NightMod.SystemActions")

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
                # Essayer plusieurs méthodes car cela peut varier selon les distributions
                try:
                    subprocess.run(["systemctl", "suspend"], check=True)
                except:
                    try:
                        subprocess.run(["pm-suspend"], check=True)
                    except:
                        os.system("echo mem > /sys/power/state")
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
                # Essayer plusieurs méthodes car cela peut varier selon les distributions et environnements de bureau
                methods = [
                    ["loginctl", "lock-session"],
                    ["gnome-screensaver-command", "--lock"],
                    ["xdg-screensaver", "lock"],
                    ["dm-tool", "lock"],
                    ["qdbus", "org.freedesktop.ScreenSaver", "/ScreenSaver", "Lock"]
                ]
                
                for method in methods:
                    try:
                        subprocess.run(method, check=True)
                        return True
                    except:
                        continue
                
                logger.warning("Aucune méthode de verrouillage d'écran n'a fonctionné. Essai de mise en veille de l'écran.")
                os.system("xset dpms force off")
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
    
    @staticmethod
    def configure_autostart(enable, app_path=None):
        """Configure le démarrage automatique au démarrage du système"""
        if app_path is None:
            import sys
            app_path = sys.executable
            
            # Si c'est un script Python, utiliser l'interpréteur
            if not app_path.endswith(('.exe', '.app')):
                app_path = f"{sys.executable} {os.path.abspath(sys.argv[0])}"
        
        logger.info(f"Configuration du démarrage automatique: {'activer' if enable else 'désactiver'}")
        
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
                
                if enable:
                    # Ajouter au démarrage automatique
                    winreg.SetValueEx(
                        key, 
                        "NightMod", 
                        0, 
                        winreg.REG_SZ, 
                        app_path
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
                
                if enable:
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
        <string>{app_path}</string>
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
                
                if enable:
                    # Créer le répertoire s'il n'existe pas
                    os.makedirs(autostart_dir, exist_ok=True)
                    
                    # Créer le fichier .desktop
                    desktop_content = f"""[Desktop Entry]
Type=Application
Name=NightMod
Comment=Surveillant de sommeil et économiseur d'énergie
Exec={app_path}
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
            
            return True
        
        except Exception as e:
            logger.error(f"Erreur lors de la configuration du démarrage automatique: {e}")
            return False