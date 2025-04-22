# NightMod

NightMod est une application de bureau légère qui surveille votre activité et éteint ou verrouille automatiquement votre ordinateur lorsque vous vous endormez.

## Fonctionnalités

- **Surveillance intelligente** : Détecte l'inactivité et vérifie si vous êtes endormi
- **Actions configurables** : Extinction, mise en veille ou verrouillage de l'écran
- **Interface moderne** : Design sombre confortable pour une utilisation nocturne
- **Icône dans la barre des tâches** : Contrôle facile depuis la barre système
- **Compatibilité multiple** : Fonctionne sur Windows, macOS et Linux

## Installation

### Windows

1. Téléchargez le fichier d'installation `NightMod-Setup-x.x.x.exe` depuis la page des [releases](https://github.com/kihw/nightmod-app/releases)
2. Double-cliquez sur le fichier et suivez les instructions à l'écran
3. Une fois l'installation terminée, NightMod sera disponible dans le menu Démarrer et sur votre bureau

### macOS

1. Téléchargez le fichier `NightMod-x.x.x.dmg` depuis la page des [releases](https://github.com/kihw/nightmod-app/releases)
2. Ouvrez le fichier DMG et faites glisser l'application NightMod vers votre dossier Applications
3. Lors du premier lancement, macOS pourrait vous demander de confirmer l'ouverture

### Linux

1. Téléchargez le fichier `NightMod-x.x.x-Linux.tar.gz` depuis la page des [releases](https://github.com/kihw/nightmod-app/releases)
2. Extrayez l'archive: `tar -xzf NightMod-x.x.x-Linux.tar.gz`
3. Accédez au répertoire extrait: `cd NightMod-x.x.x-Linux`
4. Exécutez le script d'installation: `sudo ./install.sh`

## Utilisation

- Lancez NightMod depuis le menu de votre système ou le raccourci sur le bureau
- Configurez les options selon vos préférences (intervalle de vérification, action à effectuer)
- Cliquez sur "Démarrer la surveillance" pour activer NightMod
- L'application vous demandera périodiquement si vous êtes éveillé
- Si vous ne répondez pas, l'action configurée (extinction, veille, verrouillage) sera exécutée

Pour plus de détails, consultez le [Guide d'utilisation](GUIDE_UTILISATEUR.md).

## Développement

### Prérequis

- Python 3.6 ou supérieur
- Tkinter (interface graphique)
- Les dépendances listées dans `requirements.txt`

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Pour le développement :

```bash
pip install -r requirements-dev.txt
```

### Exécution depuis les sources

```bash
python run.py
```

### Compilation

```bash
python build.py
```

## Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add some amazing feature'`)
4. Poussez vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Contact

Si vous avez des questions ou des suggestions, n'hésitez pas à ouvrir une issue sur GitHub.
