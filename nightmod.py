#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NightMod - Surveillant de sommeil et économiseur d'énergie

Ce programme vérifie périodiquement si l'utilisateur est encore éveillé en affichant
une fenêtre popup. Si l'utilisateur ne répond pas, l'ordinateur est éteint,
mis en veille ou verrouillé selon la configuration.

Point d'entrée principal de l'application (redirige vers src/app.py)
"""

import sys
import os
import logging
from pathlib import Path

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
        
        # Ajouter le répertoire courant au chemin de recherche des modules
        current_dir = Path(__file__).parent.absolute()
        sys.path.insert(0, str(current_dir))
        
        # Lancer l'application en utilisant le module de la classe principale
        from src.app import NightModApp
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
