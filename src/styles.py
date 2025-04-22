import tkinter as tk
import logging

logger = logging.getLogger("NightMod.Styles")

def apply_custom_styles(style):
    """Applique les styles personnalisés à l'interface.
    
    Cette fonction configure les styles globaux de l'application.
    Elle devrait être appelée une seule fois au démarrage.
    
    Args:
        style: L'objet ttk.Style de l'application
    """
    try:
        # Récupérer l'objet root (fenêtre principale)
        root = style.master
        
        # --- Configuration des couleurs ---
        BG_COLOR = "#1a1a1a"        # Arrière-plan principal (très sombre)
        FG_COLOR = "#FFFFFF"        # Texte (blanc)
        INPUT_BG = "#333333"        # Fond des champs de saisie (gris foncé)
        BUTTON_BG = "#2d2d2d"       # Fond des boutons normaux (gris moyen)
        PRIMARY_COLOR = "#4CAF50"   # Couleur d'accent (vert)
        DANGER_COLOR = "#F44336"    # Couleur d'alerte (rouge)
        DISABLED_COLOR = "#666666"  # Couleur désactivée (gris)
        
        # --- Configuration globale ---
        
        # Styles pour les widgets standard (tk)
        # Ces configurations s'appliquent à tous les widgets, même ceux créés après cette fonction
        
        # Boutons
        root.option_add("*Button.background", BUTTON_BG)
        root.option_add("*Button.foreground", FG_COLOR)
        root.option_add("*Button.activeBackground", PRIMARY_COLOR)
        root.option_add("*Button.activeForeground", FG_COLOR)
        root.option_add("*Button.relief", "flat")
        
        # Entrées
        root.option_add("*Entry.background", INPUT_BG)
        root.option_add("*Entry.foreground", FG_COLOR)
        root.option_add("*Entry.insertBackground", FG_COLOR)  # Curseur
        root.option_add("*Entry.selectBackground", PRIMARY_COLOR)
        root.option_add("*Entry.selectForeground", FG_COLOR)
        root.option_add("*Entry.relief", "flat")
        
        # Spinbox
        root.option_add("*Spinbox.background", INPUT_BG)
        root.option_add("*Spinbox.foreground", FG_COLOR)
        root.option_add("*Spinbox.buttonBackground", BUTTON_BG)
        root.option_add("*Spinbox.relief", "flat")
        
        # Cases à cocher
        root.option_add("*Checkbutton.background", BG_COLOR)
        root.option_add("*Checkbutton.foreground", FG_COLOR)
        root.option_add("*Checkbutton.activeBackground", BG_COLOR)
        root.option_add("*Checkbutton.activeForeground", FG_COLOR)
        root.option_add("*Checkbutton.selectColor", INPUT_BG)
        
        # Menus déroulants
        root.option_add("*OptionMenu.background", INPUT_BG)
        root.option_add("*OptionMenu.foreground", FG_COLOR)
        root.option_add("*OptionMenu.activeBackground", PRIMARY_COLOR)
        root.option_add("*OptionMenu.activeForeground", FG_COLOR)
        
        # Popups des menus
        root.option_add("*Menu.background", INPUT_BG)
        root.option_add("*Menu.foreground", FG_COLOR)
        root.option_add("*Menu.activeBackground", PRIMARY_COLOR)
        root.option_add("*Menu.activeForeground", FG_COLOR)
        root.option_add("*Menu.relief", "flat")
        
        # Éléments de liste
        root.option_add("*Listbox.background", INPUT_BG)
        root.option_add("*Listbox.foreground", FG_COLOR)
        root.option_add("*Listbox.selectBackground", PRIMARY_COLOR)
        root.option_add("*Listbox.selectForeground", FG_COLOR)
        
        # Zone de texte
        root.option_add("*Text.background", INPUT_BG)
        root.option_add("*Text.foreground", FG_COLOR)
        root.option_add("*Text.selectBackground", PRIMARY_COLOR)
        root.option_add("*Text.selectForeground", FG_COLOR)
        
        # --- Configuration des styles ttk ---
        # Pour les widgets ttk qui pourraient encore être utilisés
        
        # Frames
        style.configure("TFrame", background=BG_COLOR)
        
        # Labels
        style.configure("TLabel", 
                       background=BG_COLOR, 
                       foreground=FG_COLOR)
        
        # Boutons
        style.configure("TButton", 
                       background=BUTTON_BG, 
                       foreground=FG_COLOR)
        
        style.configure("Accent.TButton", 
                       background=PRIMARY_COLOR, 
                       foreground=FG_COLOR)
        
        # Configuration maximale des widgets d'entrée
        style.configure("TEntry", 
                       foreground=FG_COLOR,
                       fieldbackground=INPUT_BG,
                       insertcolor=FG_COLOR)
        
        style.configure("TCombobox", 
                       foreground=FG_COLOR,
                       fieldbackground=INPUT_BG,
                       selectbackground=PRIMARY_COLOR,
                       selectforeground=FG_COLOR)
        
        # Configuration spéciale pour la fenêtre de popup
        style.configure("Wake.TButton", 
                        background=PRIMARY_COLOR, 
                        foreground=FG_COLOR, 
                        font=("Segoe UI", 12, "bold"),
                        padding=(12, 10))
        
        # Fonction utilitaire pour personnaliser un widget après sa création
        def fix_widget_colors(widget):
            """Applique manuellement les couleurs à un widget spécifique.
            Utile pour les cas où les options globales ne suffisent pas."""
            widget_type = widget.winfo_class()
            
            if widget_type == "Button":
                widget.config(bg=BUTTON_BG, fg=FG_COLOR, 
                             activebackground=PRIMARY_COLOR, activeforeground=FG_COLOR)
            
            elif widget_type == "Entry":
                widget.config(bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
            
            elif widget_type == "Checkbutton":
                widget.config(bg=BG_COLOR, fg=FG_COLOR, selectcolor=INPUT_BG,
                             activebackground=BG_COLOR, activeforeground=FG_COLOR)
            
            elif widget_type in ["Menu", "Menubutton"]:
                widget.config(bg=INPUT_BG, fg=FG_COLOR,
                             activebackground=PRIMARY_COLOR, activeforeground=FG_COLOR)
            
            # Récursion pour les conteneurs
            if widget_type in ["Frame", "Toplevel", "LabelFrame"]:
                widget.config(bg=BG_COLOR)
                for child in widget.winfo_children():
                    fix_widget_colors(child)
        
        # Exposer la fonction utilitaire au niveau global pour pouvoir l'utiliser ailleurs
        apply_custom_styles.fix_widget_colors = fix_widget_colors
        
        logger.info("Styles personnalisés appliqués avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'application des styles personnalisés: {e}")     
        