#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de gestion des popups de vérification pour NightMod
"""

import tkinter as tk
from tkinter import ttk
import logging
import os
import platform

# Obtenir le logger
logger = logging.getLogger("NightMod.Popup")

class PopupChecker(tk.Toplevel):
    """Fenêtre popup qui vérifie si l'utilisateur est éveillé"""
    
    def __init__(self, parent, response_time, on_response, on_timeout, config=None):
        super().__init__(parent)
        self.parent = parent
        self.response_time = response_time
        self.on_response = on_response
        self.on_timeout = on_timeout
        self.remaining_time = response_time
        self.config = config or {}
        self.animation_speed = 1  # Pour l'animation optionnelle
        
        # Configuration de la fenêtre
        self.title("NightMod - Vérification")
        self.geometry("450x300")  # Augmentation significative de la hauteur et largeur
        self.resizable(False, False)
        
        # Configurer le style
        self.setup_style()
        
        # Toujours au premier plan et centré
        self.attributes("-topmost", True)
        self.withdraw()  # Masquer d'abord
        self.update_idletasks()
        
        # Centrer la fenêtre sur l'écran
        self.center_window()
        
        # Rendre la fenêtre visible
        self.deiconify()
        
        # Jouer un son si activé
        self.play_sound()
        
        # Éléments d'interface
        self.create_widgets()
        
        # Démarrer le compte à rebours
        self.countdown()
    
    def setup_style(self):
        """Configure le style de la fenêtre"""
        # Utiliser un thème sombre pour moins fatiguer les yeux
        self.configure(background="#2E2E2E")
        
        self.style = ttk.Style(self)
        
        # Configuration générale du style
        self.style.configure("TFrame", background="#2E2E2E")
        self.style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
        self.style.configure("Time.TLabel", font=("Segoe UI", 12), foreground="#F0F0F0")
        
        # Style du bouton principal
        self.style.configure("Accent.TButton", 
                             font=("Segoe UI", 11),
                             padding=8,
                             background="#4285f4")
        
        # Tenter de charger un thème moderne si disponible
        if platform.system() == "Windows":
            try:
                from tkinter import _tkinter
                self.tk.call("source", "themes/azure.tcl")
                self.tk.call("set_theme", "dark")
            except Exception:
                pass
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"+{x}+{y}")
    
    def play_sound(self):
        """Joue un son de notification si activé"""
        if self.config.get("sound_enabled", True):
            try:
                self.bell()
                
                # Essayer de jouer un son plus approprié si disponible
                sound_file = None
                
                if platform.system() == "Windows":
                    import winsound
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                elif platform.system() == "Darwin":  # macOS
                    sound_file = "/System/Library/Sounds/Sosumi.aiff"
                else:  # Linux
                    # Essayer plusieurs méthodes pour jouer un son
                    try:
                        import subprocess
                        subprocess.run(["aplay", "-q", "assets/alert.wav"], 
                                      stderr=subprocess.DEVNULL, 
                                      stdout=subprocess.DEVNULL)
                    except:
                        pass
            except Exception as e:
                logger.warning(f"Impossible de jouer le son: {e}")
    
    def create_widgets(self):
        """Crée les éléments d'interface de la fenêtre popup"""
        main_frame = ttk.Frame(self, padding="25 25 25 40")  # Augmentation significative du padding
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Icône
        try:
            if platform.system() == "Windows" and os.path.exists("assets/icon.png"):
                icon = tk.PhotoImage(file="assets/icon.png")
                icon = icon.subsample(4, 4)  # Réduire la taille
                logo_label = ttk.Label(main_frame, image=icon, background="#2E2E2E")
                logo_label.image = icon  # Garder une référence
                logo_label.pack(pady=(0, 10))
        except Exception:
            pass
        
        # Message principal
        ttk.Label(
            main_frame, 
            text="Êtes-vous encore éveillé ?", 
            style="Title.TLabel"
        ).pack(pady=10)
        
        # Texte du compte à rebours
        self.time_label = ttk.Label(
            main_frame, 
            text=f"Temps restant: {self.remaining_time} secondes",
            style="Time.TLabel"
        )
        self.time_label.pack(pady=10)
        
        # Bouton de réponse
        response_button = ttk.Button(
            main_frame, 
            text="Je suis éveillé",
            command=self.handle_response,
            style="Accent.TButton",
            width=20  # Fixer la largeur du bouton
        )
        response_button.pack(pady=20)  # Augmentation du padding vertical
        response_button.focus_set()
        
        # Information supplémentaire
        ttk.Label(
            main_frame,
            text="Si vous ne répondez pas, votre ordinateur s'éteindra.",
            font=("Segoe UI", 9),
            foreground="#AAAAAA",
            background="#2E2E2E"
        ).pack(side=tk.BOTTOM, pady=(35, 0))  # Augmentation significative du padding supérieur
        
        # Gérer la touche Échap pour fermer
        self.bind("<Escape>", lambda e: self.handle_response())
        
        # Intercepter la fermeture de la fenêtre
        self.protocol("WM_DELETE_WINDOW", self.handle_response)
    
    def countdown(self):
        """Gère le compte à rebours et vérifie si le temps est écoulé"""
        if self.remaining_time > 0:
            # Mettre à jour le texte
            self.time_label.config(text=f"Temps restant: {self.remaining_time} secondes")
            
            # Faire clignoter si moins de 5 secondes
            if self.remaining_time <= 5:
                self.animate_warning()
            
            # Décrémenter le temps restant
            self.remaining_time -= 1
            
            # Continuer le compte à rebours
            self.after(1000, self.countdown)
        else:
            logger.info("Aucune réponse reçue dans le délai imparti")
            self.destroy()
            self.on_timeout()
    
    def animate_warning(self):
        """Anime le texte pour attirer l'attention"""
        if self.remaining_time <= 5 and self.remaining_time % 2 == 0:
            self.time_label.configure(foreground="#FF5555")  # Rouge
            # Jouer un son plus urgent si moins de 5 secondes
            self.bell()
        else:
            self.time_label.configure(foreground="#F0F0F0")  # Normal
    
    def handle_response(self, event=None):
        """Appelé quand l'utilisateur répond au popup"""
        logger.info("Réponse reçue de l'utilisateur")
        self.destroy()
        self.on_response()