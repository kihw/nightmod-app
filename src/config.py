#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de gestion de la configuration pour NightMod
"""

import os
import json
import logging

# Obtenir le logger
logger = logging.getLogger("NightMod.Config")

# Configuration par défaut
DEFAULT_CONFIG = {
    "check_interval_minutes": 20,
    "response_time_seconds": 30,
    "shutdown_action": "shutdown",  # Options: shutdown, sleep, lock
    "sound_enabled": True,
    "start_with_system": False,
    "minimize_to_tray": True
}

class ConfigManager:
    """Gère la configuration et la persiste sur le disque"""
    
    def __init__(self):
        """Initialise le gestionnaire de configuration"""
        # Trouver le répertoire de configuration approprié selon le système
        self.config_dir = os.path.join(os.path.expanduser("~"), ".nightmod")
        self.config_file = os.path.join(self.config_dir, "config.json")
        
        # S'assurer que le répertoire existe
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Charger la configuration
        self.config = self.load_config()
    
    def load_config(self):
        """Charge la configuration depuis le fichier ou retourne la configuration par défaut"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Fusionner avec les paramètres par défaut pour les nouvelles options
                    return {**DEFAULT_CONFIG, **config}
            return DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la configuration: {e}")
            return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Sauvegarde la configuration dans le fichier"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la configuration: {e}")
            return False
    
    def get(self, key, default=None):
        """Récupère une valeur de configuration avec une valeur par défaut"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Définit une valeur de configuration et la sauvegarde"""
        self.config[key] = value
        return self.save_config()
    
    def get_all(self):
        """Retourne la configuration complète"""
        return self.config
    
    def update(self, new_config):
        """Met à jour plusieurs paramètres de configuration à la fois"""
        for key, value in new_config.items():
            self.config[key] = value
        return self.save_config()
    
    def reset(self):
        """Réinitialise la configuration aux valeurs par défaut"""
        self.config = DEFAULT_CONFIG.copy()
        return self.save_config()