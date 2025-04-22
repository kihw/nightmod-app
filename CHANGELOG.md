# Journal des modifications (Changelog)

Toutes les modifications notables apportées à ce projet seront documentées dans ce fichier.

Ce format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Non publié]

### Ajouté
- Script tools/generate_icons.py pour générer des icônes PNG à partir de l'icône ICO
- Dossier assets/img pour stocker les icônes au format PNG
- README.md pour le répertoire tools

### Modifié
- Refactorisation complète de nightmod.py pour servir uniquement de point d'entrée
- Mise à jour du fichier run.py pour une meilleure gestion des importations et des dépendances
- Amélioration des fichiers requirements.txt et requirements-dev.txt
- Restructuration du fichier README.md pour refléter correctement la nature de l'application
- Correction du doublon de la méthode setup_style dans src/popup.py

### Corrigé
- Problème de doublon de la méthode setup_style dans src/popup.py
- Problème d'initialisation de la variable initial_time dans src/popup.py
- Problèmes d'importation dans le point d'entrée principal

## [1.0.0] - 2025-04-21
### Ajouté
- Première version de l'application NightMod
- Fonctionnalité de surveillance périodique
- Interface utilisateur moderne avec thème sombre
- Support multi-plateforme (Windows, macOS, Linux)
- Icône dans la barre des tâches
- Documentation utilisateur
