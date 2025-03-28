# Makefile pour NightMod

.PHONY: all run clean build install dev test lint help

PYTHON = python3
PIP = $(PYTHON) -m pip

# Detecter le système d'exploitation
ifeq ($(OS),Windows_NT)
	INSTALL_SCRIPT = install.bat
	RM = rmdir /s /q
	MKDIR = mkdir
else
	INSTALL_SCRIPT = ./install.sh
	RM = rm -rf
	MKDIR = mkdir -p
endif

# Commande par défaut
all: help

# Exécuter l'application
run:
	$(PYTHON) run.py

# Nettoyer les fichiers générés
clean:
	@echo "Nettoyage des fichiers générés..."
	$(RM) build dist release 2>/dev/null || true
	$(RM) *.egg-info 2>/dev/null || true
	find . -type d -name "__pycache__" -exec $(RM) {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	find . -name ".DS_Store" -delete
	find . -name "*.log" -delete

# Compiler l'application en exécutables
build:
	@echo "Compilation de l'application..."
	$(PYTHON) build.py

# Installer l'application
install:
	@echo "Installation des dépendances..."
	$(PIP) install -r requirements.txt
ifeq ($(OS),Windows_NT)
	@echo "Installation de l'application (Windows)..."
	$(INSTALL_SCRIPT)
else
	@echo "Installation de l'application (Unix)..."
	$(INSTALL_SCRIPT)
endif

# Configurer l'environnement de développement
dev:
	@echo "Configuration de l'environnement de développement..."
	$(PIP) install -e ".[all]"
	$(PIP) install -r requirements-dev.txt

# Exécuter les tests unitaires
test:
	@echo "Exécution des tests..."
	$(PYTHON) -m pytest tests/

# Vérifier le code avec les linters
lint:
	@echo "Vérification du code avec flake8..."
	flake8 src/
	@echo "Vérification du code avec pylint..."
	pylint src/

# Afficher l'aide
help:
	@echo "NightMod Makefile"
	@echo ""
	@echo "Commandes disponibles:"
	@echo "  make run      - Exécuter l'application"
	@echo "  make build    - Compiler l'application"
	@echo "  make install  - Installer l'application"
	@echo "  make clean    - Nettoyer les fichiers générés"
	@echo "  make dev      - Configurer l'environnement de développement"
	@echo "  make test     - Exécuter les tests unitaires"
	@echo "  make lint     - Vérifier le code avec les linters"
	@echo "  make help     - Afficher cette aide"