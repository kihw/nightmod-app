# Structure du projet NightMod

L'application NightMod est organisée selon une architecture modulaire pour faciliter sa maintenance et son évolution.

## Arborescence des fichiers

```
nightmod/
├── nightmod.py               # Point d'entrée principal de l'application
├── README.md                 # Documentation générale
├── GUIDE_UTILISATEUR.md      # Guide d'utilisation détaillé
├── LICENSE                   # Licence du projet
├── requirements.txt          # Dépendances Python
├── build.py                  # Script de compilation
├── install.sh                # Script d'installation pour Linux
├── install.bat               # Script d'installation pour Windows
├── src/                      # Code source de l'application
│   ├── __init__.py           # Initialisation du package
│   ├── app.py                # Classe principale de l'application
│   ├── config.py             # Gestion de la configuration
│   ├── popup.py              # Interface de la fenêtre de vérification
│   ├── system_actions.py     # Actions système (extinction, veille, etc.)
│   └── tray.py               # Gestion de l'icône dans la barre des tâches
├── themes/                   # Thèmes d'interface utilisateur
│   └── azure.tcl             # Thème Azure pour une interface moderne
└── assets/                   # Ressources de l'application
    ├── icon.ico              # Icône pour Windows
    ├── icon.png              # Icône pour Linux/macOS
    └── alert.wav             # Son de notification
```

## Description des modules

### 1. Module principal (`nightmod.py`)

- Point d'entrée de l'application
- Initialise le système de journalisation (logging)
- Gère les exceptions non capturées

### 2. Classe principale (`src/app.py`)

- Contient la classe `NightModApp` qui hérite de `tk.Tk`
- Gère l'interface utilisateur principale
- Orchestre les différents composants
- Implémente la logique de surveillance et de vérification

### 3. Gestionnaire de configuration (`src/config.py`)

- Classe `ConfigManager` pour charger et sauvegarder la configuration
- Gestion des paramètres par défaut
- Stockage persistant des préférences utilisateur

### 4. Actions système (`src/system_actions.py`)

- Classe `SystemActions` avec des méthodes statiques pour:
  - Éteindre l'ordinateur
  - Mettre en veille
  - Verrouiller l'écran
  - Configurer le démarrage automatique

### 5. Interface de vérification (`src/popup.py`)

- Classe `PopupChecker` qui hérite de `tk.Toplevel`
- Affiche la fenêtre de vérification avec compte à rebours
- Gère les interactions utilisateur

### 6. Gestion de la barre des tâches (`src/tray.py`)

- Classe `TrayIcon` pour l'intégration dans la barre des tâches
- Implémentation avec pystray (optionnel)

### 7. Thèmes (`themes/`)

- Fichiers de thème pour personnaliser l'interface utilisateur
- Le thème Azure offre une interface moderne de type Fluent Design

### 8. Ressources (`assets/`)

- Icônes et sons utilisés par l'application

## Flux de données

1. L'utilisateur interagit avec l'interface (`NightModApp`)
2. Les paramètres sont stockés via `ConfigManager`
3. La surveillance est gérée par un thread dédié dans `NightModApp`
4. Les vérifications sont affichées via `PopupChecker`
5. Les actions système sont exécutées via `SystemActions`

## Conception

- L'architecture est modulaire pour faciliter les tests et la maintenance
- Compatibilité multi-plateforme (Windows, macOS, Linux)
- Interface utilisateur responsive avec support des thèmes
- Gestion robuste des erreurs et journalisation
