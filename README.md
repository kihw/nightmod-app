# NightMod

NightMod est une extension légère pour les navigateurs qui permet d'activer un mode sombre personnalisable sur n'importe quel site web.

## Fonctionnalités

- **Mode sombre automatique** : Convertit automatiquement les sites web en mode sombre
- **Personnalisation** : Configurez les couleurs et le contraste selon vos préférences
- **Règles par site** : Définissez des règles spécifiques pour certains sites web
- **Performance optimisée** : Impact minimal sur les performances de navigation
- **Compatibilité multiple** : Fonctionne sur Chrome, Firefox et Edge

## Installation

### Chrome / Edge

1. Téléchargez le répertoire ou clonez-le via `git clone https://github.com/kihw/nightmod.git`
2. Ouvrez la page des extensions de votre navigateur (`chrome://extensions/` ou `edge://extensions/`)
3. Activez le "Mode développeur"
4. Cliquez sur "Charger l'extension non empaquetée" et sélectionnez le dossier du projet

### Firefox

1. Téléchargez le répertoire ou clonez-le via `git clone https://github.com/kihw/nightmod.git`
2. Naviguez vers `about:debugging#/runtime/this-firefox`
3. Cliquez sur "Charger un module temporaire"
4. Sélectionnez le fichier `manifest.json` dans le dossier du projet

## Utilisation

- Cliquez sur l'icône de l'extension dans la barre d'outils pour activer/désactiver le mode sombre
- Accédez aux paramètres en cliquant sur l'icône d'engrenage
- Personnalisez les couleurs, le contraste et d'autres options selon vos préférences

## Configuration avancée

Vous pouvez personnaliser davantage l'extension en modifiant les options dans le panneau de configuration :

- **Niveau d'intensité** : Ajustez l'intensité du mode sombre (0-100%)
- **Exclusions** : Ajoutez des sites à la liste d'exclusion où le mode sombre ne sera pas appliqué
- **Règles CSS personnalisées** : Définissez vos propres règles CSS pour des sites spécifiques

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
