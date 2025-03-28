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
    
    icon_path = os.path.join("assets", "icon.ico")
    if not os.path.exists(icon_path):
        print("! Icône non trouvée, utilisation de l'icône par défaut")
        icon_path = None
    
    cmd = [
        "pyinstaller",
        "--name=NightMod",
        "--onefile",
        "--windowed",
        f"--version-file=VERSION",
    ]
    
    if icon_path:
        cmd.append(f"--icon={icon_path}")
    
    cmd.append("nightmod.py")
    
    # Créer un fichier de version pour Windows
    with open("VERSION", "w") as f:
        f.write(f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'NightMod'),
          StringStruct(u'FileDescription', u'Surveillant de sommeil et économiseur d'énergie'),
          StringStruct(u'FileVersion', u'{VERSION}'),
          StringStruct(u'InternalName', u'nightmod'),
          StringStruct(u'LegalCopyright', u'© 2025 NightMod'),
          StringStruct(u'OriginalFilename', u'NightMod.exe'),
          StringStruct(u'ProductName', u'NightMod'),
          StringStruct(u'ProductVersion', u'{VERSION}')])
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
""")
    
    # Exécuter PyInstaller
    subprocess.run(cmd, check=True)
    
    # Créer le dossier 'release' s'il n'existe pas
    os.makedirs("release", exist_ok=True)
    
    # Compiler pour la plateforme actuelle
    if current_system == "Windows":
        build_for_windows()
    elif current_system == "Darwin":  # macOS
        build_for_macos()
    elif current_system == "Linux":
        build_for_linux()
    else:
        print(f"Système non pris en charge: {current_system}")
        return
    
    print_header("Compilation terminée")
    print(f"Les fichiers compilés sont disponibles dans le dossier 'release'")


if __name__ == "__main__":
    main()=True)
    
    # Créer un fichier d'installation NSIS
    with open("installer.nsi", "w") as f:
        f.write(f"""
!include "MUI2.nsh"

Name "NightMod"
OutFile "release\\NightMod-Setup-{VERSION}.exe"
InstallDir "$PROGRAMFILES\\NightMod"
RequestExecutionLevel admin

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "French"

Section "Install"
  SetOutPath "$INSTDIR"
  File "dist\\NightMod.exe"
  
  ; Créer le répertoire pour les icônes
  CreateDirectory "$INSTDIR\\assets"
  SetOutPath "$INSTDIR\\assets"
  File "assets\\icon.ico"
  
  ; Créer le dossier dans le menu Démarrer
  CreateDirectory "$SMPROGRAMS\\NightMod"
  CreateShortcut "$SMPROGRAMS\\NightMod\\NightMod.lnk" "$INSTDIR\\NightMod.exe" "" "$INSTDIR\\assets\\icon.ico"
  CreateShortcut "$SMPROGRAMS\\NightMod\\Désinstaller.lnk" "$INSTDIR\\uninstall.exe"
  
  ; Créer un raccourci sur le bureau
  CreateShortcut "$DESKTOP\\NightMod.lnk" "$INSTDIR\\NightMod.exe" "" "$INSTDIR\\assets\\icon.ico"
  
  ; Créer le désinstallateur
  WriteUninstaller "$INSTDIR\\uninstall.exe"
  
  ; Ajouter des informations au désinstallateur
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\NightMod" "DisplayName" "NightMod"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\NightMod" "UninstallString" "$\\"$INSTDIR\\uninstall.exe$\\""
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\NightMod" "DisplayIcon" "$\\"$INSTDIR\\assets\\icon.ico$\\""
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\NightMod" "DisplayVersion" "{VERSION}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\NightMod" "Publisher" "NightMod"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\\NightMod.exe"
  Delete "$INSTDIR\\assets\\icon.ico"
  Delete "$INSTDIR\\uninstall.exe"
  
  RMDir "$INSTDIR\\assets"
  RMDir "$INSTDIR"
  
  Delete "$SMPROGRAMS\\NightMod\\NightMod.lnk"
  Delete "$SMPROGRAMS\\NightMod\\Désinstaller.lnk"
  RMDir "$SMPROGRAMS\\NightMod"
  
  Delete "$DESKTOP\\NightMod.lnk"
  
  DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\NightMod"
SectionEnd
""")
    
    # Vérifier si NSIS est installé
    try:
        subprocess.run(
            ["makensis", "installer.nsi"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"✓ Installateur Windows créé: release/NightMod-Setup-{VERSION}.exe")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("! NSIS non trouvé, l'installateur Windows n'a pas été créé")
        print(f"✓ Executable Windows créé: dist/NightMod.exe")
        
        # Copier l'exécutable dans le dossier release
        shutil.copy("dist/NightMod.exe", f"release/NightMod-{VERSION}.exe")

def build_for_macos():
    """Compile l'application pour macOS"""
    print_header("Compilation pour macOS")
    
    icon_path = os.path.join("assets", "icon.icns")
    if not os.path.exists(icon_path):
        print("! Icône .icns non trouvée, utilisation de l'icône par défaut")
        icon_path = None
    
    cmd = [
        "pyinstaller",
        "--name=NightMod",
        "--onefile",
        "--windowed",
    ]
    
    if icon_path:
        cmd.append(f"--icon={icon_path}")
    
    cmd.append("nightmod.py")
    
    # Exécuter PyInstaller
    subprocess.run(cmd, check=True)
    
    # Créer le dossier 'release' s'il n'existe pas
    os.makedirs("release", exist_ok=True)
    
    # Créer un DMG
    try:
        subprocess.run([
            "hdiutil", "create",
            "-volname", "NightMod",
            "-srcfolder", "dist/NightMod.app",
            "-ov", "-format", "UDZO",
            f"release/NightMod-{VERSION}.dmg"
        ], check=True)
        print(f"✓ Image disque macOS créée: release/NightMod-{VERSION}.dmg")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("! Impossible de créer l'image disque DMG")
        print(f"✓ Application macOS créée: dist/NightMod.app")
        
        # Copier l'application dans le dossier release
        shutil.copytree("dist/NightMod.app", f"release/NightMod-{VERSION}.app", dirs_exist_ok=True)

def build_for_linux():
    """Compile l'application pour Linux"""
    print_header("Compilation pour Linux")
    
    icon_path = os.path.join("assets", "icon.png")
    if not os.path.exists(icon_path):
        print("! Icône non trouvée, utilisation de l'icône par défaut")
        icon_path = None
    
    cmd = [
        "pyinstaller",
        "--name=nightmod",
        "--onefile",
        "--windowed",
    ]
    
    if icon_path:
        cmd.append(f"--icon={icon_path}")
    
    cmd.append("nightmod.py")
    
    # Exécuter PyInstaller
    subprocess.run(cmd, check=True)
    
    # Créer le dossier 'release' s'il n'existe pas
    os.makedirs("release", exist_ok=True)
    
    # Créer un script d'installation
    with open("dist/install.sh", "w") as f:
        f.write("""#!/bin/bash
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
""")
    
    # Rendre le script exécutable
    os.chmod("dist/install.sh", 0o755)
    
    # Copier les assets
    if os.path.exists("assets"):
        os.makedirs("dist/assets", exist_ok=True)
        for file in os.listdir("assets"):
            src = os.path.join("assets", file)
            if os.path.isfile(src):
                shutil.copy(src, os.path.join("dist/assets", file))
    
    # Créer une archive tar.gz
    archive_name = f"NightMod-{VERSION}-Linux"
    shutil.make_archive(f"release/{archive_name}", "gztar", "dist")
    print(f"✓ Archive Linux créée: release/{archive_name}.tar.gz")

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
    os.makedirs("release", exist_ok