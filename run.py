#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de lancement pour NightMod
Ce script vérifie l'environnement et lance l'application
"""

import sys
import os
import platform
import subprocess
import importlib.util
import logging
import traceback

# Configuration basique du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("NightMod.Launcher")

def check_python_version():
    """Vérifie si la version de Python est compatible"""
    required_version = (3, 6)
    current_version = sys.version_info
    
    if current_version < required_version:
        logger.error(f"Python {required_version[0]}.{required_version[1]} ou supérieur est requis. "
                     f"Version actuelle: {current_version[0]}.{current_version[1]}")
        print(f"Erreur: Python {required_version[0]}.{required_version[1]} ou supérieur est requis.")
        print(f"Votre version: {current_version[0]}.{current_version[1]}")
        return False
    
    return True

def check_dependencies():
    """Vérifie si les dépendances requises sont installées"""
    required_modules = ["tkinter"]
    optional_modules = ["pystray", "PIL", "psutil"]
    
    missing_required = []
    missing_optional = []
    
    # Vérifier les modules requis
    for module in required_modules:
        if not importlib.util.find_spec(module):
            missing_required.append(module)
    
    # Vérifier les modules optionnels
    for module in optional_modules:
        if not importlib.util.find_spec(module):
            missing_optional.append(module)
    
    if missing_required:
        logger.error(f"Modules requis manquants: {', '.join(missing_required)}")
        print(f"Erreur: Les modules suivants sont requis mais non installés: {', '.join(missing_required)}")
        
        # Instructions spécifiques pour tkinter qui n'est pas installable via pip
        if "tkinter" in missing_required:
            if platform.system() == "Windows":
                print("Pour installer tkinter sur Windows, réinstallez Python en cochant l'option 'tcl/tk and IDLE'.")
            elif platform.system() == "Darwin":  # macOS
                print("Pour installer tkinter sur macOS, utilisez: brew install python-tk")
            else:  # Linux
                print("Pour installer tkinter sur Linux, utilisez:")
                print("  - Debian/Ubuntu: sudo apt-get install python3-tk")
                print("  - Fedora: sudo dnf install python3-tkinter")
                print("  - Arch Linux: sudo pacman -S tk")
        
        return False
    
    if missing_optional:
        logger.warning(f"Modules optionnels manquants: {', '.join(missing_optional)}")
        print(f"Avertissement: Certains modules optionnels ne sont pas installés: {', '.join(missing_optional)}")
        print("Certaines fonctionnalités peuvent être limitées.")
        
        # Proposer d'installer les dépendances optionnelles
        print("\nVoulez-vous installer les modules optionnels? (o/n)")
        choice = input("> ").lower()
        
        if choice == 'o':
            try:
                for module in missing_optional:
                    if module == "PIL":  # PIL est en réalité installé via pillow
                        module = "pillow"
                    subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                print("Modules optionnels installés avec succès!")
            except Exception as e:
                logger.error(f"Erreur lors de l'installation des modules optionnels: {e}")
                print(f"Erreur lors de l'installation: {e}")
    
    return True

def main():
    """Fonction principale"""
    print("Initialisation de NightMod...")
    
    # Vérifier la version de Python
    if not check_python_version():
        input("Appuyez sur Entrée pour quitter...")
        return 1
    
    # Vérifier les dépendances
    if not check_dependencies():
        input("Appuyez sur Entrée pour quitter...")
        return 1
    
    # Ajouter le répertoire courant au chemin de recherche des modules
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Importer et lancer l'application principale
        from nightmod import main
        main()
        return 0
    except ImportError as e:
        logger.error(f"Erreur lors de l'importation de l'application principale: {e}")
        print("Erreur: Impossible de trouver ou d'importer l'application principale.")
        print(f"Détails: {e}")
    except Exception as e:
        logger.error(f"Erreur lors du lancement de l'application: {e}")
        logger.error(traceback.format_exc())
        print(f"Erreur: {e}")
        print("Consultez les logs pour plus de détails.")
    
    input("Appuyez sur Entrée pour quitter...")
    return 1

if __name__ == "__main__":
    sys.exit(main())