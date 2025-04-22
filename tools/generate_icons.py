#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de génération d'icônes pour NightMod
Convertit l'icône ICO en différentes tailles de PNG pour différentes plateformes
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Erreur: La bibliothèque PIL (Pillow) est requise.")
    print("Installez-la avec: pip install pillow")
    sys.exit(1)

# Tailles d'icônes à générer
ICON_SIZES = [16, 32, 48, 64, 128, 256]

# Chemins des fichiers
SCRIPT_DIR = Path(__file__).parent.absolute()
ROOT_DIR = SCRIPT_DIR.parent
ASSETS_DIR = ROOT_DIR / "assets"
ICO_PATH = ASSETS_DIR / "icon.ico"
IMG_DIR = ASSETS_DIR / "img"

def create_directory_if_not_exists(directory):
    """Crée un répertoire s'il n'existe pas déjà"""
    if not directory.exists():
        try:
            directory.mkdir(parents=True)
            print(f"✓ Répertoire créé: {directory}")
        except Exception as e:
            print(f"✗ Erreur lors de la création du répertoire {directory}: {e}")
            return False
    return True

def generate_png_icons():
    """Génère des icônes PNG à partir de l'icône ICO"""
    print("\n=== Génération des icônes PNG ===\n")
    
    # Vérifier si l'icône ICO existe
    if not ICO_PATH.exists():
        print(f"✗ Fichier d'icône ICO introuvable: {ICO_PATH}")
        return False
    
    # Créer le répertoire img s'il n'existe pas
    if not create_directory_if_not_exists(IMG_DIR):
        return False
    
    try:
        # Ouvrir l'icône ICO
        ico = Image.open(ICO_PATH)
        
        # Générer une icône PNG pour chaque taille
        for size in ICON_SIZES:
            # Nom du fichier de sortie
            output_path = IMG_DIR / f"icon_{size}x{size}.png"
            
            # Redimensionner l'icône
            resized_icon = ico.resize((size, size), Image.LANCZOS)
            
            # Enregistrer l'icône PNG
            resized_icon.save(output_path, "PNG")
            print(f"✓ Icône générée: {output_path}")
        
        # Créer également des versions active/inactive pour la barre des tâches
        for status in ["active", "inactive"]:
            # Ouvrir l'icône ICO
            ico = Image.open(ICO_PATH)
            
            # Taille pour les icônes de la barre des tâches
            size = 16
            
            # Modifier l'icône selon le statut
            resized_icon = ico.resize((size, size), Image.LANCZOS)
            
            if status == "inactive":
                # Convertir en niveaux de gris pour l'état inactif
                resized_icon = resized_icon.convert("LA").convert("RGBA")
            
            # Enregistrer l'icône
            output_path = IMG_DIR / f"icon_{status}.png"
            resized_icon.save(output_path, "PNG")
            print(f"✓ Icône d'état générée: {output_path}")
        
        # Créer une copie principale à la racine des images
        ico.resize((256, 256), Image.LANCZOS).save(IMG_DIR / "icon.png", "PNG")
        print(f"✓ Icône principale générée: {IMG_DIR / 'icon.png'}")
        
        return True
    
    except Exception as e:
        print(f"✗ Erreur lors de la génération des icônes: {e}")
        return False

if __name__ == "__main__":
    if generate_png_icons():
        print("\n✓ Génération des icônes terminée avec succès!")
    else:
        print("\n✗ La génération des icônes a échoué.")
        sys.exit(1)
