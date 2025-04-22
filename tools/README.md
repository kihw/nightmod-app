# Outils de développement pour NightMod

Ce répertoire contient divers scripts et outils pour faciliter le développement et la maintenance de NightMod.

## Scripts disponibles

### generate_icons.py

Génère des icônes PNG à différentes tailles à partir de l'icône ICO principale.

**Utilisation:**

```bash
python tools/generate_icons.py
```

**Fonctionnalités:**
- Crée des icônes PNG aux tailles 16x16, 32x32, 48x48, 64x64, 128x128 et 256x256
- Génère des versions spéciales pour la barre des tâches (active et inactive)
- Stocke les icônes dans le répertoire `assets/img/`

**Dépendances:**
- Pillow (PIL) - `pip install pillow`

## Ajout d'un nouvel outil

Pour ajouter un nouvel outil à ce répertoire:

1. Créez un script Python avec une documentation claire
2. Ajoutez une description dans ce README.md
3. Assurez-vous que les dépendances nécessaires sont listées dans requirements-dev.txt
