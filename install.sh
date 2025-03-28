#!/bin/bash
# Script d'installation pour NightMod (Linux)

echo "Installation de NightMod..."

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "Python 3 n'est pas installé. Veuillez installer Python 3 avant de continuer."
    exit 1
fi

# Vérifier si pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "pip n'est pas installé. Installation..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Créer répertoire de destination
INSTALL_DIR="$HOME/.local/share/nightmod"
mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/assets"

# Copier les fichiers
echo "Copie des fichiers..."
cp nightmod.py "$INSTALL_DIR/"
cp -r assets/* "$INSTALL_DIR/assets/" 2>/dev/null || true
cp requirements.txt "$INSTALL_DIR/" 2>/dev/null || true

# Installer les dépendances
echo "Installation des dépendances..."
pip3 install -r requirements.txt

# Créer un lanceur
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"

cat > "$DESKTOP_DIR/nightmod.desktop" << EOF
[Desktop Entry]
Name=NightMod
Comment=Surveillant de sommeil et économiseur d'énergie
Exec=python3 $INSTALL_DIR/nightmod.py
Icon=$INSTALL_DIR/assets/icon.png
Terminal=false
Type=Application
Categories=Utility;
EOF

# Créer un lien symbolique dans le PATH
LINK_DIR="$HOME/.local/bin"
mkdir -p "$LINK_DIR"

cat > "$LINK_DIR/nightmod" << EOF
#!/bin/bash
python3 "$INSTALL_DIR/nightmod.py" "\$@"
EOF

chmod +x "$LINK_DIR/nightmod"

# Vérifier si $HOME/.local/bin est dans le PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "Ajout de ~/.local/bin au PATH..."
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo "Veuillez redémarrer votre terminal ou exécuter 'source ~/.bashrc' pour mettre à jour le PATH."
fi

echo "Installation terminée!"
echo "Vous pouvez lancer NightMod en tapant 'nightmod' dans le terminal ou en le recherchant dans votre menu d'applications."