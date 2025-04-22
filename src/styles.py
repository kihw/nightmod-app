from tkinter import ttk
import logging

logger = logging.getLogger("NightMod.Styles")

def apply_custom_styles(style):
    """Applique les styles personnalisés à l'interface."""
    try:
        # Styles de base
        style.configure("TFrame", background="#1a1a1a")
        style.configure("TLabel", background="#1a1a1a", foreground="#FFFFFF")
        
        # Correction du contraste pour les boutons - fond plus foncé, texte blanc
        style.configure("TButton", 
                        background="#2d2d2d", 
                        foreground="#FFFFFF", 
                        padding=6, 
                        relief="flat")
        
        style.map("TButton", 
                  background=[("active", "#333333"), ("pressed", "#1a1a1a")],
                  foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF"), ("disabled", "#888888")])
                  
        # Correction du contraste pour les widgets d'entrée - fond plus foncé, texte blanc
        style.configure("TEntry", 
                        foreground="#FFFFFF",
                        fieldbackground="#333333", # Fond plus sombre
                        insertcolor="#FFFFFF",
                        padding=6)
                        
        style.map("TEntry",
                  fieldbackground=[("disabled", "#2a2a2a")],
                  foreground=[("disabled", "#999999")])
                        
        style.configure("TCombobox", 
                        foreground="#FFFFFF",
                        fieldbackground="#333333", # Fond plus sombre
                        arrowcolor="#4CAF50",
                        padding=6)
                        
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#333333"), ("disabled", "#2a2a2a")],
                  foreground=[("readonly", "#FFFFFF"), ("disabled", "#999999")])
                        
        style.configure("TSpinbox", 
                        foreground="#FFFFFF",
                        fieldbackground="#333333", # Fond plus sombre
                        arrowcolor="#4CAF50",
                        padding=6)
                        
        style.map("TSpinbox",
                  fieldbackground=[("readonly", "#333333"), ("disabled", "#2a2a2a")],
                  foreground=[("readonly", "#FFFFFF"), ("disabled", "#999999")])
                        
        # Styles pour les éléments de sélection
        style.configure("TCheckbutton", 
                        background="#1a1a1a", 
                        foreground="#FFFFFF")
                        
        style.map("TCheckbutton",
                  background=[("active", "#1a1a1a")],
                  foreground=[("active", "#FFFFFF"), ("disabled", "#888888")])
                  
        # Styles pour les séparateurs
        style.configure("TSeparator", background="#333333")
        
        # Styles pour les boutons d'action
        style.configure("Accent.TButton", 
                        background="#4CAF50", 
                        foreground="#FFFFFF",
                        padding=8)
                        
        style.map("Accent.TButton",
                  background=[("active", "#388E3C"), ("pressed", "#2E7D32")],
                  foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF"), ("disabled", "#AAAAAA")])
                  
        # Style pour le bouton de réponse de la popup
        style.configure("Wake.TButton", 
                        background="#4CAF50", 
                        foreground="#FFFFFF", 
                        font=("Segoe UI", 12, "bold"),
                        padding=(12, 10))
                        
        style.map("Wake.TButton",
                  background=[("active", "#388E3C"), ("pressed", "#2E7D32")],
                  foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF"), ("disabled", "#AAAAAA")])
        
        # Correction pour la liste déroulante de la combobox
        style.map("ComboboxPopdownFrame", fieldbackground=[("readonly", "#333333")])
        
        # Configuration globale pour les menus déroulants
        style.configure('TMenubutton', background='#333333', foreground='#FFFFFF')
        
        # Configuration pour les onglets si utilisés
        style.configure("TNotebook", background="#1a1a1a", tabmargins=[2, 5, 2, 0])
        style.configure("TNotebook.Tab", background="#2d2d2d", foreground="#FFFFFF", padding=[10, 2])
        style.map("TNotebook.Tab", 
                  background=[("selected", "#4CAF50"), ("active", "#388E3C")],
                  foreground=[("selected", "#FFFFFF"), ("active", "#FFFFFF")])
                  
        # Configurer l'apparence des menus déroulants au niveau global
        try:
            root = style.master
            root.option_add("*TCombobox*Listbox.background", "#333333")
            root.option_add("*TCombobox*Listbox.foreground", "#FFFFFF")
            root.option_add("*TCombobox*Listbox.selectBackground", "#4CAF50")
            root.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")
        except Exception as e:
            logger.warning(f"Impossible de configurer les menus déroulants: {e}")
                  
        logger.info("Styles personnalisés appliqués")
    except Exception as e:
        logger.error(f"Erreur lors de l'application des styles personnalisés: {e}")