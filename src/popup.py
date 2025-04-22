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
        self.initial_time = response_time  # Stockage du temps initial pour les calculs
        
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
        """Configure un style moderne et minimaliste pour la fenêtre popup"""
        # Utiliser un thème sombre pour moins fatiguer les yeux
        self.configure(background="#202020")

        self.style = ttk.Style(self)

        # Style de base sombre pour le confort nocturne
        self.style.configure("Dark.TFrame", background="#202020")
        self.style.configure("Dark.TLabel", background="#202020", foreground="#FFFFFF")

        # Texte du titre
        self.style.configure("Title.TLabel", 
                             background="#202020", 
                             foreground="#FFFFFF", 
                             font=("Segoe UI", 16, "bold"))

        # Style du compte à rebours
        self.style.configure("Time.TLabel", 
                             background="#202020", 
                             foreground="#4CAF50",  # Vert pour un départ calme
                             font=("Segoe UI", 32, "bold"))

        # Style info
        self.style.configure("Info.TLabel", 
                             background="#202020", 
                             foreground="#AAAAAA",
                             font=("Segoe UI", 9))

        # Style du bouton principal - Visible mais pas agressif
        self.style.configure("Sleep.TButton", 
                             font=("Segoe UI", 12, "bold"),
                             padding=12,
                             background="#4CAF50",
                             foreground="#FFFFFF")

        self.style.map("Sleep.TButton", 
                       background=[("pressed", "#3C9E3C"), ("active", "#3C9E3C")],
                       foreground=[("pressed", "#FFFFFF"), ("active", "#FFFFFF")])

        # Tenter de charger un thème moderne si disponible
        if platform.system() == "Windows":
            try:
                theme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "themes/azure.tcl")
                if os.path.exists(theme_path):
                    self.tk.call("source", theme_path)
                    self.tk.call("set_theme", "dark")
            except Exception as e:
                logger.warning(f"Impossible de charger le thème: {e}")

    def create_widgets(self):
        """Crée les éléments d'interface de la fenêtre popup avec un design plus élégant"""
        main_frame = ttk.Frame(self, padding="30 30 30 30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Fond légèrement plus foncé pour mieux ressortir la nuit
        main_frame.configure(style="Dark.TFrame")

        
        # Message principal - Plus grand et accrocheur
        title_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            title_frame, 
            text="Êtes-vous encore éveillé ?", 
            font=("Segoe UI", 16, "bold"),
            style="Title.TLabel"
        ).pack(anchor=tk.CENTER)
        
        # Indicateur visuel de compte à rebours (canvas)
        self.time_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        self.time_frame.pack(pady=(0, 15))
        
        # Créer l'indicateur visuel
        self.countdown_canvas = self.create_countdown_indicator(self.time_frame)
        
        # Bouton de réponse plus grand et plus visible
        button_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        button_frame.pack(pady=(5, 0))
        
        response_button = ttk.Button(
            button_frame, 
            text="Je suis éveillé",
            command=self.handle_response,
            style="Sleep.TButton",  # Style personnalisé plus visible
            width=20,
            padding=(10, 12)  # Bouton plus grand
        )
        response_button.pack(pady=15)
        response_button.focus_set()
        
        # Information de fermeture discrète
        info_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(25, 0))
        
        ttk.Label(
            info_frame,
            text="Appuyez sur Échap ou cliquez pour rester actif",
            font=("Segoe UI", 9),
            foreground="#AAAAAA",
            style="Info.TLabel"
        ).pack(side=tk.LEFT)
        
        action_text = {
            "shutdown": "extinction",
            "sleep": "mise en veille",
            "lock": "verrouillage"
        }.get(self.config.get('shutdown_action', 'shutdown'), "extinction")
        
        ttk.Label(
            info_frame,
            text=f"Action si inactif: {action_text}",
            font=("Segoe UI", 9),
            foreground="#AAAAAA",
            style="Info.TLabel"
        ).pack(side=tk.RIGHT)
        
        # Gérer la touche Échap pour fermer
        self.bind("<Escape>", lambda e: self.handle_response())
        
        # Intercepter la fermeture de la fenêtre
        self.protocol("WM_DELETE_WINDOW", self.handle_response)
    
    def countdown(self):
        """Gère le compte à rebours et vérifie si le temps est écoulé"""
        if self.remaining_time > 0:
            # Mettre à jour l'indicateur visuel
            self.update_countdown_indicator()
            
            # Faire clignoter si moins de 5 secondes
            if self.remaining_time <= 5:
                self.animate_warning()
                # Jouer un son plus urgent si moins de 5 secondes
                if self.remaining_time % 2 == 0:
                    self.bell()
            
            # Décrémenter le temps restant
            self.remaining_time -= 1
            
            # Continuer le compte à rebours
            self.after(1000, self.countdown)
        else:
            logger.info("Aucune réponse reçue dans le délai imparti")
            self.destroy()
            self.on_timeout()
    
    def center_window(self):
        """Centre la fenêtre sur l'écran et ajoute une légère animation de fondu"""
        width = 380  # Fixer la largeur
        height = 400  # Fixer la hauteur
        self.geometry(f"{width}x{height}")
        
        # Centre la fenêtre
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"+{x}+{y}")
        
        # Léger effet de fondu (uniquement si la plateforme le supporte)
        try:
            self.attributes("-alpha", 0.0)
            
            # Fonction pour augmenter progressivement l'opacité
            def fade_in(alpha=0.0):
                alpha += 0.1
                self.attributes("-alpha", min(alpha, 1.0))
                if alpha < 1.0:
                    self.after(20, lambda: fade_in(alpha))
                    
            # Démarrer l'effet de fondu
            self.after(100, fade_in)
        except:
            # Si l'attribut alpha n'est pas supporté, afficher directement
            pass
        
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
    
    def animate_warning(self):
        """Anime le texte pour attirer l'attention de façon progressive"""
        # Animation de l'indicateur visuel du compte à rebours
        # Cette méthode est appelée par update_countdown_indicator
        pass

    def create_countdown_indicator(self, parent):
        """Crée un indicateur visuel de compte à rebours circulaire"""
        # Créer un canvas pour l'indicateur circulaire
        self.canvas_size = 160
        self.canvas = tk.Canvas(
            parent,
            width=self.canvas_size,
            height=self.canvas_size,
            background="#202020",
            highlightthickness=0
        )
        self.canvas.pack(pady=(0, 10))
        
        # Paramètres de l'arc
        self.circle_radius = self.canvas_size * 0.4
        self.circle_width = self.canvas_size * 0.1
        self.circle_x = self.canvas_size / 2
        self.circle_y = self.canvas_size / 2
        
        # Cercle de fond (gris foncé)
        self.circle_bg = self.canvas.create_oval(
            self.circle_x - self.circle_radius,
            self.circle_y - self.circle_radius,
            self.circle_x + self.circle_radius,
            self.circle_y + self.circle_radius,
            width=self.circle_width,
            outline="#353535"
        )
        
        # Cercle de progression (coloré)
        self.circle_progress = self.canvas.create_arc(
            self.circle_x - self.circle_radius,
            self.circle_y - self.circle_radius,
            self.circle_x + self.circle_radius,
            self.circle_y + self.circle_radius,
            start=90,
            extent=-359.9,  # Presque un cercle complet
            width=self.circle_width,
            style=tk.ARC,
            outline="#4CAF50"  # Commence vert
        )
        
        # Texte au centre pour le compte à rebours
        self.time_label = self.canvas.create_text(
            self.circle_x,
            self.circle_y,
            text=str(self.remaining_time),
            fill="#ffffff",
            font=("Segoe UI", 32, "bold")
        )
        
        # Texte plus petit en dessous
        self.unit_label = self.canvas.create_text(
            self.circle_x,
            self.circle_y + 30,
            text="secondes",
            fill="#aaaaaa",
            font=("Segoe UI", 10)
        )
        
        return self.canvas
    
    def update_countdown_indicator(self):
        """Met à jour l'indicateur visuel de compte à rebours"""
        # Mettre à jour le texte du compte à rebours
        self.canvas.itemconfig(self.time_label, text=str(self.remaining_time))
        
        # Calculer l'étendue de l'arc (360 degrés représente le temps complet)
        # Commencer à 90 degrés (haut) et aller dans le sens horaire
        progress_percent = self.remaining_time / self.initial_time
        arc_extent = -359.9 * progress_percent  # Négatif pour l'orientation horaire
        
        # Mettre à jour l'arc de progression
        self.canvas.itemconfig(
            self.circle_progress, 
            extent=arc_extent
        )
        
        # Changer la couleur selon le temps restant
        if self.remaining_time <= 5:
            if self.remaining_time % 2 == 0:
                self.canvas.itemconfig(self.circle_progress, outline="#ff5555")  # Rouge clignotant
                self.canvas.itemconfig(self.time_label, fill="#ff5555")
            else:
                self.canvas.itemconfig(self.circle_progress, outline="#ff8888")  # Rouge plus clair
                self.canvas.itemconfig(self.time_label, fill="#ff8888")
        elif self.remaining_time <= 10:
            self.canvas.itemconfig(self.circle_progress, outline="#FFA500")  # Orange
            self.canvas.itemconfig(self.time_label, fill="#FFA500")
        else:
            self.canvas.itemconfig(self.circle_progress, outline="#4CAF50")  # Vert
            self.canvas.itemconfig(self.time_label, fill="#FFFFFF")  # Texte blanc

    def handle_response(self, event=None):
        """Appelé quand l'utilisateur répond au popup"""
        logger.info("Réponse reçue de l'utilisateur")
        self.destroy()
        self.on_response()
