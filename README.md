# NightMod

NightMod est un utilitaire simple qui aide à économiser de l'énergie et à protéger votre système lorsque vous vous endormez devant votre ordinateur.

## Fonctionnement

NightMod surveille votre activité en affichant périodiquement une fenêtre popup à laquelle vous devez répondre :

1. À intervalles réguliers (configurables), une fenêtre apparaît sur votre écran
2. Si vous répondez à cette fenêtre, le programme considère que vous êtes éveillé et reprend son cycle de surveillance
3. Si vous ne répondez pas dans le délai imparti, le programme considère que vous vous êtes endormi et éteint automatiquement votre ordinateur

## Caractéristiques

- **Intervalles configurables** : Définissez la fréquence des vérifications (par défaut: 20 minutes)
- **Délai de réponse réglable** : Configurez le temps disponible pour répondre (par défaut: 30 secondes)
- **Options d'extinction** : Choisissez entre éteindre, mettre en veille, ou simplement verrouiller l'écran
- **Interface minimaliste** : Design simple et non-intrusif
- **Mode silencieux** : Option pour désactiver les sons de notification
- **Démarrage automatique** : Possibilité de lancer NightMod au démarrage du système

## Installation

### Windows

1. Téléchargez la dernière version depuis la page des [releases](https://github.com/kihw/nightmod/releases)
2. Exécutez le fichier `nightmod-setup.exe` et suivez les instructions
3. L'application sera accessible depuis la barre des tâches

### Linux

1. Téléchargez la dernière version depuis la page des [releases](https://github.com/kihw/nightmod/releases)
2. Extrayez l'archive téléchargée
3. Exécutez le script d'installation : `./install.sh`
4. Lancez l'application avec la commande `nightmod` ou depuis le menu des applications

### macOS

1. Téléchargez la dernière version depuis la page des [releases](https://github.com/kihw/nightmod/releases)
2. Ouvrez le fichier .dmg et faites glisser l'application dans votre dossier Applications
3. Lancez NightMod depuis votre dossier Applications ou Launchpad

## Utilisation

1. Lancez NightMod
2. Cliquez sur l'icône dans la barre des tâches/barre d'état système pour accéder aux paramètres
3. Configurez les intervalles et options selon vos préférences
4. L'application s'exécute en arrière-plan et affiche des popups de vérification selon l'intervalle configuré

### Raccourcis clavier

- `Esc` : Fermer la fenêtre de vérification (compte comme une réponse)
- `Alt+N` : Afficher/masquer la fenêtre principale de configuration
- `Alt+Q` : Quitter l'application

## Configuration

Les options suivantes peuvent être configurées:

- **Intervalle entre les vérifications** : 5 à 120 minutes
- **Temps de réponse** : 15 à 60 secondes
- **Action si aucune réponse** : Éteindre, mettre en veille, verrouiller l'écran
- **Son** : Activer/désactiver les notifications sonores
- **Démarrage automatique** : Lancer au démarrage du système

## Pour les développeurs

### Prérequis

- Python 3.6 ou supérieur
- Bibliothèques: tkinter, pyautogui, psutil

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Exécution depuis le code source

```bash
python nightmod.py
```

### Compilation

```bash
# Pour Windows
pyinstaller --onefile --windowed --icon=assets/icon.ico nightmod.py

# Pour Linux
pyinstaller --onefile --windowed --icon=assets/icon.png nightmod.py

# Pour macOS
pyinstaller --onefile --windowed --icon=assets/icon.icns nightmod.py
```

## Contribution

Les contributions sont les bienvenues! Si vous souhaitez améliorer NightMod:

1. Forkez le dépôt
2. Créez une branche pour votre fonctionnalité
3. Faites vos modifications
4. Soumettez une pull request

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Contact

Pour toute question ou suggestion, veuillez ouvrir une issue sur le dépôt GitHub.
