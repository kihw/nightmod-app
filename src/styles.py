from tkinter import ttk
import logging

logger = logging.getLogger("NightMod.Styles")

def apply_custom_styles(style):
    """Applique les styles personnalisés à l'interface."""
    try:
        style.configure("TLabel", background="#1a1a1a", foreground="#FFFFFF")
        style.configure("TButton", background="#2d2d2d", foreground="#FFFFFF")
        style.map("TButton", background=[("active", "#333333")])
        style.configure("Accent.TButton", background="#4CAF50", foreground="#FFFFFF")
        style.map("Accent.TButton", background=[("active", "#388E3C")])
        logger.info("Styles personnalisés appliqués")
    except Exception as e:
        logger.error(f"Erreur lors de l'application des styles personnalisés: {e}")
