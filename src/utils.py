import os

def get_asset_path(filename):
    """Retourne le chemin absolu d'un fichier dans le dossier assets."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "assets", filename)

def get_theme_path(theme_name="modern.tcl"):
    """Retourne le chemin absolu d'un fichier de thème."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "themes", theme_name)
