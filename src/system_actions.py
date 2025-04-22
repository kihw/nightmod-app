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
import shlex
import sys

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
                # Utiliser subprocess au lieu de os.system pour plus de sécurité
                subprocess.run(["shutdown", "/s", "/t", "10", "/c", "NightMod: Extinction automatique"], check=True)
            elif platform.system() == "Darwin":  # macOS
                script = "tell app \"System Events\" to shut down"
                subprocess.run(["osascript", "-e", script], check=True)
            else:  # Linux et autres Unix
                # Utiliser des arguments séparés au lieu d'une chaîne de commande
                subprocess.run(["shutdown", "-h", "now"], check=True)
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
                subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["pmset", "sleepnow"], check=True)
            else:  # Linux
                # Essayer plusieurs méthodes car cela peut varier selon les distributions
                methods = [
                    ["systemctl", "suspend"],
                    ["pm-suspend"],
                    ["echo", "mem", ">", "/sys/power/state"]
                ]
                
                for method in methods:
                    try:
                        if method[0] == "echo":
                            # Cas spécial pour la redirection
                            with open("/sys/power/state", "w") as f:
                                f.write("mem")
                            break
                        else:
                            subprocess.run(method, check=True)
                            break
                    except (subprocess.SubprocessError, FileNotFoundError, PermissionError):
                        continue
                    except Exception as method_error:
                        logger.warning(f"Méthode {method[0]} a échoué: {method_error}")
                        continue
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
                subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["pmset", "displaysleepnow"], check=True)
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
                    except (subprocess.SubprocessError, FileNotFoundError):
                        continue
                    except Exception as method_error:
                        logger.warning(f"Méthode {method[0]} a échoué: {method_error}")
                        continue
                
                logger.warning("Aucune méthode de verrouillage d'écran n'a fonctionné. Essai de mise en veille de l'écran.")
                subprocess.run(["xset", "dpms", "force", "off"], check=True)
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
        
        # Vérification de sécurité pour éviter l'injection de commandes
        if action not in actions:
            logger.error(f"Action non reconnue: {action}")
            return False
            
        return actions[action]()
    
    @staticmethod
    def configure_autostart(enable, app_path=None):
        """Configure le démarrage automatique au démarrage du système"""
        if app_path is None:
            # Utiliser le chemin de l'exécutable actuel
            app_path = sys.executable
            
            # Si c'est un script Python, utiliser l'interpréteur
            if not app_path.endswith(('.exe', '.app')):
                # Utiliser le chemin absolu du script principal
                script_path = os.path.abspath(sys.argv[0])
                app_path = f'"{sys.executable}" "{script_path}"'
        
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