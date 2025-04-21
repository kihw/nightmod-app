#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import tempfile
import unittest
import sys
import shutil

# Ajouter le répertoire parent au chemin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importer le module à tester
from src.config import ConfigManager, DEFAULT_CONFIG

class TestConfigManager(unittest.TestCase):
    """Tests pour le gestionnaire de configuration"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        # Créer un répertoire temporaire pour les tests
        self.test_dir = tempfile.mkdtemp()
        # Sauvegarder le chemin original
        self.original_config_dir = os.environ.get('NIGHTMOD_CONFIG_DIR')
        # Définir le répertoire de configuration à notre répertoire de test
        os.environ['NIGHTMOD_CONFIG_DIR'] = self.test_dir
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        # Supprimer le répertoire temporaire
        shutil.rmtree(self.test_dir)
        # Restaurer le chemin original
        if self.original_config_dir:
            os.environ['NIGHTMOD_CONFIG_DIR'] = self.original_config_dir
        else:
            os.environ.pop('NIGHTMOD_CONFIG_DIR', None)
    
    def test_default_config(self):
        """Vérifie que la configuration par défaut est correctement chargée"""
        config_manager = ConfigManager()
        config = config_manager.get_all()
        self.assertEqual(config, DEFAULT_CONFIG)
    
    def test_save_and_load(self):
        """Vérifie que la sauvegarde et le chargement fonctionnent"""
        # Créer une instance et modifier la configuration
        config_manager = ConfigManager()
        config_manager.set('check_interval_minutes', 30)
        config_manager.set('sound_enabled', False)
        
        # Créer une nouvelle instance pour charger la configuration
        new_config_manager = ConfigManager()
        config = new_config_manager.get_all()
        
        # Vérifier que les modifications ont été sauvegardées
        self.assertEqual(config['check_interval_minutes'], 30)
        self.assertEqual(config['sound_enabled'], False)
        
        # Vérifier que les autres valeurs sont toujours par défaut
        self.assertEqual(config['response_time_seconds'], DEFAULT_CONFIG['response_time_seconds'])
    
    def test_update_multiple(self):
        """Vérifie que la mise à jour de plusieurs paramètres fonctionne"""
        config_manager = ConfigManager()
        
        # Mettre à jour plusieurs paramètres
        new_values = {
            'check_interval_minutes': 45,
            'shutdown_action': 'sleep',
            'minimize_to_tray': False
        }
        config_manager.update(new_values)
        
        # Vérifier les modifications
        config = config_manager.get_all()
        self.assertEqual(config['check_interval_minutes'], 45)
        self.assertEqual(config['shutdown_action'], 'sleep')
        self.assertEqual(config['minimize_to_tray'], False)
    
    def test_reset(self):
        """Vérifie que la réinitialisation fonctionne"""
        config_manager = ConfigManager()
        
        # Modifier plusieurs paramètres
        config_manager.set('check_interval_minutes', 60)
        config_manager.set('response_time_seconds', 15)
        
        # Réinitialiser
        config_manager.reset()
        
        # Vérifier que tout est revenu à la valeur par défaut
        config = config_manager.get_all()
        self.assertEqual(config, DEFAULT_CONFIG)

if __name__ == '__main__':
    unittest.main()