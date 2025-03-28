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


<<<<<<< HEAD
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
=======
if __name__ == "__main__":
    main()
>>>>>>> 2d8bd4e (	new file:   GUIDE_UTILISATEUR.md)
