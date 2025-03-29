#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de compilation pour NightMod
Ce script crée des executables pour Windows, macOS et Linux
"""

import os
import sys
import platform
import subprocess
import shutil
from datetime import datetime

# Version de l'application
VERSION = "1.0.0"

def print_header(message):
    """Affiche un message de titre formaté"""
    print("\n" + "=" * 60)
    print(f" {message}")
    print("=" * 60)

def check_requirements():
    """Vérifie si les outils nécessaires sont installés"""
    print_header("Vérification des prérequis")
    
    try:
        # Vérifier PyInstaller
        subprocess.run(
            [sys.executable, "-m", "pip", "show", "pyinstaller"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✓ PyInstaller est installé")
    except subprocess.CalledProcessError:
        print("✗ PyInstaller n'est pas installé")
        install = input("Voulez-vous l'installer maintenant? (o/n): ")
        if install.lower() == "o":
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "pyinstaller"],
                check=True
            )
        else:
            print("Impossible de continuer sans PyInstaller")
            sys.exit(1)
    
    # Vérifier les dépendances du projet
    try:
        if os.path.exists("requirements.txt"):
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                check=True
            )
            print("✓ Dépendances du projet installées")
    except subprocess.CalledProcessError:
        print("✗ Erreur lors de l'installation des dépendances")
        sys.exit(1)

def clean_build_dir():
    """Nettoie les répertoires de compilation"""
    print_header("Nettoyage des répertoires de compilation")
    
    dirs_to_clean = ["build", "dist"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Répertoire '{dir_name}' supprimé")
    
    # Supprimer les fichiers .spec de PyInstaller
    for file in os.listdir("."):
        if file.endswith(".spec"):
            os.remove(file)
            print(f"✓ Fichier '{file}' supprimé")

def build_for_windows():
    """Compile l'application pour Windows"""
    print_header("Compilation pour Windows")
    
    # Vérifier si l'icône existe
    icon_path = os.path.join("assets", "icon.ico")
    if not os.path.exists(icon_path):
        print("! Icône non trouvée, utilisation de l'icône par défaut")
        icon_path = None
    
    # Préparer la commande PyInstaller
    cmd = [
        sys.executable,  # Utilise le même Python que celui qui exécute le script
        "-m",
        "PyInstaller",  # Appelle le module PyInstaller directement
        "--name=NightMod",
        "--onefile",
        "--windowed",
    ]
    if icon_path:
        cmd.append(f"--icon={icon_path}")
    
    cmd.append("nightmod.py")
    
    # Exécuter PyInstaller
    try:
        subprocess.run(cmd, check=True)
        print("✓ Compilation réussie")
    except subprocess.CalledProcessError as e:
        print(f"✗ Erreur lors de la compilation: {e}")
        return False
    
    # Créer le dossier 'release' s'il n'existe pas
    os.makedirs("release", exist_ok=True)
    
    # Copier l'exécutable compilé dans le dossier release
    if os.path.exists("dist/NightMod.exe"):
        shutil.copy("dist/NightMod.exe", f"release/NightMod-{VERSION}.exe")
        print(f"✓ Executable Windows créé: release/NightMod-{VERSION}.exe")
        return True
    else:
        print("✗ L'exécutable n'a pas été créé correctement")
        return False

def build_for_macos():
    """Compile l'application pour macOS"""
    print_header("Compilation pour macOS")
    
    # Vérifier si l'icône existe
    icon_path = os.path.join("assets", "icon.icns")
    if not os.path.exists(icon_path):
        print("! Icône .icns non trouvée, utilisation de l'icône par défaut")
        icon_path = None
    
    # Préparer la commande PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "pyinstaller",
        "--name=NightMod",
        "--onefile",
        "--windowed",
    ]
    
    if icon_path:
        cmd.append(f"--icon={icon_path}")
    
    cmd.append("nightmod.py")
    
    # Exécuter PyInstaller
    try:
        subprocess.run(cmd, check=True)
        print("✓ Compilation réussie")
    except subprocess.CalledProcessError as e:
        print(f"✗ Erreur lors de la compilation: {e}")
        return False
    
    # Créer le dossier 'release' s'il n'existe pas
    os.makedirs("release", exist_ok=True)
    
    # Copier l'application dans le dossier release
    if os.path.exists("dist/NightMod.app"):
        release_path = f"release/NightMod-{VERSION}.app"
        if os.path.exists(release_path):
            shutil.rmtree(release_path)
        shutil.copytree("dist/NightMod.app", release_path)
        print(f"✓ Application macOS créée: {release_path}")
        return True
    else:
        print("✗ L'application n'a pas été créée correctement")
        return False

def build_for_linux():
    """Compile l'application pour Linux"""
    print_header("Compilation pour Linux")
    
    # Vérifier si l'icône existe
    icon_path = os.path.join("assets", "icon.png")
    if not os.path.exists(icon_path):
        print("! Icône non trouvée, utilisation de l'icône par défaut")
        icon_path = None
    
    # Préparer la commande PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "pyinstaller",
        "--name=nightmod",
        "--onefile",
        "--windowed",
    ]
    
    if icon_path:
        cmd.append(f"--icon={icon_path}")
    
    cmd.append("nightmod.py")
    
    # Exécuter PyInstaller
    try:
        subprocess.run(cmd, check=True)
        print("✓ Compilation réussie")
    except subprocess.CalledProcessError as e:
        print(f"✗ Erreur lors de la compilation: {e}")
        return False
    
    # Créer le dossier 'release' s'il n'existe pas
    os.makedirs("release", exist_ok=True)
    
    # Créer un script d'installation
    install_script = """#!/bin/bash
# Script d'installation pour NightMod (Linux)

# Vérifier les permissions root
if [ "$EUID" -ne 0 ]; then
  echo "Ce script doit être exécuté en tant que root (sudo)."
  exit 1
fi

# Créer le répertoire d'installation
INSTALL_DIR="/opt/nightmod"
mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/assets"

# Copier les fichiers
cp nightmod "$INSTALL_DIR/"
cp -r assets/* "$INSTALL_DIR/assets/" 2>/dev/null || true

# Créer un lien symbolique
ln -sf "$INSTALL_DIR/nightmod" "/usr/local/bin/nightmod"

# Créer un fichier .desktop
cat > "/usr/share/applications/nightmod.desktop" << EOF
[Desktop Entry]
Name=NightMod
Comment=Surveillant de sommeil et économiseur d'énergie
Exec=/opt/nightmod/nightmod
Icon=/opt/nightmod/assets/icon.png
Terminal=false
Type=Application
Categories=Utility;
EOF

echo "Installation terminée!"
echo "Vous pouvez lancer NightMod en tapant 'nightmod' dans le terminal ou en le recherchant dans votre menu d'applications."
"""
    
    # Créer un dossier temporaire pour l'installation
    os.makedirs("dist/package", exist_ok=True)
    
    # Copier l'exécutable
    if os.path.exists("dist/nightmod"):
        shutil.copy("dist/nightmod", "dist/package/")
    else:
        print("✗ L'exécutable n'a pas été créé correctement")
        return False
    
    # Écrire le script d'installation
    with open("dist/package/install.sh", "w") as f:
        f.write(install_script)
    
    # Rendre le script exécutable
    os.chmod("dist/package/install.sh", 0o755)
    
    # Copier les assets
    if os.path.exists("assets"):
        os.makedirs("dist/package/assets", exist_ok=True)
        for file in os.listdir("assets"):
            src = os.path.join("assets", file)
            if os.path.isfile(src):
                shutil.copy(src, os.path.join("dist/package/assets", file))
    
    # Créer une archive tar.gz
    archive_name = f"NightMod-{VERSION}-Linux"
    shutil.make_archive(f"release/{archive_name}", "gztar", "dist/package")
    print(f"✓ Archive Linux créée: release/{archive_name}.tar.gz")
    return True

def main():
    """Fonction principale"""
    current_system = platform.system()
    
    print_header(f"Compilation de NightMod v{VERSION}")
    print(f"Système détecté: {current_system}")
    
    # Vérifier les prérequis
    check_requirements()
    
    # Nettoyer les répertoires de compilation
    clean_build_dir()
    
    # Créer le dossier 'release' s'il n'existe pas
    os.makedirs("release", exist_ok=True)
    
    # Compiler pour la plateforme actuelle
    success = False
    
    if current_system == "Windows":
        success = build_for_windows()
    elif current_system == "Darwin":  # macOS
        success = build_for_macos()
    elif current_system == "Linux":
        success = build_for_linux()
    else:
        print(f"Système non pris en charge: {current_system}")
        sys.exit(1)
    
    # Afficher le résultat final
    if success:
        print_header("Compilation terminée avec succès")
        print(f"Les fichiers compilés sont disponibles dans le dossier 'release'")
    else:
        print_header("La compilation a échoué")
        print("Consultez les messages d'erreur ci-dessus pour plus d'informations")
        sys.exit(1)


if __name__ == "__main__":
    main()