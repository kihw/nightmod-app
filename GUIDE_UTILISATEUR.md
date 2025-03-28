# Guide Utilisateur - NightMod

Ce guide vous aidera à utiliser efficacement NightMod, l'outil qui surveille votre activité et éteint automatiquement votre ordinateur lorsque vous vous endormez.

## Table des matières

1. [Installation](#installation)
2. [Démarrage](#démarrage)
3. [Configuration](#configuration)
4. [Utilisation quotidienne](#utilisation-quotidienne)
5. [Dépannage](#dépannage)
6. [FAQ](#faq)

## Installation

### Windows

1. Téléchargez le fichier d'installation `NightMod-Setup-x.x.x.exe` depuis la page des [releases](https://github.com/kihw/nightmod/releases)
2. Double-cliquez sur le fichier et suivez les instructions à l'écran
3. Une fois l'installation terminée, NightMod sera disponible dans le menu Démarrer et sur votre bureau

### macOS

1. Téléchargez le fichier `NightMod-x.x.x.dmg` depuis la page des [releases](https://github.com/kihw/nightmod/releases)
2. Ouvrez le fichier DMG et faites glisser l'application NightMod vers votre dossier Applications
3. Lors du premier lancement, macOS pourrait vous demander de confirmer l'ouverture

### Linux

1. Téléchargez le fichier `NightMod-x.x.x-Linux.tar.gz` depuis la page des [releases](https://github.com/kihw/nightmod/releases)
2. Extrayez l'archive: `tar -xzf NightMod-x.x.x-Linux.tar.gz`
3. Accédez au répertoire extrait: `cd NightMod-x.x.x-Linux`
4. Exécutez le script d'installation: `sudo ./install.sh`

## Démarrage

1. Lancez NightMod depuis le menu de votre système ou le raccourci sur le bureau
2. À la première exécution, configurez les options selon vos préférences
3. Cliquez sur "Démarrer la surveillance" pour activer NightMod

## Configuration

### Options principales

- **Intervalle entre les vérifications**: Définit le temps (en minutes) entre chaque vérification. Valeur recommandée: 20 minutes.
- **Temps de réponse maximum**: Combien de temps (en secondes) vous avez pour répondre à la notification avant que l'ordinateur ne s'éteigne. Valeur recommandée: 30 secondes.
- **Action en cas d'inactivité**: Choisissez ce que NightMod doit faire si vous ne répondez pas:
  - `shutdown`: Éteindre complètement l'ordinateur
  - `sleep`: Mettre l'ordinateur en veille
  - `lock`: Simplement verrouiller l'écran

### Options supplémentaires

- **Activer le son de notification**: Si activé, un son sera joué lors de l'apparition de la fenêtre de vérification
- **Démarrer la surveillance automatiquement**: Si activé, NightMod démarrera automatiquement la surveillance à chaque lancement
- **Minimiser dans la barre des tâches**: Si activé, NightMod sera réduit dans la barre des tâches au lieu de s'afficher dans la barre des applications

## Utilisation quotidienne

1. **Démarrage de la surveillance**: Cliquez sur le bouton "Démarrer la surveillance" dans l'interface principale
2. **Fenêtre de vérification**: Périodiquement, une fenêtre apparaîtra vous demandant si vous êtes éveillé
   - Si vous êtes éveillé, cliquez sur le bouton "Je suis éveillé" ou appuyez sur la touche Échap
   - Si vous ne répondez pas dans le délai imparti, l'action configurée (extinction, veille, verrouillage) sera exécutée
3. **État de la surveillance**: L'interface principale affiche le temps restant avant la prochaine vérification
4. **Arrêt de la surveillance**: Cliquez sur "Arrêter la surveillance" pour désactiver les vérifications

## Dépannage

### La fenêtre de vérification n'apparaît pas

- Vérifiez que NightMod est bien en cours d'exécution (visible dans la barre des tâches)
- Assurez-vous qu'aucune autre application n'est en mode plein écran
- Redémarrez NightMod

### L'ordinateur ne s'éteint pas automatiquement

- Vérifiez que vous avez accordé les autorisations nécessaires à NightMod
- Sur macOS et Linux, des autorisations supplémentaires peuvent être nécessaires
- Essayez de changer l'action en cas d'inactivité (par exemple, utilisez "verrouiller" au lieu de "éteindre")

### NightMod utilise trop de ressources

- Augmentez l'intervalle entre les vérifications
- Fermez l'interface principale et laissez NightMod fonctionner en arrière-plan

## FAQ

### Puis-je programmer des heures spécifiques pour les vérifications?

Non, actuellement NightMod fonctionne avec un intervalle régulier dès que la surveillance est activée.

### NightMod peut-il détecter automatiquement si je suis inactif?

Non, NightMod utilise spécifiquement une méthode de vérification active qui nécessite votre réponse. Cela garantit que vous êtes non seulement présent, mais aussi éveillé.

### NightMod fonctionne-t-il pendant les présentations ou les vidéos?

Oui, mais vous devrez toujours répondre aux vérifications. Si vous souhaitez éviter les interruptions, désactivez temporairement NightMod.

### NightMod enregistre-t-il des données sur mon activité?

Non, NightMod n'enregistre aucune donnée sur votre activité. L'application fonctionne entièrement en local sur votre ordinateur.

### Comment puis-je désinstaller NightMod?

**Windows**:
Utilisez l'option "Ajouter ou supprimer des programmes" dans les paramètres Windows

**macOS**:
Faites glisser l'application de votre dossier Applications vers la corbeille

**Linux**:
Exécutez les commandes suivantes:

```bash
sudo rm /usr/local/bin/nightmod
sudo rm /usr/share/applications/nightmod.desktop
sudo rm -rf /opt/nightmod
```
